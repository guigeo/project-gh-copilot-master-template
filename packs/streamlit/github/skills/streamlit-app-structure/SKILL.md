---
name: streamlit-app-structure
description: Use esta skill ao criar ou reorganizar um app Streamlit — separar dados de UI, escolher o cache certo, estado de sessão, multipágina e formulários.
---

Ao construir um app Streamlit, siga nesta ordem:

1. **Separe camadas.** Lógica de dados (carga, transformação, validação) em módulos puros e testáveis sob `src/`; o arquivo do app só monta a UI e chama essas funções. Isso mantém o app testável sem subir o servidor.

2. **Escolha o cache certo** para cada função de dados:
   - `@st.cache_data` → retorna valor serializável (DataFrame, dict, JSON). Retorne cópia; defina `ttl` se expira.
   - `@st.cache_resource` → retorna recurso compartilhado e vivo (conexão, client, modelo). Uma instância para toda a sessão.

3. **Modele o estado.** O que precisa sobreviver ao rerun (filtros, login, passo atual) vai em `st.session_state`, inicializado com `setdefault`. O resto é derivado a cada execução.

4. **Controle reruns.** Entradas relacionadas dentro de `st.form` submetem juntas. Para recomputar só um trecho, use `@st.fragment`. Evite trabalho pesado fora de função cacheada.

5. **Estruture a navegação.** Mais de uma tela → pasta `pages/` (multipágina) ou `st.navigation`. Uma tela → layout com `st.columns`, `st.tabs`, `st.sidebar`.

6. **Feche com segurança e UX.** Segredos em `st.secrets`; feedback com `st.spinner`/`st.status`/`st.toast`; trate erros com `st.error` em vez de deixar o traceback cru aparecer.
