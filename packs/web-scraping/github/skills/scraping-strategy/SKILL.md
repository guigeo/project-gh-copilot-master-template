---
name: scraping-strategy
description: Use esta skill para escolher COMO extrair dados de um site antes de escrever código — da fonte mais barata e estável (API) à mais cara e frágil (navegador headless).
---

Antes de raspar HTML, suba a escada de extração e pare no primeiro degrau que resolver (do mais estável/barato ao mais frágil/caro):

1. **Dados oficiais**: existe download, dataset, RSS/Atom ou `sitemap.xml`? Use isso e pare aqui.
2. **API pública/interna**: abra as DevTools → aba Network e veja se a página carrega dados de um endpoint JSON. Chamar o JSON direto é mais estável que parsear HTML e costuma trazer paginação limpa.
3. **HTML estático**: se o dado já vem no HTML inicial (veja "View Source", não o DOM renderizado), use `httpx` + `BeautifulSoup`. Caminho padrão.
4. **HTML renderizado por JS**: só se o dado **não** existe no HTML inicial e não há API. Use Playwright headless; espere por seletor específico, não por `sleep` fixo.

Para qualquer degrau, antes de codar:

- **Mapeie a paginação**: parâmetro de página/offset, cursor, scroll infinito (geralmente é uma API por baixo) ou "próxima página" via link. Defina o critério de parada.
- **Cheque robots.txt e ToS** do domínio para os caminhos que vai acessar.
- **Estime o volume** (nº de páginas × intervalo de rate limit) e confirme que é razoável; raspe um lote pequeno primeiro.
- **Escolha seletores estáveis**: prefira `id`, `data-*` e atributos semânticos a XPaths longos dependentes de posição.

Regra de ouro: quanto mais alto na escada você resolve, menos o scraper quebra quando o site muda o layout.
