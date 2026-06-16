---
name: hive-tuning
description: Use esta skill para diagnosticar e otimizar queries Hive lentas ou caras — partition pruning, map join, skew, small files, formato e vetorização.
---

Ao otimizar uma query Hive, siga nesta ordem:

1. **EXPLAIN**: leia o plano e veja se há *partition pruning* (só as partições filtradas são lidas), *Map Join* vs *Common Join* e nº de stages/reducers.
2. **Partition pruning**: confirme o filtro literal na coluna de partição; remova função em volta da coluna. Sem pruning, o job varre a tabela inteira.
3. **Formato**: tabela em TEXTFILE? Migrar para ORC/Parquet + Snappy costuma cortar I/O drasticamente e habilita pushdown/vetorização.
4. **Column pruning**: selecione só as colunas necessárias; em formato colunar isso reduz leitura de verdade.
5. **Map join**: tabela pequena no join → confirme `hive.auto.convert.join=true` e que o `EXPLAIN` mostra Map Join (sem reduce shuffle).
6. **Skew**: poucas tasks muito mais lentas → `hive.optimize.skewjoin=true` ou trate a chave quente separadamente.
7. **Small files**: muitos arquivos minúsculos nas partições degradam tudo; compacte com `hive.merge.*` ou ajuste reducers.
8. **Vetorização + stats**: garanta `hive.vectorized.execution.enabled=true` (precisa de colunar) e rode `ANALYZE TABLE ... COMPUTE STATISTICS` para o CBO.
9. **ORDER BY global**: se não precisa de ordem total, troque por `DISTRIBUTE BY` + `SORT BY` para não estrangular num único reducer.

Meça por volume de dados lido (bytes), nº de mappers/reducers e tempo; valide equivalência com contagens/agregados.
