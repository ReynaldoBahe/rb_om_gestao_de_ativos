import streamlit as st

# 1. Configuração da página (Deve ser a primeira linha)
st.set_page_config(page_title="RB Consultoria", page_icon="🏢", layout="centered")

# 2. Inicializa as variáveis de controle de login globais
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cliente_ativo" not in st.session_state:
    st.session_state.cliente_ativo = ""

# 3. Definição das Páginas do Sistema utilizando st.Page
# O primeiro parâmetro é o caminho real do arquivo dentro da pasta 'pages/'
pagina_login = st.Page("app.py", title="Acesso ao Sistema", icon="🔒", default=True)
pagina_home = st.Page("pages/01_Home.py", title="Home", icon="🏠")
pagina_engenharia = st.Page("pages/01_Modulos_de_Engenharia.py", title="Módulos de Engenharia", icon="⚙️")
pagina_manutencao = st.Page("pages/02_Gestao_da_Manutencao.py", title="Gestão da Manutenção", icon="🛠️")
pagina_indicadores = st.Page("pages/03_Indicadores_de_Tempo.py", title="Indicadores de Tempo", icon="📊")
pagina_telemetria = st.Page("pages/04_Telemetria_em_Tempo_Real.py", title="Telemetria em Tempo Real", icon="⚡")

# =========================================================================
# 🧭 GERENCIADOR DE NAVEGAÇÃO DINÂMICA
# =========================================================================
if st.session_state.logged_in:
    # Se o usuário ESTIVER LOGADO, ele enxerga o menu completo
    paginas_disponiveis = [pagina_home, pagina_engenharia, pagina_manutencao, pagina_indicadores, pagina_telemetria]
else:
    # Se o usuário NÃO ESTIVER LOGADO, a barra lateral mostra apenas a tela de Login
    paginas_disponiveis = [pagina_login]

# Inicializa a navegação oficial controlada pelo script
pg = st.navigation(paginas_disponiveis)


# =========================================================================
# LÓGICA DE RENDERIZAÇÃO DAS TELAS
# =========================================================================
if not st.session_state.logged_in:
    
    # Criamos duas colunas de tamanhos iguais (1 para logo, 1 para formulário)
    col_logo, col_login = st.columns(2, gap="large")
    
    # -----------------------------------------------------------------
    # COLUNA DA ESQUERDA: Logomarca e Boas-Vindas
    # -----------------------------------------------------------------
    with col_logo:
        st.markdown("<br><br>", unsafe_allow_html=True) # Espaçamento para alinhar verticalmente
        # Substitua a URL abaixo pelo link real da imagem da sua logomarca
        st.image("https://placeholder.com", use_container_width=True)
        st.markdown("""
            <div style='text-align: center; margin-top: 20px;'>
                <h3>Gestão Estratégica de Ativos</h3>
                <p style='color: gray;'>Painel integrado de Engenharia, Manutenção e Telemetria Operacional.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # -----------------------------------------------------------------
    # COLUNA DA DIREITA: Formulário de Acesso
    # -----------------------------------------------------------------
    with col_login:
        st.markdown("<h2 style='text-align: center;'>Acesso ao Sistema</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Insira suas credenciais para acessar.</p>", unsafe_allow_html=True)
        
        # Formulário estruturado e seguro em caixa
        with st.form("formulario_login"):
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            lembrar = st.checkbox("Lembrar de mim")
            
            # Botão de submissão do formulário
            botao_entrar = st.form_submit_button("Entrar", use_container_width=True)
