---
name: pptx-templating
description: Use esta skill para trabalhar com templates .pptx no python-pptx — layouts, placeholders por idx, tema/marca e consistência visual sem posicionar no olho.
---

Para gerar slides consistentes com a marca usando um template `.pptx`:

1. **Carregue o template**: `Presentation("templates/marca.pptx")`. Os layouts e o tema (cores/fontes) vêm dele; novos slides herdam isso automaticamente.
2. **Inspecione os layouts**: percorra `prs.slide_layouts` e, em cada um, os `layout.placeholders` para descobrir o `idx`, o tipo (`placeholder_format.type`) e o nome. Documente o mapa (ex.: layout 1 = Título e Conteúdo; idx 0 = título, idx 1 = corpo).
3. **Adicione por layout**: `slide = prs.slides.add_slide(prs.slide_layouts[i])`; escolha o layout pela função do slide, não improvise.
4. **Preencha placeholders, não crie shapes**: use `slide.shapes.title.text` e `slide.placeholders[idx]`. Criar caixa de texto em coordenada absoluta quebra a consistência e a edição posterior.
5. **Texto rico**: acesse `placeholder.text_frame`, manipule `paragraphs`/`runs`; `clear()` antes de repovoar; defina nível de bullet com `paragraph.level`.
6. **Cores e fontes**: prefira herdar do tema. Se precisar de cor explícita, use a paleta do tema (`MSO_THEME_COLOR`) em vez de RGB fixo espalhado pelo código.
7. **Imagens e logos**: respeite a proporção (defina só largura **ou** só altura); o logo de marca normalmente já está no master — não recarregue em cada slide.

Se o template não tiver o placeholder esperado, pare e reporte o mapa real dos layouts em vez de cair para posicionamento absoluto.
