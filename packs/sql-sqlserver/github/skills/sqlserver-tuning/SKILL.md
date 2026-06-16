---
name: sqlserver-tuning
description: Use esta skill para diagnosticar e otimizar T-SQL lento — planos de execução, índices, predicados SARGable, parameter sniffing e estatísticas.
---

Ao otimizar uma query no SQL Server, siga nesta ordem:

1. **Plano real**: capture o *Actual Execution Plan* (não só o estimado). Compare linhas estimadas × reais; divergência grande = estatística desatualizada (`UPDATE STATISTICS` / `sp_updatestats`).
2. **SARGability**: remova funções e conversões implícitas sobre colunas filtradas/indexadas; reescreva para intervalos. Isto sozinho costuma transformar Scan em Seek.
3. **Key Lookup**: se o plano mostra Key Lookup repetido, adicione as colunas faltantes via `INCLUDE` num índice nonclustered (índice de cobertura).
4. **Operadores caros**: ache o operador de maior custo (Sort, Hash Match, Scan). Sort caro às vezes some com índice na ordem certa; Hash Match em join grande pode indicar falta de índice na chave.
5. **Parameter sniffing**: plano ótimo para um valor e péssimo para outro → teste `OPTION (RECOMPILE)`, `OPTIMIZE FOR` ou variável local.
6. **UDF escalar**: substitua UDF escalar em `WHERE`/`SELECT` por inline TVF ou expressão; em versões antigas ela serializa a execução.
7. **CTE reusada**: CTE referenciada N vezes é reavaliada N vezes; materialize em `#temp` quando o reuso for pesado.
8. **Concorrência**: se a dor é bloqueio (não CPU), avalie RCSI em vez de `NOLOCK`; cheque `sys.dm_exec_requests`/waits.

Valide a equivalência com contagens/agregados antes e depois; meça por leituras lógicas (`SET STATISTICS IO ON`) e tempo.
