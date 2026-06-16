# Templates

Coloque aqui o `.pptx` de marca (ex.: `marca.pptx`) e passe o caminho para
`nova_apresentacao("templates/marca.pptx")`.

Os novos slides herdam **layouts, cores e fontes** do template. Para descobrir
o mapa de placeholders do seu template, percorra `prs.slide_layouts` e, em cada
layout, os `layout.placeholders` (veja `idx`, `placeholder_format.type` e nome)
— e ajuste os índices de layout em `deck.py` ao seu arquivo.

Sem template, `nova_apresentacao()` usa o template padrão do python-pptx
(layouts 0 = capa, 1 = título e conteúdo, 5 = só título).
