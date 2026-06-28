import streamlit as st
import time

if "login_step" not in st.session_state:
    st.session_state.login_step = 1
if "usuario_validado" not in st.session_state:
    st.session_state.usuario_validado = ""

try:
    lista_usuarios = st.secrets["users"]
except KeyError:
    lista_usuarios = {
        "gerente.om@resortboaviagem.com": {"password": "SenhaResort123", "token": "852369", "cliente": "Resort Boa Viagem"}
    }

css_code = """
header[data-testid="stHeader"] { visibility: hidden !important; height: 0px !important; }
div[data-testid="collapsedControl"] { display: none !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #03111E !important; color: #FFFFFF !important; }
.left-panel { padding: 30px 5px 15px 5px; text-align: center; }
.network-container { position: relative; width: 330px; height: 250px; margin: 20px auto 20px auto; }
.node-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: linear-gradient(135deg, #092543 0%, #103B66 100%); border-radius: 50%; width: 115px; height: 115px; display: flex; flex-direction: column; justify-content: center; align-items: center; font-weight: 900; color: #00D2FF; font-size: 20px; border: 2.5px solid #00D2FF; box-shadow: 0 0 25px rgba(0,210,255,0.5); z-index: 10; }
.node-center span { font-size: 11px; font-weight: 800; color: #8AB4F8; margin-top: 0px; letter-spacing: 0.5px; }
.node-sat { position: absolute; background-color: #06182B; border-radius: 50%; width: 68px; height: 68px; display: flex; justify-content: center; align-items: center; font-size: 15px; font-weight: 900; color: #FFFFFF; border: 2px solid #1A446F; box-shadow: 0 6px 15px rgba(0,0,0,0.5); z-index: 5; }
.node-top-left { top: 5px; left: 5px; }
.node-top-right { top: 5px; right: 5px; }
.node-bot-left { bottom: 5px; left: 5px; }
.node-bot-right { bottom: 5px; right: 5px; }
.pct-badge { position: absolute; top: 15px; right: -65px; color: #00D2FF; font-size: 22px; font-weight: 900; text-align: left; line-height: 1.1; }
.pct-badge span { font-size: 12px; color: #8AB4F8; font-weight: bold; }
.network-lines { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
.dt-title { font-size: 16px; letter-spacing: 3px; color: #8AB4F8; margin-bottom: 8px; font-weight: bold; }
.main-brand { font-size: 52px; font-weight: 950; color: #FFFFFF; margin-bottom: 10px; line-height: 1; }
.sub-brand { font-size: 14px; letter-spacing: 3px; color: #00D2FF; font-weight: bold; margin-bottom: 20px; }
.slogan { font-style: italic; color: #D1E2F4; font-size: 16px; margin-bottom: 30px; font-weight: 500; }
.tags-footer { font-size: 14px !important; color: #8AB4F8 !important; letter-spacing: 1px !important; font-weight: 700 !important; margin-top: 20px; }
.right-wrapper { max-width: 420px; margin: 0 auto; padding-top: 30px; }
.login-card { background-color: #06182B !important; padding: 35px 30px !important; border-radius: 16px !important; border: 1px solid #103154 !important; box-shadow: 0 12px 40px rgba(0,0,0,0.6) !important; }

/* Configuração dos campos de entrada */
div[data-baseweb="input"], div[data-baseweb="input"] > div { background-color: #0C233C !important; border: 1px solid #1A446F !important; border-radius: 12px !important; height: 52px !important; }
input { background-color: transparent !important; color: #FFFFFF !important; font-weight: 600 !important; font-size: 17px !important; }
input::placeholder { color: #5F82A8 !important; font-size: 15px !important; }
label { color: #8AB4F8 !important; font-weight: 700 !important; font-size: 15px !important; margin-bottom: 6px !important; display: block !important; }
div[data-testid="stForm"] { border: none !important; padding: 0 !important; }

/* 🛠️ APAGÃO DA TARJA: Esconde o bloco esticado azul e deixa apenas o ícone do olho visível */
div[data-testid="stTextInputAdornment"], 
div[data-testid="stTextInputAdornment"] > div { 
    visibility: hidden !important;
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
}

/* Força apenas o botão do olho a reaparecer flutuando de forma transparente */
div[data-testid="stTextInputAdornment"] button { 
    visibility: visible !important;
    background-color: transparent !important; 
    background: transparent !important; 
    border: none !important; 
    box-shadow: none !important; 
    color: #8AB4F8 !important; 
}
div[data-testid="stTextInputAdornment"] button:hover { color: #00D2FF !important; }

/* Botões do formulário */
div[data-testid="stForm"] button, .stButton button { background-color: #104A7E !important; color: #FFFFFF !important; border-radius: 12px !important; border: 1px solid #1A62A3 !important; font-weight: 800 !important; font-size: 17px !important; height: 52px !important; width: 100% !important; margin-top: 15px !important; box-shadow: 0 4px 15px rgba(16,74,126,0.4) !important; }
div[data-testid="stForm"] button:hover { background-color: #165CA1 !important; }
div[data-testid="stNotification"] { background-color: #0C233C !important; border: 1px solid #1A446F !important; color: #FFFFFF !important; border-radius: 12px !important; }
.top-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.resort-badge { background: #0A1E33; padding: 8px 16px; border-radius: 12px; font-weight: bold; font-size: 13px; border: 1px solid #143A63; color: #FFFFFF; }
.verified-badge { background: rgba(0,210,255,0.08); color: #00D2FF; padding: 8px 16px; border-radius: 12px; font-size: 12px; border: 1px solid rgba(0,210,255,0.2); font-weight: 600; }
.ssl-footer { color: #5F82A8; font-size: 12px; margin-top: 20px; display: flex; align-items: center; gap: 6px; justify-content: center; }
"""

