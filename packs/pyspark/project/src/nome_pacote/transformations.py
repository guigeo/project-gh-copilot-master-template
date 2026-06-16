"""Transformações puras (DataFrame -> DataFrame), testáveis sem cluster.

Leitura e escrita ficam nas bordas do pipeline; aqui só entra lógica.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def normalizar_colunas(df: DataFrame) -> DataFrame:
    """Renomeia colunas para snake_case minúsculo, sem espaços."""
    renomeadas = {c: c.strip().lower().replace(" ", "_") for c in df.columns}
    return df.withColumnsRenamed(renomeadas)


def remover_duplicatas(df: DataFrame, chaves: list[str], coluna_ordem: str) -> DataFrame:
    """Mantém a linha mais recente por chave de negócio, segundo `coluna_ordem`."""
    from pyspark.sql.window import Window

    janela = Window.partitionBy(*chaves).orderBy(F.col(coluna_ordem).desc())
    return df.withColumn("_rn", F.row_number().over(janela)).filter(F.col("_rn") == 1).drop("_rn")
