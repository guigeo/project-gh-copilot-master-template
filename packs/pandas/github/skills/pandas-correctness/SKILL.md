---
name: pandas-correctness
description: Use esta skill para encontrar bugs sutis de pandas — chained indexing, NaN, merge que multiplica linhas, dtypes traiçoeiros e alinhamento por índice.
---

Ao revisar ou depurar correção em pandas, verifique nesta ordem:

1. **Atribuição segura**: há chained indexing (`df[...][...] = ...`)? Troque por `.loc[linhas, colunas] = ...`. Com Copy-on-Write, atribuição via view silenciosamente não persiste — reatribua o resultado.
2. **merge / cardinalidade**: todo `merge` deveria declarar `validate=` ("1:1"/"m:1"/"1:m"). Rode com `indicator=True` e cheque `_merge` para chaves órfãs e multiplicação de linhas. Compare `len()` antes/depois.
3. **NaN**: lembre `NaN != NaN`; comparações com `NA` retornam `NA`, não `False`. Use `.isna()`/`.fillna()` explícito. `groupby` descarta grupos `NaN` por padrão — use `dropna=False` se forem relevantes.
4. **Dtypes traiçoeiros**: coluna `int` que virou `float` (NaN presente) → use `Int64` anulável. Coluna `object` escondendo tipos mistos → normalize o dtype. Datas como `string` quebram comparação/ordenação.
5. **Alinhamento por índice**: operações entre Series/DataFrame alinham pelo índice, não pela posição; resultado com `NaN` inesperado costuma ser índice desalinhado. `reset_index(drop=True)` quando o índice não é chave.
6. **Ordenação/dedupe**: `drop_duplicates`/`sort_values` dependem de `keep=` e estabilidade; para "última linha por chave", ordene explicitamente antes.
7. **Cópia vs view**: não dependa de mutar um slice; em CoW isso não afeta o original. Trabalhe com funções puras que retornam novo DataFrame.
8. **Equivalência**: ao alterar lógica, valide com `pd.testing.assert_frame_equal` sobre um caso pequeno e com contagens/somatórios antes e depois.

Para cada achado, explique a consequência prática (linhas a mais, valor errado, NA silencioso) e como reproduzir.
