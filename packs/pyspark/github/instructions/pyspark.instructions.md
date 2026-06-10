---
applyTo: "**/*.py"
description: Padrões de PySpark — DataFrame API, schemas explícitos, shuffle, joins, UDFs e testabilidade.
---

# Instruções para PySpark

## Sessão e ambiente

- Obtenha a sessão via `get_spark()` (módulo `session`); não crie `SparkSession` solta no meio da lógica.
- Não use `master("local[*]")` em código de produção; isso é configuração de teste/execução, não de lógica.
- Não fixe configurações de cluster no código; receba via configuração externa.

## API e schemas

- Prefira a DataFrame API; não use RDDs sem justificativa explícita.
- Declare schema explícito (`StructType` ou string DDL) ao ler CSV/JSON; evite `inferSchema` em produção.
- Prefira funções de `pyspark.sql.functions` a UDFs Python; se UDF for inevitável, prefira `pandas_udf`.
- Encadeie transformações com `.transform()` ou variáveis intermediárias nomeadas; evite expressões gigantes ilegíveis.

## Performance

- Não use `collect()`, `toPandas()` ou `count()` em DataFrames grandes sem necessidade justificada.
- Em join com tabela pequena, use `broadcast()`; em joins grandes, confirme que as chaves não têm skew severo.
- Filtre e selecione colunas o mais cedo possível (predicate pushdown e column pruning).
- Use `cache()`/`persist()` apenas quando o DataFrame for reutilizado; libere com `unpersist()` ao final.
- Ao escrever, controle o número de arquivos com `repartition()`/`coalesce()`; evite milhares de arquivos pequenos.

## Testabilidade

- Escreva transformações como funções puras `DataFrame -> DataFrame`, sem I/O dentro; leitura e escrita ficam nas bordas.
- Teste com a fixture `spark` de `tests/conftest.py` (sessão local) e DataFrames pequenos via `createDataFrame`.
- Compare resultados com `assertDataFrameEqual` de `pyspark.testing` ou `collect()` sobre dados pequenos.
- Não use `.show()` ou `print` de DataFrame em produção; use `logging` para métricas (contagens, partições).
