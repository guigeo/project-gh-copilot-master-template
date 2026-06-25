---
applyTo: "**/*.py"
description: Padrões de apps Streamlit — modelo de execução (rerun), cache, session_state, layout e segredos.
---

# Instruções para Streamlit

Complementa o pack `python` com o que é específico de Streamlit.

## Modelo de execução

- Todo widget faz o script **reexecutar de cima a baixo** a cada interação. Não dependa de ordem de efeitos colaterais; escreva o script como função do estado atual.
- Mantenha a lógica de dados em funções puras (em módulos), separada da camada de UI. A UI só lê e exibe.
- Use `if __name__ == "__main__":` ou um `main()` chamado no fim; evite trabalho pesado no nível do módulo.

## Cache

- Use `@st.cache_data` para **dados serializáveis** (DataFrames, dicts, resultados de query). Retorne cópias; não mute o valor cacheado.
- Use `@st.cache_resource` para **recursos não serializáveis e compartilhados** (conexões de banco, clientes, modelos ML).
- Defina `ttl` quando os dados expiram; parametrize a função para a chave de cache refletir as entradas.

## Estado e fluxo

- Use `st.session_state` para estado entre reruns (filtros, autenticação, passo de wizard). Inicialize com `st.session_state.setdefault(...)`.
- Agrupe entradas que devem ser submetidas juntas em `st.form` + `st.form_submit_button` para evitar rerun a cada tecla.
- Para apps com várias telas, use a pasta `pages/` (multipágina nativo) em vez de um `if` gigante.

## Performance

- Não carregue arquivos grandes nem rode queries fora de função cacheada — roda a cada rerun.
- Use `st.spinner`/`st.status` em operações lentas e `st.fragment` para reexecutar só um trecho.

## Segurança

- Segredos vão em `st.secrets` (`.streamlit/secrets.toml`), **nunca** versionados nem hardcoded.
- Valide/sanitize entrada do usuário antes de usar em query ou caminho de arquivo.
