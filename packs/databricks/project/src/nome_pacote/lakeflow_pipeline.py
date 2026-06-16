"""Pipeline declarativo (Lakeflow/DLT) — só roda dentro do pipeline Databricks.

Mantenha aqui apenas a declaração das tabelas; lógica reutilizável vai para
módulos comuns (ex.: transformations.py), testáveis localmente.
"""

import dlt
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.getActiveSession()


@dlt.table(comment="Bronze: ingestão bruta via Auto Loader.")
def bronze_exemplo():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/Volumes/main/raw/exemplo")
    )


@dlt.table(comment="Silver: registros válidos e tipados.")
@dlt.expect_or_drop("valor_nao_negativo", "valor >= 0")
@dlt.expect_or_drop("id_presente", "id IS NOT NULL")
def silver_exemplo():
    return dlt.read_stream("bronze_exemplo").withColumn("ingerido_em", F.current_timestamp())
