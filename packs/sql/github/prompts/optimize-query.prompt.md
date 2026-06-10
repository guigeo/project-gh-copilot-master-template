---
mode: agent
description: Analisa e otimiza uma query SQL preservando o resultado e a granularidade.
---

Otimize a query SQL selecionada (ou o arquivo aberto, se não houver seleção):

${selection}

Siga estes passos:

1. Identifique a granularidade e as chaves de join; aponte risco de multiplicação de linhas.
2. Verifique filtros de partição/data e se chegam cedo o suficiente.
3. Procure `SELECT *`, funções sobre colunas de filtro e CTEs reavaliadas.
4. Proponha a query otimizada, preservando exatamente o resultado.
5. Liste cada mudança com a consequência prática (custo, leitura, shuffle).
6. Sugira como validar a equivalência (contagens e agregados antes/depois).

Se a granularidade ou regra de negócio não estiver documentada, pergunte antes de alterar.
