import streamlit as st
import time

# --- CONTROLE DE SESSÃO INTERNO ---
if "login_step" not in st.session_state:
    st.session_state.login_step = 1
if "usuario_validado" not in st.session_state:
    st.session_state.usuario_validado = ""

# --- BANCO DE DADOS DINÂMICO VIA CONFIG (SECRETS) ---
try:
    lista_usuarios = st.secrets["users"]
except KeyError:
    lista_usuarios = {
        "gerente.om@resortboaviagem.com": {"password": "SenhaResort123", "token": "852369", "cliente": "Resort Boa Viagem"}
    }

# --- INJEÇÃO DE CSS DE ALTO IMPACTO (FONTES AMPLIADAS E REDE ROBUSTA) ---
st.markdown("""
<style>
    .stApp { 
        background-color: #03111E !important; 
        color: #FFFFFF !important; 
    }
    
    .left-panel { padding: 20px; text-align: center; }
    
    .network-container {
        position: relative;
        width: 320px;
        height: 260px;
        margin: 0 auto 25px auto;
    }
    
    .node-center {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #092543 0%, #103B66 100%);
        border-radius: 50%;
        width: 110px; height: 110px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        font-weight: 800; color: #00D2FF; font-size: 22px;
        border: 2.5px solid #00D2FF;
        box-shadow: 0 0 25px rgba(0,210,255,0.5);
        z-index: 10;
    }
    .node-center span { font-size: 11px; font-weight: bold; color: #8AB4F8; margin-top: -1px; letter-spacing: 0.5px; }
    
    .node-sat {
        position: absolute;
        background-color: #06182B;
        border-radius: 50%;
        width: 65px; height: 65px;
        display: flex; justify-content: center; align-items: center;
        font-size: 15px; font-weight: 800; color: #FFFFFF;
        border: 2px solid #1A446F;
        box-shadow: 0 6px 15px rgba(0,0,0,0.5);
        z-index: 5;
        letter-spacing: 0.5px;
    }
    .node-top-left  { top: 5px; left: 5px; }
    .node-top-right { top: 5px; right: 5px; }
    .node-bot-left  { bottom: 5px; left: 5px; }
    .node-bot-right { bottom: 5px; right: 5px; }
    
    .pct-badge {
        position: absolute;
        top: 15px; right: -65px;
        color: #00D2FF; font-size: 22px; font-weight: 900;
        text-align: left; line-height: 1.1;
    }
    .pct-badge span { font-size: 12px; color: #8AB4F8; font-weight: bold; letter-spacing: 1px; }

    .network-lines {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 1;
    }
    
    .dt-title { font-size: 16px; letter-spacing: 3px; color: #8AB4F8; margin-bottom: 8px; font-weight: bold; }
    .main-brand { font-size: 54px; font-weight: 900; color: #FFFFFF; margin-bottom: 15px; line-height: 1; letter-spacing: 1px; }
    .sub-brand { font-size: 14px; letter-spacing: 3px; color: #00D2FF; font-weight: bold; margin-bottom: 25px; }
    .slogan { font-style: italic; color: #D1E2F4; font-size: 16px; margin-bottom: 35px; font-weight: 500; }
    
    .tags-footer {
        font-size: 13px !important;
        color: #6C8EB4 !important;
        letter-spacing: 1px !important;
        font-weight: 600 !important;
        margin-top: 20px;
    }
    
    .login-card { 
        background-color: #06182B !important; 
        padding: 35px !important; 
        border-radius: 16px !important; 
        border: 1px solid #103154 !important; 
        box-shadow: 0 12px 40px rgba(0,0,0,0.6) !important; 
    }
    
    .login-title { font-size: 28px; font-weight: bold; color: #FFFFFF; text-align: center; margin-bottom: 5px; }
    .login-subtitle { font-size: 14px; color: #8AB4F8; text-align: center; margin-bottom: 30px; }
    
    div[data-baseweb="input"], div[data-baseweb="input"] > div { 
        background-color: #0C233C !important; 
        border: 1px solid #1A446F !important; 
        border-radius: 12px !important; 
    }
    
    input[data-testid="stTextInputRootElement"], input { 
        background-color: transparent !important;
        color: #FFFFFF !important; 
        font-weight: 500 !important; 
    }
    input::placeholder { color: #5F82A8 !important; }
    label { color: #8AB4F8 !important; font-weight: 600 !important; font-size: 14px !important; }
    
    button[data-testid="baseButton-secondaryFormSubmit"], button[data-testid="baseButton-secondary"] {
        background-color: #104A7E !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid #1A62A3 !important;
        font-weight: bold !important;
        padding: 12px 0 !important;
    }
    
    div[data-testid="stNotification"] {
        background-color: #0C233C !important;
        border: 1px solid #1A446F !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
    }
    
    .top-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
    .resort-badge { background: #0A1E33; padding: 8px 16px; border-radius: 12px; font-weight: bold; font-size: 13px; border: 1px solid #143A63; color: #FFFFFF; }
    .verified-badge { background: rgba(0,210,255,0.08); color: #00D2FF; padding: 8px 16px; border-radius: 12px; font-size: 12px; border: 1px solid rgba(0,210,255,0.2); font-weight: 600; }
    .ssl-footer { color: #5F82A8; font-size: 12px; margin-top: 20px; display: flex; align-items: center; gap: 6px; justify-content: center; }
</style>
""", unsafe_allow_html=True)

