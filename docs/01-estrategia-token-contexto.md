# Estratégia para consumir menos tokens

## O erro comum

Colocar todas as regras em um único arquivo grande sempre carregado. Isso piora o foco do
agente e paga token em **todo** prompt.

## O que de fato custa token

Só a camada **always-on** entra no contexto a cada prompt:

- `.github/copilot-instructions.md`
- `AGENTS.md`

Todo o resto é **sob-demanda**:

| Camada | Quando carrega |
|---|---|
| `instructions/*.instructions.md` | Quando o arquivo editado casa com o `applyTo` |
| `prompts/*.prompt.md` | Quando o prompt é chamado manualmente |
| `skills/*/SKILL.md` | Quando a skill é acionada |
| `agents/*.agent.md` | Quando o agente é selecionado |

Por isso a métrica que importa é o **orçamento da camada always-on**, não o tamanho total
do projeto. O `new_project.py --dry-run` e o `validate.py` medem e orçam exatamente isso.

## Boas práticas

- Mantenha `copilot-instructions.md` + `AGENTS.md` curtos (orçamento padrão: 1500 tokens).
- Toda instrução de tecnologia deve ter `applyTo` específico (ex.: `**/*.sas`), para não
  pagar regra de SQL em arquivo Python.
- Detalhe procedimental pesado vai para **skills**, não para instruções.
- Não repita a mesma regra em várias camadas: cada repetição é paga quando a camada carrega.
- Não cole documentação externa inteira; resuma e linke em `docs/03-referencias.md`.
- Peça plano antes de implementar tarefas grandes.

## Bootstrap enxuto

Escolha o profile aderente ao caso de uso e reduza categorias opcionais:

```bash
python scripts/new_project.py --profile data-engineering --target . \
  --without-agents --without-skills --without-prompts --without-ci --dry-run
```

Use `--dry-run` antes de gravar para revisar o plano e o orçamento de tokens.
Ver também [05-arquitetura.md](05-arquitetura.md).
