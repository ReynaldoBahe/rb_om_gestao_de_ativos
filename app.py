import streamlit as st

# 1. Configuração da página em modo AMPLO (Wide)
st.set_page_config(page_title="RB Consultoria", page_icon="🏢", layout="wide")

# Estilização CSS Avançada para Centralização e Alinhamento Perfeito
st.markdown("""
    <style>
    /* Ajustes globais de espaçamento */
    .block-container { padding-top: 5rem !important; padding-bottom: 2rem !important; max-width: 1200px !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    
    /* Container Flex para igualar as alturas das colunas */
    [data-testid="stHorizontalBlock"] {
        display: flex;
        align-items: stretch;
    }
    
    /* Banner da Esquerda Premium */
    .banner-esquerda {
        background: linear-gradient(135deg, #0e1e38 0%, #1a365d 100%);
        color: #ffffff;
        padding: 45px;
        border-radius: 16px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }
    
    /* Card de Login Integrado (Ajustado) */
    .card-login-container {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        height: 100%;
    }
    
    /* Customização do Botão de Login Nativo para cor Azul Corporativo */
    div.stFormSubmitButton > button {
        background-color: #1a365d !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 0px !important;
        transition: all 0.3s ease;
    }
    div.stFormSubmitButton > button:hover {
        background-color: #2b5284 !important;
        box-shadow: 0 4px 12px rgba(26, 54, 93, 0.2);
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
    
    # Divisão balanceada lado a lado (Proporção equilibrada 50/50)
    col_logo, col_login = st.columns([1, 1], gap="large")
    
    # -----------------------------------------------------------------
    # COLUNA DA ESQUERDA: Banner Corporativo Premium
    # -----------------------------------------------------------------
    with col_logo:
        st.markdown("""
            <div class="banner-esquerda">
                <h1 style='font-size: 38px; font-weight: 800; margin-bottom: 10px; color: #fff; letter-spacing: 1px;'>RB CONSULTORIA</h1>
                <h3 style='color: #63b3ed; font-weight: 400; margin-bottom: 25px; font-size: 22px;'>Gestão Estratégica de Ativos</h3>
                <p style='font-size: 15px; line-height: 1.6; color: #e2e8f0; margin-bottom: 40px;'>
                    Bem-vindo ao portal integrado de Engenharia e O&M. 
                    Acesse para monitorar métricas operacionais, telemetria em tempo real 
                    e diagnósticos prescritivos por Inteligência Preditiva.
                </p>
                <small style='color: #a0aec0; margin-top: auto;'>© 2026 RB Consultoria Engenharia.</small>
            </div>
        """, unsafe_allow_html=True)
        
    # -----------------------------------------------------------------
    # COLUNA DA DIREITA: Formulário Totalmente Integrado dentro do Card
    # -----------------------------------------------------------------
    with col_login:
        # Abrimos a estrutura do card branco com HTML estilizado
        st.markdown("""
            <div class="card-login-container">
                <h2 style='text-align: center; color: #1a202c; font-weight: 700; margin-bottom: 5px; font-size: 28px;'>Acesso ao Sistema</h2>
                <p style='text-align: center; color: #718096; margin-bottom: 25px; font-size: 15px;'>Insira suas credenciais corporativas.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # O formulário agora é renderizado logo após, mantendo os inputs integrados ao visual
        with st.form("menu_login_unico"):
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            lembrar = st.checkbox("Lembrar de mim")
            botao_entrar = st.form_submit_button("Entrar no Portal", use_container_width=True)
            
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
                st.error("❌ Usuário ou senha incorretos.")

else:
    # Se já estiver logado, renderiza a página ativa do menu lateral
    pg.run()
    
    # Inclui o botão de Logout na barra lateral logada de forma fixa
    with st.sidebar:
        st.markdown("---")
        if st.button("Sair da Conta", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
