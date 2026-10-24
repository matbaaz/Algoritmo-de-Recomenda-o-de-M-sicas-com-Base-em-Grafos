"""
Tratamento do Music_Info.csv (Million Song Dataset - Spotify + Last.fm)
para import no Neo4j / Aura, seguindo a modelagem do projeto:

  (Artista)-[:COMPOSED]->(Musica)
  (Musica)-[:HAS]->(Gênero)
  (Artista)-[:BELONG]->(Gênero)

Saida (um CSV por tipo de no / relacionamento), em --out (padrao: data/):
  music.csv    id, name, length, uploaded_at
  artists.csv  id, name, age
  genres.csv   id, name
  compose.csv  artist_id, music_id, at
  has.csv      music_id, genre_id
  belong.csv   artist_id, genre_id

Uso:
  pip install pandas
  python scripts/prepare_data.py --input Music_Info.csv --out data_raw --raw
"""
import argparse
from pathlib import Path

import pandas as pd

# Configuracao
# ----------------------------------------------------------------------------

# Tags do Last.fm que NÃO sao genero musical (décadas, país/idioma,
# humor/descritor, instrumento/voz, formato).
NON_GENRE_TAGS = {
    # décadas
    "00s", "60s", "70s", "80s", "90s",
    # país / idioma
    "american", "british", "french", "german", "japanese", "polish",
    "russian", "swedish",
    # humor / descritores
    "acoustic", "beautiful", "chill", "chillout", "love", "mellow", "oldies",
    # instrumento / voz
    "guitar", "piano", "instrumental", "female_vocalists", "male_vocalists",
    # formato / outros
    "cover", "soundtrack", "singer_songwriter",
}

# Ano de referência para estimar Artista.Age (maior ano do dataset = 2022).
REF_YEAR = 2022

# Anos abaixo disso sao tratados como invalidos (o dataset tem uns 13 registros
# com ano 1900 / placeholders).
MIN_VALID_YEAR = 1920

# Musica.uploaded_at e COMPOSED.at NAO existem no dataset. Se True, usa 01/01 do
# ano de lancamento como aproximação; se False, deixa em branco (propriedade
# não sera criada no Neo4j).
DATE_FROM_YEAR = True

# Um artista "pertence" a um genero se esse genero aparece em pelo menos
# 20% das musicas dele (o genero mais frequente do artista sempre entra).
# Use 0 para ligar o artista a TODO genero de qualquer musica dele.
MIN_ARTIST_GENRE_SHARE = 0.20

# Se True, descarta musicas que ficaram sem nenhum genero.
DROP_TRACKS_WITHOUT_GENRE = False


# Funcoes

