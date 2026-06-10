---
applyTo: "**/*.sas"
description: Padrões de SAS — DATA steps, PROC SQL, macros, performance e migração para Python.
---

# Instruções para SAS

## Estilo

- Use nomes de bibliotecas (`libname`) e datasets descritivos e em minúsculas.
- Indente blocos `DATA` e `PROC` de forma consistente.
- Comente o objetivo de cada step, não o óbvio de cada linha.
- Prefira `PROC SQL` para joins e agregações complexas; `DATA step` para lógica linha a linha.

## Boas práticas

- Sempre declare `libname` no início e use caminhos via macro variável, nunca path local fixo.
- Use `OPTIONS` de forma explícita no topo do programa (ex.: `mprint`, `nodate`).
- Evite `SELECT *` em `PROC SQL`; liste colunas necessárias.
- Trate valores ausentes (`.`, `''`) explicitamente antes de cálculos.
- Use `%MACRO`/`%MEND` para lógica reutilizável; evite copiar steps.
- Limpe datasets temporários com `PROC DATASETS` ao final de jobs longos.

## Dados e performance

- Filtre cedo com `WHERE` antes de joins para reduzir volume.
- Para tabelas grandes, prefira pushdown no banco via `PROC SQL` pass-through em vez de trazer tudo para `WORK`.
- Declare e documente o schema esperado (colunas, tipos, formatos) na entrada.

## Segurança

- Nunca coloque senha, token ou string de conexão direto no `.sas`.
- Use arquivos de autenticação externos ou variáveis de ambiente.

## Migração

- Ao migrar lógica para Python, mapeie `DATA step` para pandas/polars e `PROC SQL` para SQL equivalente; ver a skill `sas-to-python`.
