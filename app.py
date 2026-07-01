import streamlit as st

# 1. Configuração da Página Inicial
st.set_page_config(
    page_title="RB Gestão de Ativos",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicialização do estado de login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 3. Estrutura de Autenticação e Roteamento
if not st.session_state["logged_in"]:
    st.title("🔑 Portal de Acesso - Gestão de Ativos")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        usuario = st.text_input("Usuário:")
        senha = st.text_input("Senha:", type="password")
        botao_entrar = st.button("Acessar System", use_container_width=True)
        
        if botao_entrar:
            usuarios_validos = {
                "admin": "RB_eng_admin_2026!",
                "fiat": "Fiat_Ativos_RB99*",
                "ambev": "Ambev_OM_RB2026#"
            }
            
            if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
                st.session_state["logged_in"] = True
                st.session_state["cliente_ativo"] = usuario.upper()
                st.rerun()
            else:
                st.error("❌ Credenciais inválidas. Tente novamente.")
else:
    # 4. ÁREA INTERNA: Menu de Navegação Clássico para carregar os módulos
    st.sidebar.title("Navegação")
    st.sidebar.markdown(f"👤 Conectado como: **{st.session_state['cliente_ativo']}**")
    st.sidebar.markdown("---")
    
    # Lista com o nome amigável dos módulos para exibição
    paginas = {
        "🏠 Home": "pages/01_Home.py",
        "⚙️ Módulos de Engenharia": "pages/01_Modulos_de_Engenharia.py",
        "📊 Gestão da Manutenção": "pages/02_Gestao_da_Manutencao.py",
        "⏱️ Indicadores de Tempo": "pages/03_Indicadores_de_Tempo.py",
        "🌐 Telemetria em Tempo Real": "pages/04_Telemetria_em_Tempo_Real.py",
        "🕶️ Tour Virtual": "pages/05_Tour_Virtual.py",
        "🖥️ Portal CMMS": "pages/06_Portal_CMMS.py"
    }
    
    # Cria o seletor de páginas na barra lateral
    pagina_selecionada = st.sidebar.radio("Selecione o Módulo:", list(paginas.keys()))
    
    # Botão de Logout posicionado abaixo do seletor
    st.sidebar.markdown("---")
    if st.sidebar.button("Sair da conta", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()

    # Executa o código da página escolhida na área central automaticamente
    caminho_arquivo = paginas[pagina_selecionada]
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            exec(f.read(), globals())
    except Exception as e:
        st.error(f"Erro ao carregar o módulo {pagina_selecionada}: {e}")
