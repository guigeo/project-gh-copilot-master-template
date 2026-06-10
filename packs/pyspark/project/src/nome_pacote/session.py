"""Criação centralizada da SparkSession."""

from pyspark.sql import SparkSession


def get_spark(app_name: str = "nome_pacote") -> SparkSession:
    """Retorna a SparkSession ativa ou cria uma nova.

    Em cluster (Databricks, EMR, etc.) reaproveita a sessão existente;
    localmente cria uma sessão standalone. Configurações de cluster
    (master, memória, etc.) ficam fora do código.
    """
    return SparkSession.builder.appName(app_name).getOrCreate()
