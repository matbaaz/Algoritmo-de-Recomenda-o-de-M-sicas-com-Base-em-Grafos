#!/usr/bin/env python3
"""
Reduz o arquivo de historico de escuta (muito grande) para um CSV pequeno,
mantendo so o que cabe no grafo do Aura:
  - apenas musicas que existem no catalogo (data_raw), ja sem as que ficariam
    sem genero apos a limpeza;
  - uma amostra aleatoria (reprodutivel) de usuarios com escutas suficientes;
  - no maximo N escutas por usuario (as mais ouvidas).

Le o arquivo em chunks (nao carrega tudo na memoria) e faz 2 passadas.

Uso:
  python scripts/shrink_listening.py --input User_Listening_History.csv \
      --catalog data_raw --out listening_small.csv
"""
import argparse
import random
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

from prepare_data import NON_GENRE_TAGS  # mesma lista de tags que nao sao genero

CANDIDATES = {
    "user_id": ["user_id", "user", "userid"],
    "track_id": ["track_id", "track", "trackid"],
    "playcount": ["playcount", "play_count", "count", "plays"],
}


def detect_columns(path: str) -> dict:
    header = pd.read_csv(path, nrows=0).columns.tolist()
    lower = {h.lower().strip(): h for h in header}
    found = {}
    for key, options in CANDIDATES.items():
        for opt in options:
            if opt in lower:
                found[key] = lower[opt]
                break
    missing = [k for k in CANDIDATES if k not in found]
    if missing:
        print(f"Nao achei as colunas {missing}. Cabecalho do arquivo: {header}")
        print("Ajuste CANDIDATES no topo do script ou me envie o cabecalho.")
        sys.exit(1)
    return found


def valid_tracks(catalog: Path) -> set:
    """track_ids que terao pelo menos 1 genero real apos a limpeza."""
    genres = pd.read_csv(catalog / "genres.csv")
    has = pd.read_csv(catalog / "has.csv", dtype={"music_id": str})
    keep_genres = set(genres.loc[~genres["name"].isin(NON_GENRE_TAGS), "id"])
    return set(has.loc[has["genre_id"].isin(keep_genres), "music_id"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--catalog", default="data_raw")
    ap.add_argument("--out", default="listening_small.csv")
    ap.add_argument("--users", type=int, default=2000, help="usuarios na amostra")
    ap.add_argument("--max-per-user", type=int, default=30)
    ap.add_argument("--min-listens", type=int, default=20,
                    help="so sorteia usuarios com pelo menos X escutas no catalogo")
    ap.add_argument("--chunksize", type=int, default=1_000_000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    cols = detect_columns(args.input)
    use = [cols["user_id"], cols["track_id"], cols["playcount"]]
    valid = valid_tracks(Path(args.catalog))
    print(f"Musicas validas no catalogo: {len(valid):,}")

    def chunks():
        for ch in pd.read_csv(args.input, usecols=use, chunksize=args.chunksize,
                              dtype={cols["user_id"]: str, cols["track_id"]: str}):
            ch = ch.rename(columns={v: k for k, v in cols.items()})
            yield ch[ch["track_id"].isin(valid)]

    # Passada 1: quantas escutas (no catalogo) tem cada usuario
    counts = Counter()
    for i, ch in enumerate(chunks(), 1):
        counts.update(ch["user_id"].value_counts().to_dict())
        print(f"  passada 1: chunk {i}", end="\r")
    eligible = sorted(u for u, n in counts.items() if n >= args.min_listens)
    print(f"\nUsuarios no catalogo: {len(counts):,} | elegiveis (>= {args.min_listens}): {len(eligible):,}")
    chosen = set(random.Random(args.seed).sample(eligible, min(args.users, len(eligible))))

    # Passada 2: so as linhas dos usuarios sorteados
    parts = []
    for i, ch in enumerate(chunks(), 1):
        parts.append(ch[ch["user_id"].isin(chosen)])
        print(f"  passada 2: chunk {i}", end="\r")
    df = pd.concat(parts)
    df = df.groupby(["user_id", "track_id"], as_index=False)["playcount"].sum()
    df = (df.sort_values(["user_id", "playcount"], ascending=[True, False])
            .groupby("user_id").head(args.max_per_user))
    df.to_csv(args.out, index=False)

    size_mb = Path(args.out).stat().st_size / 1e6
    print(f"\nUsuarios: {df['user_id'].nunique():,} | escutas (LISTEN): {len(df):,} | "
          f"arquivo: {size_mb:.1f} MB -> {args.out}")


if __name__ == "__main__":
    main()
