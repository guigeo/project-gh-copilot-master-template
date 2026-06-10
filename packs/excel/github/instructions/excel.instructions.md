---
applyTo: "**/*excel*.py,**/excel/**/*.py,**/*openpyxl*.py,**/*xlsx*.py,**/*xlsm*.py,**/*planilha*.py"
description: Padrões para ler, validar e escrever planilhas Excel com pandas/openpyxl.
---

# Instruções para projetos Excel

## Bibliotecas e formato

- Prefira `pandas` com engine explícita quando possível.
- Para escrita com formatação/células, prefira `openpyxl`.
- Preserve encoding, locale e formato de datas de forma explícita.
- Não assuma nome de planilha padrão; valide existência da worksheet.

## Leitura e validação

- Valide se o arquivo existe antes de abrir.
- Declare colunas obrigatórias e valide schema mínimo.
- Trate células vazias, tipos mistos e valores inválidos com mensagens claras.
- Evite carregar planilhas muito grandes sem estratégia de chunking ou filtro.

## Escrita e segurança

- Não sobrescreva arquivo final sem `backup` ou escrita em arquivo temporário.
- Não logue conteúdo sensível de células.
- Evite fórmulas dinâmicas sem validação de entrada para reduzir risco de injeção.

## Boas práticas

- Separe leitura, transformação e escrita em funções pequenas.
- Use `pathlib.Path` para caminhos.
- Cubra com testes pelo menos: leitura válida, aba inexistente e coluna faltante.
