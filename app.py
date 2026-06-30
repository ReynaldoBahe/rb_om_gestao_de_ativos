import streamlit as st

# 1. Configuração da página (Centralizada para o card flutuar perfeitamente)
st.set_page_config(page_title="RB Consultoria", page_icon="🏢", layout="centered")

# Estilização CSS de Alto Padrão - Cores corporativas, sombras reais e card destacado
st.markdown("""
    <style>
        .block-container { padding-top: 4rem !important; max-width: 480px !important; }
    
    /* Transforma o contêiner padrão em um Card Branco Flutuante com Sombra */
    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        padding: 35px 30px !important;
        border-radius: 16px !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Estilização dos textos internos do formulário */
    label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Inputs arredondados e limpos */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        padding: 12px !important;
        background-color: #f9fafb !important;
        color: #111827 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1e3a8a !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.15) !important;
    }
    
    /* Botão de Login Azul Safira com efeito de clique */
    div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 0px !important;
        font-size: 16px !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 10px rgba(30, 58, 138, 0.3) !important;
        transition: all 0.2s ease-in-out;
    }
    div.stFormSubmitButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 15px rgba(30, 58, 138, 0.4) !important;
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Inicializa as variáveis de controle de login globais
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cliente_ativo" not in st.session_state:
    st.session_state.cliente_ativo = ""

# 3. Definição das Páginas do Sistema utilizando st.Page
pagina_login = st.Page("app.py", title="Acesso ao Sistema", icon="🔒", default=True)
pagina_home = st.Page("pages/01_Home.py", title="Home", icon="🏠")
pagina_engenharia = st.Page("pages/01_Modulos_de_Engenharia.py", title="Módulos de Engenharia", icon="⚙️")
pagina_manutencao = st.Page("pages/02_Gestao_da_Manutencao.py", title="Gestão da Manutenção", icon="🛠️")
pagina_indicadores = st.Page("pages/03_Indicadores_de_Tempo.py", title="Indicadores de Tempo", icon="📊")
pagina_telemetria = st.Page("pages/04_Telemetria_em_Tempo_Real.py", title="Telemetria em Tempo Real", icon="⚡")

# Gerenciador de Navegação Dinâmica
if st.session_state.logged_in:
    paginas_disponiveis = [pagina_home, pagina_engenharia, pagina_manutencao, pagina_indicadores, pagina_telemetria]
else:
    paginas_disponiveis = [pagina_login]

pg = st.navigation(paginas_disponiveis)

# =========================================================================
# LÓGICA DE RENDERIZAÇÃO DAS TELAS
# =========================================================================
if not st.session_state.logged_in:
    
    # Formulário de Credenciais Premium
    with st.form("menu_login_premium"):
        
        # Cabeçalho integrado dentro do card branco
        st.markdown("""
            <div style='text-align: center; margin-bottom: 20px;'>
                <h1 style='color: #1e3a8a; font-size: 32px; font-weight: 800; margin-bottom: 2px; letter-spacing: 0.5px;'>RB CONSULTORIA</h1>
                <p style='color: #6b7280; font-size: 14px; font-weight: 500; margin-top: 0px;'>Gestão Estratégica de Ativos</p>
                <div style='height: 2px; background: linear-gradient(to right, transparent, #1e3a8a, transparent); margin-top: 15px;'></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Inputs de dados
        usuario = st.text_input("👤 Usuário Corporativo", placeholder="Ex: admin")
        senha = st.text_input("🔑 Senha de Acesso", type="password", placeholder="Digite sua senha")
        lembrar = st.checkbox("Manter conectado neste dispositivo")
        
        botao_entrar = st.form_submit_button("Entrar no Sistema", use_container_width=True)
        
    if botao_entrar:
        usuarios_validos = {
            "admin": "admin",
            "fiat": "fiat123",
            "ambev": "ambev123"
        }
        
        if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
            st.session_state.logged_in = True
            st.session_state.cliente_ativo = usuario.upper()
            st.rerun()
        else:
            st.error("❌ Credenciais inválidas. Tente novamente.")

else:
    # Se já estiver logado, executa a aplicação padrão
    pg.run()
    
    # Adiciona botão de Logout na barra lateral pós-login
    with st.sidebar:
        st.markdown("---")
        if st.button("Sair da Conta", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
