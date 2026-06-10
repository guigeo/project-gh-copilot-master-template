---
name: sql-query-review
description: Use esta skill ao revisar SQL, principalmente joins, performance, granularidade, filtros e qualidade de dados.
---

Checklist de revisão SQL:

1. Identifique a granularidade da query.
2. Liste tabelas de entrada e chaves de join.
3. Verifique se algum join pode multiplicar linhas.
4. Confirme filtros de partição/data.
5. Verifique tratamento de nulos.
6. Procure `SELECT *` e substitua por colunas explícitas.
7. Avalie CTEs muito grandes ou repetidas.
8. Sugira testes de contagem antes/depois.
9. Documente regra de negócio em comentário quando não for óbvia.
