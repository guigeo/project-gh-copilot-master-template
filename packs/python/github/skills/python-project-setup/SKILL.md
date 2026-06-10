---
name: python-project-setup
description: Use esta skill para criar ou revisar a estrutura inicial de um projeto Python com uv, pytest, ruff e layout src.
---

Ao configurar projeto Python:

1. Use `pyproject.toml` como fonte principal de configuração.
2. Use layout `src/<package_name>/`.
3. Crie `tests/`.
4. Configure `pytest`, `ruff` e, se fizer sentido, `mypy`.
5. Adicione comandos no README:
   - `uv sync`
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run ruff format .`
6. Crie `.env.example`, nunca `.env` com valores reais.
7. Inclua logging básico.
8. Não adicione dependências sem justificar.
