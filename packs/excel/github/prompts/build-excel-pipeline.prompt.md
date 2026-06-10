---
mode: agent
description: Cria um pipeline de processamento de planilha Excel com leitura validada e escrita segura.
---

Crie um pipeline de Excel para a seguinte necessidade:

${input:descricao:Descreva a planilha de entrada (abas, colunas) e a saída esperada}

Siga estes passos:

1. Liste entradas (arquivo, abas, colunas obrigatórias, tipos) e a saída esperada.
2. Proponha a estrutura (funções de leitura, validação, transformação e escrita) antes de codificar.
3. Implemente usando pandas com engine `openpyxl`, type hints e logging.
4. Valide existência de arquivo/worksheet e colunas obrigatórias com erros claros.
5. Escreva a saída de forma segura, sem sobrescrever a entrada.
6. Gere testes cobrindo: roundtrip, aba inexistente, coluna faltante e recusa de sobrescrita.

Use a skill `excel-pipeline` como referência e siga o padrão de `excel_pipeline.py` se existir.
