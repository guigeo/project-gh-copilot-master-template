---
applyTo: "**/*.sql"
description: Padrões de T-SQL (SQL Server) — TOP/OFFSET-FETCH, predicados SARGable, índices, planos, isolamento e parameter sniffing.
---

# Instruções para SQL Server (T-SQL)

Complementa o pack `sql` com o que é específico do SQL Server.

## Predicados SARGable

- Não aplique função sobre a coluna indexada no `WHERE` (`WHERE YEAR(data) = 2026` impede seek); use intervalo: `data >= '2026-01-01' AND data < '2027-01-01'`.
- Evite conversão implícita de tipo (comparar `nvarchar` com `int`, datas como string) — vira scan e ignora índice.

## Paginação e janelas

- Pagine com `OFFSET ... FETCH NEXT ... ROWS ONLY` (precisa de `ORDER BY`), não com truques de `TOP` aninhado.
- Use funções de janela (`ROW_NUMBER`, `SUM() OVER`) em vez de subqueries correlacionadas.

## Índices e planos

- Prefira índice **clustered** na chave de acesso por intervalo; **nonclustered** com `INCLUDE` para cobrir a query e evitar key lookup.
- Leia o plano (Actual, não só Estimated): procure *Key Lookup*, *Sort* caro, *Scan* onde deveria haver *Seek* e divergência grande entre linhas estimadas e reais (estatística velha).
- Trate sugestão de *missing index* como pista, não ordem — avalie antes de criar.

## Funções e CTEs

- Evite **UDF escalar** no `SELECT`/`WHERE` (execução linha a linha antes do SQL 2019); prefira função inline TVF ou expressão.
- CTE no SQL Server **não** é materializada — se referenciada várias vezes, é reavaliada; considere tabela temporária para reuso pesado.

## Concorrência e temporários

- Não use `WITH (NOLOCK)` como atalho de performance — lê dados sujos; prefira `READ COMMITTED SNAPSHOT` (RCSI).
- `#temp` tem estatística (melhor para volume grande); variável de tabela (`@t`) não — use com cuidado em volumes altos.
- **Parameter sniffing**: se o plano varia muito por parâmetro, use `OPTION (RECOMPILE)` ou `OPTIMIZE FOR`.

## Cuidados

- Use `TRY_CAST`/`TRY_CONVERT` para conversão segura; `STRING_AGG` para concatenar; `IIF` para condicional curto.
- Não fixe nomes de instância/banco nem credenciais no código.
