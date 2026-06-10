---
mode: agent
description: Diagnostica e otimiza um job PySpark lento ou caro.
---

Otimize o job PySpark abaixo. Se estiver vazio, use o arquivo aberto (${file}).

${selection}

Sintoma relatado: ${input:sintoma:ex. job demora 2h, shuffle gigante, muitos arquivos pequenos}

Siga a skill spark-optimization:

1. Identifique no código os pontos caros (shuffles, joins, UDFs, ações sobre dados grandes).
2. Proponha as otimizações em ordem de impacto, explicando o porquê de cada uma.
3. Mostre o código alterado mantendo o comportamento.
4. Indique como validar: comparação de `explain()`, métricas a observar e teste com a fixture `spark`.

Não aplique otimização que mude o resultado sem avisar explicitamente.