def split_genres(tags, raw: bool = False) -> list:
    """'rock, indie, 90s' -> ['indie', 'rock'] (sem tags que nao sao genero).
    Com raw=True mantem todas as tags."""
    if not isinstance(tags, str):
        return []
    found = {t.strip().lower() for t in tags.split(",") if t.strip()}
    return sorted(found if raw else found - NON_GENRE_TAGS)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="Music_Info.csv")
    ap.add_argument("--out", default="data")
    ap.add_argument("--raw", action="store_true",
                    help="carga bruta: todas as tags viram Genre e nao gera belong.csv")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Leitura e limpeza basica 
    df = pd.read_csv(
        args.input,
        usecols=["track_id", "name", "artist", "tags", "year", "duration_ms"],
    )
    print(f"Linhas lidas: {len(df):,}")

    for col in ("track_id", "name", "artist"):
        df[col] = df[col].astype("string").str.strip()
    df = df.dropna(subset=["track_id", "name", "artist"])
    df = df[(df["name"] != "") & (df["artist"] != "")]
    df = df.drop_duplicates(subset="track_id").reset_index(drop=True)
    print(f"Apos limpeza/dedupe por track_id: {len(df):,}")

    # Generos a partir das tags
    df["genres"] = df["tags"].map(lambda t: split_genres(t, raw=args.raw))
    sem_genero = (df["genres"].str.len() == 0).sum()
    print(f"Modo: {'BRUTO (todas as tags)' if args.raw else 'FILTRADO'}")
    print(f"Musicas sem genero: {sem_genero:,} ({sem_genero / len(df):.1%})")
    if DROP_TRACKS_WITHOUT_GENRE and not args.raw:
        df = df[df["genres"].str.len() > 0].reset_index(drop=True)
        print(f"Descartadas; restam {len(df):,} musicas")

    genre_names = sorted({g for gs in df["genres"] for g in gs})
    genres = pd.DataFrame({"id": range(1, len(genre_names) + 1),
                           "name": genre_names})
    genre_id = dict(zip(genres["name"], genres["id"]))

    # Artistas 
    df["year_ok"] = df["year"].where(df["year"] >= MIN_VALID_YEAR)
    first_year = df.groupby("artist")["year_ok"].min()

    artists = pd.DataFrame({"name": sorted(df["artist"].unique())})
    artists.insert(0, "id", range(1, len(artists) + 1))
    # Idade estimada = anos desde a primeira musica no dataset.
    # Pode (e deve) ser revisada a mao em artists.csv.
    artists["age"] = (REF_YEAR - artists["name"].map(first_year)).astype("Int64")
    artist_id = dict(zip(artists["name"], artists["id"]))

    velhos = (artists["age"] > 80).sum()
    sem_idade = artists["age"].isna().sum()
    print(f"Artistas: {len(artists):,} | sem idade estimada: {sem_idade:,} "
          f"| idade > 80 (revisar): {velhos:,}")

    # Musicas
    music = pd.DataFrame({
        "id": df["track_id"],
        "name": df["name"],
        "length": (df["duration_ms"] / 1000).round().astype(int),
    })
    if DATE_FROM_YEAR:
        date = df["year_ok"].map(lambda y: f"{int(y)}-01-01" if pd.notna(y) else "")
    else:
        date = ""
    music["uploaded_at"] = date

    # Relacionamentos
    # COMPOSE: Artist -> Music
    compose = pd.DataFrame({
        "artist_id": df["artist"].map(artist_id),
        "music_id": df["track_id"],
        "at": date,
    })

    # HAS: Music -> Genre
    has = (df[["track_id", "genres"]].explode("genres").dropna(subset=["genres"]))
    has = pd.DataFrame({
        "music_id": has["track_id"],
        "genre_id": has["genres"].map(genre_id),
    })

    # BELONG: Artist -> Genre (derivado das musicas do artista)
    # No modo --raw ele nao e gerado: sera derivado em Cypher após a limpeza.
    ag = (df[["artist", "genres"]].explode("genres").dropna(subset=["genres"]))
    n_tracks = df.groupby("artist").size().rename("n_tracks")
    ag = ag.groupby(["artist", "genres"]).size().rename("n").reset_index()
    ag = ag.join(n_tracks, on="artist")
    ag["share"] = ag["n"] / ag["n_tracks"]
    is_top = ag["share"] == ag.groupby("artist")["share"].transform("max")
    ag = ag[(ag["share"] >= MIN_ARTIST_GENRE_SHARE) | is_top]
    belong = pd.DataFrame({
        "artist_id": ag["artist"].map(artist_id),
        "genre_id": ag["genres"].map(genre_id),
    }).drop_duplicates()

    # Exportacao
    files = {
        "music.csv": music, "artists.csv": artists, "genres.csv": genres,
        "compose.csv": compose, "has.csv": has,
    }
    if not args.raw:
        files["belong.csv"] = belong
    for fname, frame in files.items():
        frame.to_csv(out / fname, index=False, encoding="utf-8")

    n_nodes = len(music) + len(artists) + len(genres)
    n_rels = len(compose) + len(has) + len(belong)
    print("\nResumo")
    for fname, frame in files.items():
        print(f"  {fname:<12} {len(frame):>9,} linhas")
    print(f"  Nos totais:             {n_nodes:,}")
    print(f"  Relacionamentos totais: {n_rels:,}")
    print(f"\nArquivos gravados em: {out.resolve()}")


if __name__ == "__main__":
    main()
