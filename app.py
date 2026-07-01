import streamlit as st

# 1. Configuração inicial do ecossistema
st.set_page_config(page_title="Portal RB Engenharia", page_icon="🏗️", layout="wide")

# Inicializa o estado de login caso não exista
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 2. LISTA DECLARATIVA: Força a exibição de todas as 6 páginas no menu
paginas_do_portal = [
    st.Page("pages/01_Home.py", title="Home", icon="🏠"),
    st.Page("pages/01_Modulos_de_Engenharia.py", title="Módulos de Engenharia", icon="⚙️"),
    st.Page("pages/02_Gestao_da_Manutencao.py", title="Gestão da Manutenção", icon="🔧"),
    st.Page("pages/03_Indicadores_de_Tempo.py", title="Indicadores de Tempo", icon="📊"),
    st.Page("pages/04_Telemetria_em_Tempo_Real.py", title="Telemetria em Tempo Real", icon="⚡"),
    st.Page("pages/05_Tour_Virtual.py", title="Tour Virtual", icon="📸"),
    st.Page("pages/06_Portal_CMMS.py", title="Portal CMMS", icon="🛠️")
]

# 3. Controle de Acesso Seguro
if not st.session_state.logged_in:
    st.title("🏗️ Acesso ao Portal - RB Engenharia")
    
    usuario = st.text_input("Usuário:")
    senha = st.text_input("Senha:", type="password")
    
    if st.button("Entrar no Sistema", use_container_width=True):
        # Altere para a lógica de validação original da sua empresa se necessário
        if usuario == "ADMIN" and senha == "1234": 
            st.session_state.logged_in = True
            st.session_state.cliente_ativo = "ADMIN"
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
else:
    # Gerenciador nativo que corrige o cache e exibe as páginas na barra lateral
    navegacao = st.navigation(paginas_do_portal)
    navegacao.run()
