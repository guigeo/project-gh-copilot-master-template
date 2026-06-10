---
name: spark-optimization
description: Use esta skill para diagnosticar e otimizar jobs PySpark lentos ou caros — plano de execução, shuffle, joins, skew, particionamento e caching.
---

Ao otimizar um job PySpark, siga nesta ordem (do mais barato ao mais invasivo):

1. **Plano**: rode `df.explain("formatted")` e identifique scans completos, shuffles (`Exchange`) e tipos de join; otimize o que o plano mostra, não o que você supõe.
2. **Poda**: aplique filtros e `select` de colunas o mais cedo possível; em fontes particionadas, confirme que o filtro atinge a coluna de partição (partition pruning).
3. **Shuffle**: reduza o número de `Exchange`; agregue antes de join quando possível; confirme `spark.sql.adaptive.enabled=true` (AQE).
4. **Joins**: tabela pequena (< ~100 MB) → `broadcast()`; verifique no plano se virou `BroadcastHashJoin` em vez de `SortMergeJoin`.
5. **Skew**: se poucas tasks demoram muito mais que as demais, há skew; use o skew join do AQE ou aplique salting na chave.
6. **UDFs**: substitua UDF Python por funções nativas de `pyspark.sql.functions`; se impossível, converta para `pandas_udf`.
7. **Caching**: faça `cache()` somente de DataFrames reutilizados 2+ vezes; verifique na Spark UI se coube em memória; `unpersist()` ao final.
8. **Escrita**: ajuste `repartition()`/`coalesce()` para arquivos de ~128 MB–1 GB; evite milhares de arquivos pequenos.

Para cada mudança, meça antes e depois (tempo, bytes de shuffle, arquivos gerados) e registre o ganho; não acumule otimizações sem medição.
