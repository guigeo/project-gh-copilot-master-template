---
mode: agent
description: Cria uma página Streamlit a partir de um objetivo, separando dados (cacheados) de UI.
---

Crie uma página Streamlit para: ${input:objetivo:o que a página deve mostrar/fazer}.

Antes de implementar, apresente um plano curto: dados necessários, onde cacheá-los
(`cache_data` vs `cache_resource`), estado de sessão e layout.

Ao implementar:

- Ponha a lógica de dados em função(ões) pura(s) com o cache adequado; a UI só consome.
- Inicialize `st.session_state` com `setdefault`; agrupe entradas relacionadas em `st.form`.
- Use segredos via `st.secrets`, nunca hardcoded.
- Dê feedback de carregamento (`st.spinner`/`st.status`) e trate erros com `st.error`.
