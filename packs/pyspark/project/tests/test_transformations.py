from pyspark.sql import SparkSession

from nome_pacote.transformations import normalizar_colunas, remover_duplicatas


def test_normalizar_colunas(spark: SparkSession) -> None:
    df = spark.createDataFrame([(1, "a")], ["ID Cliente", " Nome "])

    resultado = normalizar_colunas(df)

    assert resultado.columns == ["id_cliente", "nome"]


def test_remover_duplicatas_mantem_mais_recente(spark: SparkSession) -> None:
    df = spark.createDataFrame(
        [
            (1, "antigo", "2024-01-01"),
            (1, "novo", "2024-06-01"),
            (2, "unico", "2024-03-01"),
        ],
        ["id", "valor", "atualizado_em"],
    )

    resultado = remover_duplicatas(df, chaves=["id"], coluna_ordem="atualizado_em")

    linhas = {r["id"]: r["valor"] for r in resultado.collect()}
    assert linhas == {1: "novo", 2: "unico"}
