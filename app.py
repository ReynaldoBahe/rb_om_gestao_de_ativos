import streamlit as st

# =========================================================================
# 1. INICIALIZAÇÃO DE VARIÁVEIS DO SISTEMA
# =========================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "cliente_ativo" not in st.session_state:
    st.session_state["cliente_ativo"] = "Resort Boa Viagem"

# =========================================================================
# 2. DECLARAÇÃO DE TODAS AS PÁGINAS DO PORTAL
# =========================================================================
login_page = st.Page("pages/00_Login.py", title="Acesso ao Sistema", icon="🔐")
home_page = st.Page("pages/01_Home.py", title="Página Inicial", icon="🏠")
eng_page = st.Page("pages/01_Modulos_de_Engenharia.py", title="Módulos de Engenharia", icon="🏗️")
manut_page = st.Page("pages/02_Gestao_da_Manutencao.py", title="Gestão da Manutenção", icon="🛠️")
tempo_page = st.Page("pages/03_Indicadores_de_Tempo.py", title="Indicadores de Tempo", icon="⏱️")
telemetria_page = st.Page("pages/04_Telemetria_em_Tempo_Real.py", title="Telemetria em Tempo Real", icon="📊")

# =========================================================================
# 3. LÓGICA DE PROTEÇÃO DE ACESSO
# =========================================================================
if not st.session_state.logged_in:
    # Se NÃO estiver logado, oculta o menu lateral e força a exibição da tela de login
    pg = st.navigation([login_page], position="hidden")
else:
    # Se estiver logado com sucesso, monta o menu estruturado e libera os arquivos técnicos
    pg = st.navigation({
        "Menu Principal": [home_page],
                "Módulos Operacionais": [eng_page, manut_page, tempo_page, telemetria_page]
    })


# Executa o sistema de rotas do Streamlit
pg.run()

# =========================================================================
# 4. BOTÃO DE LOGOUT UNIFICADO
# =========================================================================
if st.session_state.logged_in:
    st.sidebar.markdown("---")
    if st.sidebar.button("🔒 Desconectar Sessão", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state["cliente_ativo"] = "Resort Boa Viagem"
        st.rerun()
