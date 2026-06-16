---
mode: agent
description: Escreve uma função de parsing pura (HTML -> registros tipados) a partir de um trecho de HTML, com teste.
---

Extraia dados estruturados do HTML abaixo. Se estiver vazio, use o arquivo aberto (${file}).

${selection}

Campos desejados: ${input:campos:ex. titulo, preco, url, data}

Implemente seguindo as instruções de web scraping:

1. Modele o registro como `dataclass` com os campos pedidos (tipos explícitos; opcionais quando o dado pode faltar).
2. Escreva uma função pura `parse_*(html: str) -> list[Registro]`, sem rede nem I/O, com seletores estáveis.
3. Trate elemento ausente como caso normal (pule ou `None`), normalize valores (trim, número, data ISO-8601).
4. Gere um teste com este HTML como fixture fixo, cobrindo um caso completo e um com campo faltando.

Não adicione requisição de rede dentro da função de parsing.
