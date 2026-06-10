---
mode: agent
description: Analisa erro e propõe correção objetiva.
---

Analise o erro abaixo:

${input:erro:Cole a mensagem de erro ou o trecho relevante do stack trace}

Contexto adicional:

${input:contexto:O que estava sendo executado quando o erro ocorreu}

Se necessário, localize no repositório o código apontado pelo erro antes de concluir.

Responda com:

1. Causa mais provável
2. Como confirmar
3. Correção recomendada
4. Alternativas
5. Como testar
6. Como evitar recorrência
