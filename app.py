import streamlit as st

# Configuração global da janela do navegador
st.set_page_config(page_title="Portal de Engenharia & Gestão de Ativos", layout="wide")

# Inicializa a variável global que controla a segurança do portal
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Mapeia os arquivos específicos criados na pasta pages
login_page = st.Page("pages/00_Login.py", title="Acesso ao Sistema", icon="🔒")
home_page = st.Page("pages/01_Home.py", title="Página Inicial", icon="🏠", default=True)
eng_page = st.Page("pages/01_Modulos_de_Engenharia.py", title="Módulos de Engenharia", icon="🏗️")
manut_page = st.Page("pages/02_Gestao_da_Manutencao.py", title="Gestão da Manutenção", icon="🛠️")
# NOVA PÁGINA ADICIONADA:
tempo_page = st.Page("pages/03_Indicadores_de_Tempo.py", title="Indicadores de Tempo", icon="⏱️")

# LÓGICA DE PROTEÇÃO DE ACESSO
if not st.session_state.logged_in:
    # Se NÃO estiver logado, oculta o menu lateral e força a exibição da tela de login
    pg = st.navigation([login_page], position="hidden")
else:
    # Se estiver logado com sucesso, monta o menu estruturado e libera os arquivos técnicos
    pg = st.navigation({
        "Menu Principal": [home_page],
        "Módulos Operacionais": [eng_page, manut_page, tempo_page]
    })

# Adiciona de forma limpa o botão de Logout no final do menu lateral
st.sidebar.markdown("---")
if st.sidebar.button("🔒 Desconectar Sessão", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.login_step = 1
    st.rerun()

# Executa a página ativa selecionada pelo usuário
pg.run()
