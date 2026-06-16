---
mode: agent
description: Gera uma apresentação PowerPoint orientada a dados a partir de um DataFrame/descrição, com gráficos e tabelas nativos.
---

Quero um deck a partir destes dados: ${input:dados:descreva o DataFrame/fonte e a mensagem do deck}

Use o código/seleção como base, se houver:

${selection}

Siga a skill deck-from-data e a pptx-templating:

1. **Agregue (pandas)**: reduza os dados ao que vai aparecer; valide o DataFrame resultante.
2. **Planeje** a sequência de slides (capa → KPIs → uma ideia por slide → conclusão) e diga o layout de cada um.
3. **Conteúdo puro**: escreva funções `dados -> spec de slide`, testáveis isoladamente.
4. **Renderize** com o builder: abra o template, adicione por layout, preencha placeholders e insira gráficos/tabelas **nativos** (não imagens) a partir do DataFrame.
5. **Teste**: valide a estrutura lendo o modelo (nº de slides, `has_chart`/`has_table`, textos) e faça round-trip em `BytesIO`.

Não posicione shapes no olho nem cole PNG quando o nativo resolve; se o template não tiver o placeholder esperado, reporte o mapa de layouts em vez de improvisar.
