import streamlit as st

# Configuração básica de navegação
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Páginas do sistema corporativo
home_page = st.Page("pages/01_Home.py", title="Home", icon="🏠", default=True)
engenharia_page = st.Page("pages/01_Modulos_de_Engenharia.py", title="Módulos de Engenharia", icon="⚙️")
manutencao_page = st.Page("pages/02_Gestao_da_Manutencao.py", title="Gestão da Manutenção", icon="📊")
indicadores_page = st.Page("pages/03_Indicadores_de_Tempo.py", title="Indicadores de Tempo", icon="⏱️")
telemetria_page = st.Page("pages/04_Telemetria_em_Tempo_Real.py", title="Telemetria em Tempo Real", icon="🌐")
tour_page = st.Page("pages/05_Tour_Virtual.py", title="Tour Virtual", icon="🕶️")
portal_page = st.Page("pages/06_Portal_CMMS.py", title="Portal CMMS", icon="🖥️")

# Gerenciamento de roteamento
if st.session_state.logged_in:
    pg = st.navigation({
        "Menu Principal": [home_page],
        "Módulos Operacionais": [engenharia_page, manutencao_page, indicadores_page, telemetria_page, tour_page, portal_page]
    })
    pg.run()
    
    with st.sidebar:
        st.markdown("---")
        if st.button("Sair da conta", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
else:
    # Se não estiver logado, força a renderização da página de login (Home)
    pg = st.navigation([home_page])
    pg.run()
