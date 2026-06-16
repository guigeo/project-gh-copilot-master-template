---
name: deck-from-data
description: Use esta skill para gerar uma apresentação PowerPoint a partir de dados (DataFrame) — da agregação ao slide com gráficos e tabelas nativos.
---

Ao montar um deck orientado a dados, siga nesta ordem:

1. **Agregue antes (pandas)**: reduza os dados brutos ao que vai aparecer — um slide mostra resultado, não dado cru. Cada gráfico/tabela sai de um DataFrame pequeno e já validado.
2. **Planeje os slides**: defina a sequência (capa → sumário/KPIs → 1 ideia por slide → conclusão). Um gráfico por ideia; tabela só quando o número exato importa.
3. **Conteúdo como spec pura**: escreva funções puras `dados -> spec de slide` (título, bullets, dados do gráfico). Sem tocar no `.pptx` ainda — isso é testável isoladamente.
4. **Renderize com builder**: o builder abre o template, adiciona o slide pelo **layout** certo, preenche placeholders e insere gráfico/tabela **nativos** a partir do DataFrame.
5. **Gráfico nativo**: `CategoryChartData` (categorias + séries) e `add_chart(XL_CHART_TYPE..., ...)`. Escolha o tipo pela mensagem (barras p/ comparar, linha p/ tendência, pizza só p/ poucas fatias).
6. **Tabela nativa**: `add_table(linhas, colunas, ...)`; cabeçalho na linha 0; formate números antes (casas decimais, milhar) — a tabela mostra texto.
7. **Valide a estrutura**: leia de volta o modelo (nº de slides, `has_chart`/`has_table`, textos) e faça round-trip em `BytesIO`. Não dependa de abrir o PowerPoint.

Mantenha a lógica de conteúdo separada da renderização; a leitura dos dados e o `save` ficam nas bordas.
