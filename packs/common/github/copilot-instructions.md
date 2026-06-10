# Instruções gerais do repositório para GitHub Copilot

## Papel esperado

Atue como assistente técnico deste repositório. As regras específicas de cada tecnologia estão em `.github/instructions/`; fluxos especializados estão em `.github/skills/`.

## Regras gerais

- Responda e gere código em português brasileiro, exceto nomes de variáveis, APIs e padrões técnicos que devam ficar em inglês.
- Antes de propor código, identifique o objetivo, entradas, saídas e restrições.
- Prefira soluções simples, testáveis e fáceis de manter.
- Não crie abstrações complexas sem necessidade clara.
- Não altere comportamento público sem explicar o impacto.
- Não remova validações, logs, tratamento de erro ou testes sem justificativa.
- Não use credenciais, tokens, senhas ou caminhos pessoais hardcoded.
- Use variáveis de ambiente para segredos e caminhos dependentes do ambiente.
- Prefira pequenos commits/PRs com escopo claro.
- Sempre que criar ou alterar código, considere testes e documentação.

## Segurança

- Verifique risco de SQL injection, command injection, path traversal, vazamento de segredo e logs com dados sensíveis.
- Nunca recomende salvar credenciais em arquivos versionados.
- Em scripts de automação, prefira falhar com erro claro a seguir silenciosamente com estado inconsistente.

## Performance e dados

- Para dados grandes, evite carregar tudo em memória.
- Prefira processamento incremental, particionamento, streaming/chunks ou pushdown quando aplicável.
- Não use `collect()` em Spark sem justificar.
- Para SQL, evite `SELECT *` em produção.
- Para arquivos, registre encoding, separador, schema e tratamento de nulos.

## Entrega

Ao finalizar uma tarefa, informe:

1. O que foi alterado.
2. Como validar.
3. Riscos ou pontos pendentes.
