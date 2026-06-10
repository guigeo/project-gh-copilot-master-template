---
name: sas-to-python
description: Use esta skill para migrar lógica SAS (DATA step e PROC SQL) para Python com pandas/polars, preservando regras de negócio.
---

Ao migrar SAS para Python:

1. Leia o programa SAS e identifique entradas (`libname`/datasets), transformações e saídas.
2. Mapeie cada step:
   - `DATA step` com filtros/derivações → operações em pandas/polars.
   - `PROC SQL` → SQL equivalente ou API do DataFrame.
   - `BY` + `RETAIN` → `groupby` + acumuladores.
   - `MERGE` → `join`/`merge` com chave explícita.
   - Formatos/`FORMAT` → conversão e formatação no Python.
3. Trate valores ausentes de forma equivalente (`.`/`''` SAS → `NaN`/`None`).
4. Preserve a ordem das operações quando ela afeta o resultado.
5. Escreva testes comparando uma amostra do resultado SAS com o Python.
6. Documente diferenças intencionais de comportamento (ex.: arredondamento).
7. Não traga datasets inteiros para memória sem necessidade; use chunking quando grande.
