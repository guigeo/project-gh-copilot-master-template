---
applyTo: "**/*.sql,**/*.hql"
description: Padrões de Hive (HiveQL) — partições, bucketing, formatos colunares, partition pruning, map join e vetorização.
---

# Instruções para Hive (HiveQL)

Complementa o pack `sql` com o que é específico do Hive.

## Partições

- Particione por coluna de **baixa cardinalidade** e usada em filtro (ex.: data como `dt=2026-01-01`); nunca por coluna de alta cardinalidade (gera milhões de diretórios).
- **Sempre** filtre pela coluna de partição com literal para haver *partition pruning*; função em volta da coluna mata o pruning.
- Para carga dinâmica, configure `hive.exec.dynamic.partition.mode=nonstrict`, mas controle o nº de partições geradas.
- Tabela externa apontando para dados novos: `MSCK REPAIR TABLE` ou `ALTER TABLE ... ADD PARTITION` para registrar partições.

## Formato e arquivos

- Use formato colunar **ORC** ou **Parquet** com compressão (Snappy/Zlib); evite TEXTFILE em tabela analítica.
- Evite o problema de *small files*: controle o nº de reducers / use `hive.merge.*` para compactar a saída.
- Aproveite o *predicate pushdown* e o *column pruning* do ORC/Parquet — selecione só as colunas necessárias.

## Joins e skew

- Para join com tabela pequena, deixe o **map join** atuar (`hive.auto.convert.join=true`); confirme no `EXPLAIN` que virou *Map Join*.
- Trate skew de join com `hive.optimize.skewjoin=true` ou separe a chave problemática.
- **Bucketing** (`CLUSTERED BY ... INTO n BUCKETS`) ajuda joins e amostragem quando as duas tabelas usam o mesmo bucketing.

## Execução

- Mantenha **vetorização** ligada (`hive.vectorized.execution.enabled=true`) — exige formato colunar.
- Rode `ANALYZE TABLE ... COMPUTE STATISTICS` (e `FOR COLUMNS`) para o CBO funcionar.
- Não use `ORDER BY` em volume grande (reduz a um único reducer); prefira `DISTRIBUTE BY` + `SORT BY` quando ordenação global não for necessária.

## Cuidados

- Saiba a diferença entre tabela **MANAGED** (DROP apaga dados) e **EXTERNAL** (não apaga); `INSERT OVERWRITE` substitui a partição inteira.
- Não fixe caminhos absolutos de cluster, nomes de schema ou credenciais no código.
