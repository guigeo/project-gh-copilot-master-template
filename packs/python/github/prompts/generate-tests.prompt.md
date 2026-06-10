---
mode: agent
description: Gera testes unitários pytest para código Python.
---

Crie testes para o código abaixo. Se estiver vazio, use o arquivo aberto (${file}).

${selection}

Regras:

- Use pytest.
- Não dependa de rede, banco real ou arquivos locais do usuário; use `tmp_path` e fixtures.
- Cubra sucesso, erro esperado, nulos e limites.
- Siga as convenções existentes em `tests/`.
- Explique rapidamente como rodar os testes.

Ao final, informe qualquer dependência ou ajuste necessário.
