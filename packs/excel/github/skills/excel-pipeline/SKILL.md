---
name: excel-pipeline
description: Use esta skill para criar ou revisar pipelines de planilhas Excel (xlsx/xlsm, pandas, openpyxl) — leitura validada, transformação e escrita segura.
---

Ao construir um pipeline de Excel:

1. Valide existência do arquivo e da worksheet antes de ler (`pd.ExcelFile` + `sheet_names`).
2. Declare colunas obrigatórias e tipos esperados; falhe com mensagem clara se faltarem.
3. Use engine explícita (`openpyxl` para xlsx/xlsm).
4. Trate células vazias, tipos mistos e datas: documente formato e timezone esperados.
5. Para planilhas grandes, leia apenas as colunas necessárias (`usecols`) ou filtre cedo.
6. Separe leitura, transformação, validação e escrita em funções pequenas e testáveis.
7. Escreva em arquivo temporário e renomeie; nunca sobrescreva a entrada original.
8. Não logue conteúdo de células que possa ser sensível.
9. Cubra com testes: leitura válida (roundtrip), aba inexistente, coluna faltante e recusa de sobrescrita.

Use `src/<pacote>/excel_pipeline.py` como referência de estrutura.
