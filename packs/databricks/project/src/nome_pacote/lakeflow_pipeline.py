"""Pipeline declarativo (Lakeflow Declarative Pipelines) — roda dentro do pipeline Databricks.

Mantenha aqui apenas a declaração das tabelas; lógica reutilizável vai para
módulos comuns (ex.: transformations.py), testáveis localmente.

API atual do Lakeflow: `from pyspark import pipelines as dp`. A antiga
`import dlt` ainda funciona, mas `pyspark.pipelines` é o caminho recomendado.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from pyspark import pipelines as dp

spark = SparkSession.getActiveSession()


@dp.table(comment="Bronze: ingestão bruta via Auto Loader.")
def bronze_exemplo():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        # Schema evolution: resgata campos inesperados em vez de falhar.
        .option("cloudFiles.schemaEvolutionMode", "rescue")
        .load("/Volumes/main/raw/exemplo")
    )


@dp.table(comment="Silver: registros válidos e tipados.")
@dp.expect_or_drop("valor_nao_negativo", "valor >= 0")
@dp.expect_or_drop("id_presente", "id IS NOT NULL")
def silver_exemplo():
    return spark.readStream.table("bronze_exemplo").withColumn("ingerido_em", F.current_timestamp())
