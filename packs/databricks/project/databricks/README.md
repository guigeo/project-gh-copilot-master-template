# Databricks

Scaffold do tema Databricks (compõe sobre python + pyspark).

## Estrutura

- `databricks.yml` — bundle (DAB) com targets `dev` (mode development, default) e `prod`.
- `resources/*_job.yml` — job serverless rodando `src/nome_pacote/main.py`.
- `resources/*_pipeline.yml` — pipeline Lakeflow/DLT serverless com expectativas de qualidade.
- `src/nome_pacote/lakeflow_pipeline.py` — declaração das tabelas bronze/silver (roda só no pipeline).

## Primeiros passos

1. Preencha `workspace.host` nos targets do `databricks.yml`.
2. `databricks bundle validate`
3. `databricks bundle deploy -t dev` e `databricks bundle run -t dev nome_pacote_job`

## Convenções

- Recurso novo = yaml novo em `resources/` (ver prompt `add-bundle-resource`); nada de criar pela UI em prod.
- Lógica de transformação fica em módulos testáveis (`transformations.py`); o pipeline só declara tabelas.
- O que muda entre ambientes vai em `variables`/`${bundle.target}`, nunca duplicando yaml.