st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

col_esquerda, col_direita = st.columns([1.1, 1.0], gap="large")

with col_esquerda:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)
    html_net = '<div class="network-container"><svg class="network-lines"><line x1="40" y1="40" x2="290" y2="210" style="stroke:#1A446F; stroke-width:3" /><line x1="290" y1="40" x2="40" y2="210" style="stroke:#1A446F; stroke-width:3" /></svg><div class="node-sat node-top-left">BIM</div><div class="node-sat node-top-right">IA</div><div class="node-sat node-bot-left">IoT</div><div class="node-sat node-bot-right">O&M</div><div class="pct-badge">88%<br><span>SLA</span></div><div class="node-center">DT<br><span>Facilities</span></div></div>'
    st.markdown(html_net, unsafe_allow_html=True)
    st.markdown('<div class="dt-title">DT FACILITIES</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-brand">O&M</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-brand">GESTÃO INTELIGENTE DE ATIVOS</div>', unsafe_allow_html=True)
    st.markdown('<div class="slogan">"Seu patrimônio sob controle, onde você estiver."</div>', unsafe_allow_html=True)
    st.markdown('<div class="tags-footer">Hospital &nbsp;•&nbsp; Resort &nbsp;•&nbsp; Supermercado &nbsp;•&nbsp; Facilities</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssl-footer" style="justify-content:flex-start; margin-top:40px;">🔒 Conexão segura SSL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_direita:
    st.markdown('<div class="right-wrapper">', unsafe_allow_html=True)
    nome_cliente = "Acesso Uniforme"
    if st.session_state.logged_in == False and st.session_state.usuario_validado in lista_usuarios:
        nome_cliente = lista_usuarios[st.session_state.usuario_validado]["cliente"]
    st.markdown('<div class="top-header">', unsafe_allow_html=True)
    st.markdown(f'<div class="resort-badge">🏢 {nome_cliente}</div>', unsafe_allow_html=True)
    st.markdown('<div class="verified-badge">✓ Cliente verificado</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
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
                        st.success("Acesso authorized!")
