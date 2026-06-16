---
applyTo: "**/*.py"
description: Padrões de geração de PowerPoint (python-pptx) — template/placeholders, gráficos/tabelas nativos, EMU, builders puros e testáveis.
---

# Instruções para PowerPoint (python-pptx)

Complementa os packs `python` e `pandas` com a geração de `.pptx`.

## Template e layouts (não posicione no olho)

- Parta de um **template `.pptx`** de marca e adicione slides por **layout** (`prs.slide_layouts[i]`); não monte tudo com caixas de texto em coordenadas absolutas.
- Preencha **placeholders** existentes (`slide.placeholders[idx]`, `slide.shapes.title`) em vez de criar shapes soltos; o `idx` do placeholder é estável, a posição na tela não.
- Deixe cores e fontes virem do **tema/master** do template; não fixe a paleta no código.

## Conteúdo nativo, não imagem

- Gere **gráficos nativos** (`add_chart` + `CategoryChartData`) e **tabelas nativas** (`add_table`) — ficam editáveis no PowerPoint. Não cole PNG de matplotlib quando o nativo resolve.
- Alimente gráfico/tabela a partir de um DataFrame **já agregado** (use pandas para reduzir antes); um slide não é lugar de processar dados brutos.
- Um gráfico por ideia; evite tabelas gigantes — resuma ou pagine.

## Unidades e medidas

- Use os helpers de unidade (`Inches`, `Pt`, `Emu`) — internamente é tudo EMU; nunca passe pixels ou números crus para posição/tamanho.
- Defina tamanho de fonte com `Pt(...)`; cuidado com autofit de texto em caixas com muito conteúdo.

## Arquitetura (puro vs efeito)

- Separe **conteúdo** de **renderização**: funções puras transformam dados em uma *spec* de slide (título, bullets, dados do gráfico); o builder aplica a spec na apresentação.
- Leitura de dados e `prs.save(...)` ficam nas bordas; a lógica que decide o slide não faz I/O.
- Receba o caminho do template e do arquivo de saída por parâmetro/config; não fixe caminhos locais.

## Testabilidade

- Teste lendo de volta o modelo de objetos (sem abrir o PowerPoint): conte `len(prs.slides)`, confira `shapes.title.text`, `has_chart`/`has_table` e textos de placeholder.
- Valide a apresentação em memória com `BytesIO` (round-trip `save`), sem depender de arquivo no disco.
- Não fixe segredos nem caminhos locais; o template de marca vai em `templates/`.
