# Subagents no Copilot

Subagents não são arquivos que você cria diretamente neste template.

Eles são execuções delegadas pelo agente principal para isolar uma parte do trabalho, preservar contexto e permitir especialização.

## Como influenciar o uso de subagents

Você influencia subagents por meio de:

- Custom agents em `.github/agents/*.agent.md`.
- Skills bem descritas em `.github/skills/*/SKILL.md`.
- Prompts claros pedindo pesquisa, plano, revisão ou execução separada.
- Escopo pequeno e objetivo.

## Exemplos de uso

- Usar `sql-reviewer` para revisar queries.
- Usar `python-reviewer` para revisar módulo Python.
- Usar `python-reviewer` para revisar leitura, validação e escrita de planilhas no profile `excel`.
- Usar `arcgis-arcpy-specialist` para validar scripts ArcPy.
- Usar `docs-writer` para atualizar README e troubleshooting.

## Exemplo prático no profile Excel

Em projetos com perfil `excel`, um fluxo eficiente é:

1. Pedir revisão do módulo de ingestão com `python-reviewer`.
2. Pedir atualização de documentação de schema/abas com `docs-writer`.
3. Rodar revisão final de consistência entre código e README.

Esse fluxo reduz retrabalho e evita carregar contexto desnecessário em uma única execução longa.
