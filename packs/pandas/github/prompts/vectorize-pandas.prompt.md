---
mode: agent
description: Converte loop/apply linha a linha em pandas vetorizado, preservando o resultado.
---

Vetorize o código pandas abaixo (ou o arquivo aberto, se não houver seleção):

${selection}

Siga a skill pandas-performance e as instruções de pandas:

1. Identifique o ponto linha a linha (`iterrows`, `itertuples`, `apply(axis=1)`, loop com `concat`).
2. Reescreva com operações de coluna, `.str`/`.dt`, `np.where`/`np.select` ou `groupby.transform`, preservando exatamente o resultado.
3. Ajuste dtypes onde ajudar (anuláveis/`category`/Arrow) e evite cópias intermediárias.
4. Mantenha a função pura (`DataFrame -> DataFrame`, sem I/O).
5. Mostre como validar a equivalência com `pd.testing.assert_frame_equal` sobre um caso pequeno.

Não altere a granularidade nem o significado das colunas sem avisar explicitamente.
