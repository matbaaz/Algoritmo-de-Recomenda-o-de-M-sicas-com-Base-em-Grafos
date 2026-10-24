"""
Etapa 2 do tratamento: gera User, LISTEN, FOLLOW, LIKE e CONNECT a partir do
histórico de escuta reduzido (listening_small.csv) e do catalogo ja gerado
(data_raw/: compose.csv, has.csv, genres.csv).

Origem de cada dado:
  users.csv   id curto (u0001...) + hash original (source_id).
              age e sex: SINTETICOS (nao existem no dataset), sorteio com seed fixa.
  listen.csv  REAL: playcount -> quantity. liked = quantity >= LIKED_MIN_PLAYS.
  follow.csv  DERIVADO: artistas mais ouvidos pelo usuario.
  like.csv    DERIVADO: generos mais ouvidos pelo usuario.
  connect.csv DERIVADO: usuarios com gosto parecido (similaridade de cosseno
              sobre os artistas ouvidos).

Uso:
python scripts/prepare_users.py --listening listening_small.csv --catalog data_raw --out data_raw
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

# Configuração
LIKED_MIN_PLAYS = 3        # liked = true se quantity >= 3
FOLLOW_TOP = 3             # artistas seguidos por usuario (top por reproduções)
FOLLOW_MIN_PLAYS = 3       # so segue se ouviu >= 3 vezes no total
LIKE_TOP = 3               # gêneros curtidos por usuario
CONNECT_TOP = 3            # vizinhos mais parecidos por usuario
CONNECT_MIN_SIM = 0.10     # similaridade minima para conectar
AGE_MEAN, AGE_STD, AGE_MIN, AGE_MAX = 28, 8, 14, 65

# Mesma lista de tags que NÃO sao gênero de prepare_data.py.
NON_GENRE_TAGS = {
    "00s", "60s", "70s", "80s", "90s",
    "american", "british", "french", "german", "japanese", "polish",
    "russian", "swedish",
    "acoustic", "beautiful", "chill", "chillout", "love", "mellow", "oldies",
    "guitar", "piano", "instrumental", "female_vocalists", "male_vocalists",
    "cover", "soundtrack", "singer_songwriter",
}


def top_n(df: pd.DataFrame, key: str, score: str, n: int) -> pd.DataFrame:
    """Top n linhas de `key` por usuario, ordenando por score (desc)."""
    return (df.sort_values(["user_id", score], ascending=[True, False])
              .groupby("user_id").head(n))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--listening", default="listening_small.csv")
    ap.add_argument("--catalog", default="data_raw")
    ap.add_argument("--out", default="data_raw")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--no-synthetic", action="store_true",
                    help="deixa age e sex em branco em vez de gerar dados sinteticos")
    args = ap.parse_args()
    cat, out = Path(args.catalog), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Leitura
    hist = pd.read_csv(args.listening, dtype={"user_id": str, "track_id": str})
    hist = hist.groupby(["user_id", "track_id"], as_index=False)["playcount"].sum()
    compose = pd.read_csv(cat / "compose.csv", dtype={"music_id": str})
    has = pd.read_csv(cat / "has.csv", dtype={"music_id": str})
    genres = pd.read_csv(cat / "genres.csv")

    valid_genres = set(genres.loc[~genres["name"].isin(NON_GENRE_TAGS), "id"])
    has = has[has["genre_id"].isin(valid_genres)]
    valid_tracks = set(has["music_id"])
    antes = len(hist)
    hist = hist[hist["track_id"].isin(valid_tracks)]
    print(f"Escutas: {antes:,} -> {len(hist):,} (so musicas com genero valido)")

    # Users
    hashes = sorted(hist["user_id"].unique())
    uid = {h: f"u{i:04d}" for i, h in enumerate(hashes, 1)}
    users = pd.DataFrame({"id": [uid[h] for h in hashes], "source_id": hashes})
    if args.no_synthetic:
        users["age"] = pd.array([pd.NA] * len(users), dtype="Int64")
        users["sex"] = ""
    else:
        rng = np.random.default_rng(args.seed)
        age = rng.normal(AGE_MEAN, AGE_STD, len(users)).round()
        users["age"] = np.clip(age, AGE_MIN, AGE_MAX).astype(int)
        users["sex"] = rng.choice(["M", "F", "Outro"], len(users), p=[0.48, 0.48, 0.04])
    users = users[["id", "source_id", "age", "sex"]]

    h = hist.assign(user_id=hist["user_id"].map(uid))

    # LISTEN
    listen = pd.DataFrame({
        "user_id": h["user_id"],
        "music_id": h["track_id"],
        "quantity": h["playcount"],
        "liked": np.where(h["playcount"] >= LIKED_MIN_PLAYS, "true", "false"),
    })

    # FOLLOW
    t2a = compose.drop_duplicates("music_id").set_index("music_id")["artist_id"]
    ua = (h.assign(artist_id=h["track_id"].map(t2a))
            .dropna(subset=["artist_id"])
            .groupby(["user_id", "artist_id"], as_index=False)["playcount"].sum())
    ua["artist_id"] = ua["artist_id"].astype(int)
    follow = top_n(ua[ua["playcount"] >= FOLLOW_MIN_PLAYS], "artist_id", "playcount", FOLLOW_TOP)
    follow = follow[["user_id", "artist_id"]]

    # LIKE
    ug = (h.merge(has, left_on="track_id", right_on="music_id")
            .groupby(["user_id", "genre_id"], as_index=False)["playcount"].sum())
    like = top_n(ug, "genre_id", "playcount", LIKE_TOP)[["user_id", "genre_id"]]

    # CONNECT
    # Similaridade de cosseno entre usuarios sobre o vetor de reproduções por artista.
    users_idx = {u: i for i, u in enumerate(users["id"])}
    arts = sorted(ua["artist_id"].unique())
    art_idx = {a: i for i, a in enumerate(arts)}
    M = np.zeros((len(users_idx), len(arts)), dtype=np.float32)
    M[ua["user_id"].map(users_idx).values, ua["artist_id"].map(art_idx).values] = np.log1p(ua["playcount"].values)
    norm = np.linalg.norm(M, axis=1, keepdims=True)
    norm[norm == 0] = 1
    S = (M / norm) @ (M / norm).T
    np.fill_diagonal(S, 0)
    pairs = set()
    ids = users["id"].tolist()
    for i in range(len(ids)):
        for j in np.argsort(-S[i])[:CONNECT_TOP]:
            if S[i, j] >= CONNECT_MIN_SIM:
                a, b = sorted((ids[i], ids[j]))
                pairs.add((a, b))
    connect = pd.DataFrame(sorted(pairs), columns=["user_a", "user_b"])

    # Saida
    files = {"users.csv": users, "listen.csv": listen, "follow.csv": follow,
             "like.csv": like, "connect.csv": connect}
    for name, frame in files.items():
        frame.to_csv(out / name, index=False, encoding="utf-8")

    print("\nResumo")
    for name, frame in files.items():
        print(f"  {name:<12}{len(frame):>9,} linhas")
    print(f"  Novos nos (User): {len(users):,}")
    print(f"  Novos relacionamentos: {len(listen) + len(follow) + len(like) + len(connect):,}")
    print(f"  Usuarios sem FOLLOW: {users['id'].nunique() - follow['user_id'].nunique()}"
          f" | sem CONNECT: {len(users) - len(set(connect.user_a) | set(connect.user_b))}")
    print(f"\nArquivos gravados em: {out.resolve()}")


if __name__ == "__main__":
    main()
