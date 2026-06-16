---
applyTo: "**/*.sql,**/*.pls,**/*.pkb,**/*.pks"
description: Padrões de Oracle — bind variables, FETCH FIRST/ROWNUM, particionamento, hints, índices, DBMS_STATS e PL/SQL em massa.
---

# Instruções para Oracle

Complementa o pack `sql` com o que é específico do Oracle.

## Bind variables

- Use **bind variables** (`:param`), não concatenação de literais — literais diferentes geram *hard parse* a cada execução e poluem a shared pool.
- Em aplicação, nunca monte SQL concatenando entrada do usuário (parse excessivo + risco de injeção).

## Limite de linhas e janelas

- Use `FETCH FIRST n ROWS ONLY` (12c+) para top-N; `ROWNUM` só com cuidado (é aplicado **antes** do `ORDER BY` — use subquery se precisar ordenar primeiro).
- Prefira funções analíticas (`ROW_NUMBER`, `RANK`, `SUM() OVER`) a subqueries correlacionadas.

## Índices e SARGability

- Não aplique função sobre coluna indexada no filtro, a menos que exista **function-based index** correspondente.
- Evite conversão implícita de tipo (comparar `VARCHAR2` com `NUMBER`, datas como string) — invalida o índice; use `TO_DATE`/`TO_NUMBER` explícito com formato.
- Trate `NULL` conscientemente (`NVL`/`COALESCE`); lembre que índice B-tree não indexa linhas todas-nulas.

## Particionamento

- Use particionamento (range/list/hash) em tabelas grandes e filtre pela chave de partição para *partition pruning*.
- Prefira **índice local** em tabela particionada quando o acesso é por partição; **global** quando o acesso cruza partições.

## Diagnóstico

- Leia o plano com `EXPLAIN PLAN` + `DBMS_XPLAN.DISPLAY` ou `DBMS_XPLAN.DISPLAY_CURSOR` (plano real); autotrace para I/O.
- Mantenha estatísticas atuais com `DBMS_STATS.GATHER_TABLE_STATS`; o CBO depende delas.
- Use **hints** (`/*+ ... */`) como último recurso, depois de corrigir stats e índices — não como primeira solução.

## PL/SQL

- Evite processamento linha a linha; use `BULK COLLECT` + `FORALL` para ler/gravar em massa e reduzir context switch SQL↔PL/SQL.
- Não fixe nomes de schema/instância nem credenciais; parametrize.
