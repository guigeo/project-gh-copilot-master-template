---
name: pandas-performance
description: Use esta skill para acelerar e reduzir memória de código pandas — vetorização, dtypes (category/Arrow), leitura eficiente e quando migrar para Spark.
---

Ao otimizar código pandas, siga nesta ordem (do mais barato ao mais invasivo):

1. **Meça**: identifique o gargalo real (tempo e memória). Use `df.memory_usage(deep=True)` e cronometre o trecho; não otimize por suposição.
2. **Leitura**: leia só o necessário — `usecols`, `dtype`, `parse_dates` e `dtype_backend="pyarrow"`. Para arquivos grandes, `chunksize` ou Parquet em vez de CSV.
3. **Dtypes**: converta colunas de baixa cardinalidade para `category`; use dtypes anuláveis (`Int64`, `string`) e/ou backend Arrow. Isso costuma cortar memória pela metade ou mais.
4. **Vetorize**: substitua `iterrows`/`apply(axis=1)` por operações de coluna, acessadores `.str`/`.dt`, `np.where`/`np.select`. `apply` linha a linha é o gargalo nº 1.
5. **Não cresça em loop**: troque `concat`/`append` dentro de loop por acumular em lista e um `pd.concat` no final.
6. **groupby**: use `transform` quando precisar devolver na granularidade original; evite `apply` em groupby quando `agg`/`transform` vetorizado resolve.
7. **merge**: junte cedo e só as colunas necessárias; confirme `validate=` para não inflar linhas (linha a mais = trabalho a mais depois).
8. **Eval/query**: para expressões aritméticas grandes, `df.eval`/`df.query` podem reduzir cópias intermediárias.
9. **Cabe em memória?**: se o dataset não cabe (> ~1/3 da RAM) ou o job vive estourando, pare de espremer pandas e migre o pesado para Spark; use pandas só no resultado já reduzido.

Para cada mudança, registre o ganho (tempo, memória, linhas); não acumule otimizações sem medir.
