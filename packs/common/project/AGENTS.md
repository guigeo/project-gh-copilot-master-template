# AGENTS.md

Orientações para agentes de codificação que trabalham neste repositório.

## Antes de alterar código

- Leia `README.md`, `.github/copilot-instructions.md` e as instruções em `.github/instructions/` que se aplicam aos arquivos da tarefa.
- Para fluxos especializados (setup, revisão, migração), use as skills em `.github/skills/`.
- Busque por termos e trechos relevantes antes de abrir muitos arquivos; não carregue arquivos grandes inteiros sem necessidade.

## Regras gerais

- Prefira alterações pequenas, revisáveis e com testes.
- Não faça mudanças amplas sem explicar o plano antes.
- Não invente dependências, caminhos, tabelas, credenciais ou ambientes.
- Nunca exponha segredos, tokens, senhas, chaves ou dados sensíveis.
- Quando houver dúvida entre simplicidade e arquitetura complexa, prefira simplicidade.

## Setup e validação

Se o projeto usa Python, o gerenciador é `uv`:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Checklist antes de concluir

- Código formatado e lint sem erros.
- Testes para comportamento novo, ou justificativa da ausência.
- README/documentação atualizados quando uso ou configuração mudar.
- Nenhum segredo ou caminho local fixo introduzido.
