# PowerPoint (data-driven)

Scaffold de geração de `.pptx` orientada a dados com python-pptx. Combina com
o pack `pandas`: pipeline dados → deck.

## Estrutura

- `src/nome_pacote/content.py` — funções puras `dados -> spec de slide` (sem python-pptx, sem I/O); testáveis isoladamente.
- `src/nome_pacote/deck.py` — builder: abre template, adiciona slides por **layout** e preenche placeholders.
- `src/nome_pacote/charts.py` — gráficos e tabelas **nativos** (editáveis) a partir de DataFrame.
- `tests/test_deck.py` — valida lendo o modelo (nº de slides, `has_chart`/`has_table`, textos) + round-trip em `BytesIO`.
- `templates/` — coloque aqui o `.pptx` de marca.

## Fluxo

1. Leia e **agregue** os dados com pandas (use os módulos do pack pandas).
2. Transforme em specs com funções puras de `content`.
3. Renderize com `deck` + `charts` sobre o template.
4. `deck.salvar(prs, "saida/relatorio.pptx")` na borda.

## Convenções

- Template + placeholders, nunca posicionamento absoluto.
- Gráfico/tabela **nativos**, não PNG colado.
- Unidades com `Inches`/`Pt`; nada de pixels crus.
- Conteúdo separado de renderização; I/O só nas bordas.

## Requisitos

- `uv sync` instala pandas, pyarrow, pandera e python-pptx.
- Testes rodam sem abrir o PowerPoint: `uv run pytest`.
