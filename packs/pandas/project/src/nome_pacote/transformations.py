"""Transformações puras (DataFrame -> DataFrame), testáveis sem I/O.

Escritas em estilo Copy-on-Write: cada função retorna um novo DataFrame e
nunca depende de mutar uma view. Leitura e escrita ficam em `io`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Renomeia colunas para snake_case minúsculo, sem espaços nas bordas."""
    renomeadas = {c: c.strip().lower().replace(" ", "_") for c in df.columns}
    return df.rename(columns=renomeadas)


def remover_duplicatas(
    df: pd.DataFrame, chaves: list[str], coluna_ordem: str
) -> pd.DataFrame:
    """Mantém a linha mais recente por chave de negócio, segundo `coluna_ordem`."""
    return (
        df.sort_values(coluna_ordem)
        .drop_duplicates(subset=chaves, keep="last")
        .reset_index(drop=True)
    )


def faixa_valor(df: pd.DataFrame, coluna: str = "valor") -> pd.DataFrame:
    """Adiciona `faixa` (baixo/medio/alto) de forma vetorizada — sem apply linha a linha."""
    v = df[coluna]
    faixa = np.select(
        [v < 100, v < 1000],
        ["baixo", "medio"],
        default="alto",
    )
    return df.assign(faixa=pd.Series(faixa, index=df.index, dtype="string"))


def juntar_clientes(vendas: pd.DataFrame, clientes: pd.DataFrame) -> pd.DataFrame:
    """Enriquece vendas com dados do cliente.

    Usa `validate="m:1"` (muitas vendas para um cliente) para falhar cedo se a
    cardinalidade for violada, e `indicator` para flagrar chaves órfãs.
    """
    juncao = vendas.merge(
        clientes,
        on="id_cliente",
        how="left",
        validate="m:1",
        indicator=True,
    )
    return juncao.drop(columns="_merge")
