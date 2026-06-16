---
mode: agent
description: Reduz o uso de memória de um pipeline pandas via dtypes, leitura eficiente e Arrow.
---

Reduza o uso de memória do código pandas abaixo (ou o arquivo aberto, se não houver seleção):

${selection}

Tamanho/sintoma: ${input:contexto:ex. CSV de 5 GB, processo estoura RAM, leitura lenta}

Siga a skill pandas-performance:

1. Otimize a leitura: `usecols`, `dtype`, `parse_dates`, `dtype_backend="pyarrow"`; Parquet ou `chunksize` se fizer sentido.
2. Converta colunas para `category` (baixa cardinalidade) e dtypes anuláveis/Arrow; mostre o ganho com `memory_usage(deep=True)`.
3. Elimine cópias intermediárias desnecessárias e materializações grandes.
4. Avalie honestamente se o dado ainda cabe em pandas; se não, recomende lotes ou migração para Spark e explique o critério.
5. Liste cada mudança com o ganho estimado de memória e como medir antes/depois.

Não troque dtypes de forma que altere valores (ex.: downcast que perde precisão) sem avisar.
