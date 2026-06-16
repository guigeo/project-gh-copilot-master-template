"""Leitura e escrita nas bordas do pipeline. A lógica fica em `transformations`.

Habilite Copy-on-Write no início da aplicação (padrão no pandas 3.0):

    import pandas as pd
    pd.options.mode.copy_on_write = True
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def ler_csv(
    caminho: str | Path,
    *,
    colunas: list[str] | None = None,
    dtypes: dict[str, str] | None = None,
    datas: list[str] | None = None,
) -> pd.DataFrame:
    """Lê CSV pedindo só o necessário e com backend Arrow (menos memória)."""
    return pd.read_csv(
        caminho,
        usecols=colunas,
        dtype=dtypes,
        parse_dates=datas,
        dtype_backend="pyarrow",
    )


def ler_parquet(caminho: str | Path, *, colunas: list[str] | None = None) -> pd.DataFrame:
    """Lê Parquet (preferível a CSV para intermediários) com backend Arrow."""
    return pd.read_parquet(caminho, columns=colunas, dtype_backend="pyarrow")


def escrever_parquet(df: pd.DataFrame, caminho: str | Path) -> None:
    """Persiste em Parquet comprimido; cria o diretório-pai se faltar."""
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(destino, compression="snappy", index=False)
