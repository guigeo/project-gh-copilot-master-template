# Excel

## Objetivo

Guia para projetos com manipulação de planilhas Excel usando Python.

## Bibliotecas

`pandas` e `openpyxl` já estão declaradas no `pyproject.toml` deste projeto.

## Pipeline de referência

O módulo `src/<pacote>/excel_pipeline.py` demonstra o padrão esperado:

- `validate_excel_input` — valida existência do arquivo.
- `read_excel_sheet` — valida worksheet e colunas obrigatórias antes de retornar o DataFrame.
- `write_excel_safe` — escreve em arquivo temporário e renomeia, sem sobrescrever destino.

Os testes em `tests/test_excel_pipeline.py` cobrem roundtrip, aba inexistente,
coluna faltante e recusa de sobrescrita.

## Boas práticas

- Validar existência do arquivo e da worksheet antes de processar.
- Definir colunas obrigatórias e tipos esperados.
- Registrar tratamento de nulos e datas.
- Nunca sobrescrever o arquivo original.
