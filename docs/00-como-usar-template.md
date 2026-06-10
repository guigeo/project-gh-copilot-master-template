# Como usar este template

## Estratégia recomendada

Use este repositório como base central e copie apenas o necessário para cada projeto.

Exemplos:

- Projeto Python simples: `common` + `python`.
- Projeto Python com contexto mínimo: `python-minimal`.
- Projeto Excel com Python: `excel`.
- Projeto SQL: `common` + `sql`.
- Projeto ArcPy: `common` + `python` + `arcgis-arcpy`.
- Projeto engenharia de dados: `common` + `python` + `sql`.

## Ordem de adoção

1. Comece pelo `common`.
2. Adicione uma tecnologia principal.
3. Rode o projeto.
4. Ajuste README e `.env.example`.
5. Depois adicione agents/skills específicos.

## Evite

- Copiar todas as skills para todo projeto.
- Colocar regra muito específica em `.github/copilot-instructions.md`.
- Misturar padrões de tecnologias que o projeto não usa.
