---
applyTo: "**/*.py,**/databricks.yml,**/resources/**/*.yml"
description: Padrões de Databricks — Unity Catalog, secrets, bundles (DABs), Lakeflow/DLT, serverless e notebooks finos.
---

# Instruções para Databricks

## Unity Catalog e dados

- Referencie tabelas com nome de três níveis: `catalogo.schema.tabela`; nunca abrevie em produção.
- Parametrize catálogo/schema por ambiente (variável do bundle ou config); não fixe `dev`/`prod` no código.
- Use Volumes (`/Volumes/...`) para arquivos; não use `dbfs:/` nem montagens legadas.

## Segurança

- Segredos só via `dbutils.secrets.get(scope, key)` ou variáveis de ambiente; nunca token/senha no código ou notebook.
- Não fixe host de workspace no código; isso pertence ao `databricks.yml` (targets).

## Deploy e infraestrutura

- Todo recurso (job, pipeline, schedule) é declarado no bundle (`databricks.yml` + `resources/*.yml`); não crie recursos manualmente pela UI em produção.
- Prefira compute serverless; se precisar de cluster, declare no bundle, não no código.
- Deploy sempre por target: `databricks bundle deploy -t dev|prod`.

## Código e notebooks

- Notebooks são camada fina de orquestração; lógica de transformação vive em módulos `src/` (funções puras `DataFrame -> DataFrame`, testáveis localmente com a fixture `spark`).
- Em pipelines Lakeflow, use a API atual `from pyspark import pipelines as dp` (`@dp.table`, `@dp.expect_or_drop`, `spark.readStream.table(...)`); a antiga `import dlt` ainda funciona, mas prefira `pyspark.pipelines`.
- Declare expectativas de qualidade (`@dp.expect_or_drop`/`@dp.expect`) nas tabelas críticas.
- Não use `display()`/`print` em código de produção; use `logging`.
