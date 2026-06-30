import streamlit as st

# 1. Configuração da página (Deve ser mantida como centered para o card flutuar)
# Mude de "centered" para "wide" no seu arquivo raiz
st.set_page_config(page_title="RB Consultoria", page_icon="🏢", layout="wide")


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
    
    # 🔐 INJEÇÃO ISOLADA: O componente de fundo só existe dentro do bloco 'if deslogado'
    st.components.v1.html("""
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -9999;
            background-image: linear-gradient(rgba(10, 20, 40, 0.75), rgba(10, 20, 40, 0.85)), 
                              url('https://unsplash.com');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        "></div>
    """, height=0, width=0)

    # 🔐 CSS ISOLADO: Estilos de transparência aplicados estritamente na tela de login
    st.markdown("""
        <style>
        .stApp, div[data-testid="stAppViewContainer"], div[data-testid="stAppViewBlockContainer"], .main, .stMainBlockContainer {
            background-color: transparent !important;
            background: transparent !important;
        }
        [data-testid="stHeader"] { background: transparent !important; }
        .block-container { padding-top: 4rem !important; max-width: 480px !important; }
        
        /* Formatação do Card Branco */
        div[data-testid="stForm"] {
            background-color: #ffffff !important;
            padding: 35px 30px !important;
            border-radius: 16px !important;
            border: 1px solid #e5e7eb !important;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.3) !important;
        }
        label { color: #374151 !important; font-weight: 600 !important; font-size: 14px !important; }
        .stTextInput > div > div > input {
            border-radius: 8px !important;
            border: 1px solid #d1d5db !important;
            padding: 12px !important;
            background-color: #f9fafb !important;
            color: #111827 !important;
        }
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
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Formulário de Credenciais Premium
    with st.form("menu_login_premium"):
        st.markdown("""
            <div style='text-align: center; margin-bottom: 20px;'>
                <h1 style='color: #1e3a8a; font-size: 32px; font-weight: 800; margin-bottom: 2px; letter-spacing: 0.5px;'>RB CONSULTORIA</h1>
                <p style='color: #6b7280; font-size: 14px; font-weight: 500; margin-top: 0px;'>Gestão Estratégica de Ativos</p>
                <div style='height: 2px; background: linear-gradient(to right, transparent, #1e3a8a, transparent); margin-top: 15px;'></div>
            </div>
        """, unsafe_allow_html=True)
        
        usuario = st.text_input("👤 Usuário Corporativo", placeholder="Ex: admin")
        senha = st.text_input("🔑 Senha de Acesso", type="password", placeholder="Digite sua senha")
        lembrar = st.checkbox("Manter conectado neste dispositivo")
        botao_entrar = st.form_submit_button("Entrar no Sistema", use_container_width=True)
        
    if botao_entrar:
        usuarios_validos = {"admin": "admin", "fiat": "fiat123", "ambev": "ambev123"}
        if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
            st.session_state.logged_in = True
            st.session_state.cliente_ativo = usuario.upper()
            st.rerun()
        else:
            st.error("❌ Credenciais inválidas. Tente novamente.")

else:
    # 🔓 ÁREA LOGADA: Roda a navegação padrão sem NENHUM CSS intrusivo ativo
    pg.run()
    
    # Adiciona botão de Logout limpo na barra lateral pós-login
    with st.sidebar:
        st.markdown("---")
        if st.button("Sair da Conta", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