# --- DIVISÃO DA INTERFACE EM 2 COLUNAS ---
col_esquerda, col_direita = st.columns([1.1, 1.0], gap="large")

with col_esquerda:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="network-container">
            <svg class="network-lines">
                <line x1="37" y1="37" x2="283" y2="223" style="stroke:#1A446F; stroke-width:2.5" />
                <line x1="283" y1="37" x2="37" y2="223" style="stroke:#1A446F; stroke-width:2.5" />
            </svg>
            <div class="node-sat node-top-left">BIM</div>
            <div class="node-sat node-top-right">IA</div>
            <div class="node-sat node-bot-left">IoT</div>
            <div class="node-sat node-bot-right">O&M</div>
            <div class="pct-badge">88%<br><span>SLA</span></div>
            <div class="node-center">DT<br><span>Facilities</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="dt-title">DT FACILITIES</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-brand">O&M</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-brand">GESTÃO INTELIGENTE DE ATIVOS</div>', unsafe_allow_html=True)
    st.markdown('<div class="slogan">"Seu patrimônio sob controle, onde você estiver."</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="tags-footer">Hospital &nbsp;•&nbsp; Resort &nbsp;•&nbsp; Supermercado &nbsp;•&nbsp; Facilities</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssl-footer" style="justify-content:flex-start; margin-top:50px;">🔒 Conexão segura SSL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_direita:
    nome_cliente = "Acesso Uniforme"
    if st.session_state.login_step == 2 and st.session_state.usuario_validado in lista_usuarios:
        nome_cliente = lista_usuarios[st.session_state.usuario_validado]["cliente"]

    st.markdown('<div class="top-header">', unsafe_allow_html=True)
    st.markdown(f'<div class="resort-badge">🏢 {nome_cliente}</div>', unsafe_allow_html=True)
    st.markdown('<div class="verified-badge">✓ Cliente verificado</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # --- ETAPA 1: LOGIN E SENHA ---
    if st.session_state.login_step == 1:
        st.markdown('<div class="login-title">Acesse sua conta</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Entre com seu e-mail e senha</div>', unsafe_allow_html=True)
        
        with st.form("form_etapa_1", clear_on_submit=False):
            email = st.text_input("E-mail", placeholder="seu.email@email.com")
            senha = st.text_input("Senha", type="password", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("🔵 Verificação em 2 etapas: Um código será enviado ao seu e-mail.")
            
            if st.form_submit_button("Entrar", use_container_width=True):
                if email in lista_usuarios and senha == lista_usuarios[email]["password"]:
                    st.session_state.usuario_validado = email
                    st.session_state.login_step = 2
                    st.rerun()
                else:
                    st.error("Credenciais inválidas para o ecossistema multi-cliente.")

    # --- ETAPA 2: TOKEN DE SEGURANÇA ---
    elif st.session_state.login_step == 2:
        st.markdown('<div class="login-title">Verificação</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Insira o código de segurança</div>', unsafe_allow_html=True)
        
        with st.form("form_etapa_2", clear_on_submit=False):
            codigo = st.text_input("Código de 6 dígitos", max_chars=6, placeholder="000000")
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.form_submit_button("Voltar", use_container_width=True):
                    st.session_state.login_step = 1
                    st.rerun()
            with col_b2:
                if st.form_submit_button("Confirmar", use_container_width=True):
                    user_info = lista_usuarios[st.session_state.usuario_validado]
                    if codigo == user_info["token"]:
                        st.success("Acesso autorizado!")
                        time.sleep(0.5)
