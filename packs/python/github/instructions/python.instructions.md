---
applyTo: "**/*.py,pyproject.toml,requirements*.txt"
description: Padrões de Python — layout src/, type hints, logging, ruff e pytest.
---

# Instruções para Python

## Ambiente

- Use o gerenciador que o projeto adotar (venv + pip, uv, poetry...). Não force um.
- Prefira projeto com layout `src/`.
- Evite depender de estado global.
- Não coloque caminho local fixo no código.
- Configure parâmetros via `.env`, variáveis de ambiente ou arquivo de configuração não sensível.

## Código

- Use type hints em funções públicas.
- Prefira funções pequenas e testáveis.
- Separe leitura, transformação, validação e escrita.
- Use `pathlib.Path` para caminhos.
- Use `logging` em vez de `print` em código de produção.
- Trate exceções com mensagens úteis, sem engolir erro silenciosamente.
- Evite notebooks como única fonte de lógica de produção; mova lógica reutilizável para módulos.

## Qualidade

- Use `ruff` para lint/format.
- Use `pytest` para testes.
- Ao criar função nova, crie ou sugira teste.
- Para scripts CLI, use `argparse` ou `typer` quando fizer sentido.

## Dados

- Declare schema esperado quando ler CSV/Parquet.
- Normalize encoding e separadores.
- Não carregue arquivos grandes sem chunking ou estratégia incremental.
