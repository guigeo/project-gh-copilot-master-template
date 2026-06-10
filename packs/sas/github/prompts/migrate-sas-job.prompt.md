---
mode: agent
description: Migra um job SAS para Python preservando as regras de negócio e gerando testes de equivalência.
---

Migre o programa SAS selecionado para Python.

Siga estes passos:

1. Liste entradas, transformações e saídas do programa SAS.
2. Proponha a estrutura Python (módulos, funções) antes de gerar código.
3. Implemente a migração usando pandas ou polars, com type hints e logging.
4. Mapeie explicitamente cada `DATA step`/`PROC SQL` para o trecho Python correspondente.
5. Gere testes que comparem uma amostra do resultado original com o Python.
6. Liste diferenças de comportamento intencionais e riscos.

Não invente colunas, tabelas ou caminhos. Use a skill `sas-to-python` como referência de mapeamento.
