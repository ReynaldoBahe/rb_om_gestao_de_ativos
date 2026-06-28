import streamlit as st
import time

if "login_step" not in st.session_state:
    st.session_state.login_step = 1
if "usuario_validado" not in st.session_state:
    st.session_state.usuario_validado = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cliente_ativo" not in st.session_state:
    st.session_state.cliente_ativo = ""
if "mostrar_senha" not in st.session_state:
    st.session_state.mostrar_senha = False

try:
    lista_usuarios = st.secrets["users"]
except KeyError:
    lista_usuarios = {
        "gerente.om@resortboaviagem.com": {
            "password": "SenhaResort123",
            "token": "852369",
            "cliente": "Resort Boa Viagem"
        }
    }

css_code = """
header[data-testid="stHeader"] { visibility: hidden !important; height: 0px !important; }
div[data-testid="collapsedControl"] { display: none !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #03111E !important; color: #FFFFFF !important; }

.left-panel {
    padding: 20px 10px 15px 10px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 95vh;
}
.network-container {
    position: relative; width: 300px; height: 230px; margin: 0 auto 16px auto;
}
.node-center {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    background: linear-gradient(135deg, #092543 0%, #103B66 100%);
    border-radius: 50%; width: 105px; height: 105px;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    font-weight: 900; color: #00D2FF; font-size: 20px;
    border: 2.5px solid #00D2FF;
    box-shadow: 0 0 25px rgba(0,210,255,0.5); z-index: 10;
}
.node-center span { font-size: 11px; font-weight: 800; color: #8AB4F8; margin-top: 2px; letter-spacing: 0.5px; }
.node-sat {
    position: absolute; background-color: #06182B;
    border-radius: 50%; width: 64px; height: 64px;
    display: flex; justify-content: center; align-items: center;
    font-size: 14px; font-weight: 900; color: #FFFFFF;
    border: 2px solid #1A446F; box-shadow: 0 6px 15px rgba(0,0,0,0.5); z-index: 5;
}
.node-top-left { top: 5px; left: 5px; }
.node-top-right { top: 5px; right: 5px; }
.node-bot-left { bottom: 5px; left: 5px; }
.node-bot-right { bottom: 5px; right: 5px; }
.pct-badge {
    position: absolute; top: 10px; right: -55px;
    color: #00D2FF; font-size: 20px; font-weight: 900; text-align: left; line-height: 1.1;
}
.pct-badge span { font-size: 11px; color: #8AB4F8; font-weight: bold; }
.network-lines { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }
.dt-title { font-size: 13px; letter-spacing: 3px; color: #8AB4F8; margin-bottom: 4px; font-weight: bold; }
.main-brand { font-size: 48px; font-weight: 950; color: #FFFFFF; margin-bottom: 6px; line-height: 1; }
.sub-brand { font-size: 12px; letter-spacing: 3px; color: #00D2FF; font-weight: bold; margin-bottom: 14px; }
.slogan { font-style: italic; color: #D1E2F4; font-size: 14px; margin-bottom: 20px; font-weight: 500; }
.tags-footer { font-size: 13px !important; color: #8AB4F8 !important; letter-spacing: 1px !important; font-weight: 700 !important; }
.ssl-footer { color: #5F82A8; font-size: 11px; margin-top: 24px; display: flex; align-items: center; gap: 6px; }

.right-wrapper {
    max-width: 400px; margin: 0 auto; padding-top: 0;
    display: flex; flex-direction: column; justify-content: center; min-height: 95vh;
}
.top-header {
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: 14px; gap: 8px;
}
.resort-badge {
    background: #0A1E33; padding: 7px 12px; border-radius: 10px;
    font-weight: bold; font-size: 12px; border: 1px solid #143A63;
    color: #FFFFFF; white-space: nowrap; flex: 1;
}
.verified-badge {
    background: rgba(0,210,255,0.08); color: #00D2FF;
    padding: 7px 12px; border-radius: 10px; font-size: 11px;
    border: 1px solid rgba(0,210,255,0.2); font-weight: 600; white-space: nowrap;
}
.login-card {
    background-color: #06182B !important; padding: 28px 24px !important;
    border-radius: 16px !important; border: 1px solid #103154 !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.6) !important;
}
.login-title { font-size: 20px; font-weight: 800; color: #FFFFFF; margin-bottom: 4px; }
.login-subtitle { font-size: 12px; color: #8AB4F8; margin-bottom: 20px; }

div[data-baseweb="input"], div[data-baseweb="input"] > div {
    background-color: #0C233C !important; border: 1px solid #1A446F !important;
    border-radius: 12px !important; height: 50px !important;
}
input { background-color: transparent !important; color: #FFFFFF !important; font-weight: 600 !important; font-size: 16px !important; }
input::placeholder { color: #5F82A8 !important; font-size: 14px !important; }
label { color: #8AB4F8 !important; font-weight: 700 !important; font-size: 13px !important; margin-bottom: 4px !important; display: block !important; }
div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
/* Remove completamente o adornment/olho nativo do Streamlit */
div[data-testid="stTextInputAdornment"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    max-width: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
    position: absolute !important;
}
div[data-baseweb="input"] > div:not(:first-child) {
    display: none !important;
}
/* Garante campo senha ocupa largura total */
div[data-baseweb="input"] input[type="password"],
div[data-baseweb="input"] input[type="text"] {
    width: 100% !important;
}
input::-ms-reveal, input::-ms-clear {
    display: none !important;
}

/* Esconde olho nativo do browser e do Streamlit no campo password */
input[type="password"]::-ms-reveal,
input[type="password"]::-ms-clear,
input[type="password"]::-webkit-credentials-auto-fill-button,
input[type="password"]::-webkit-password-auto-fill-button {
    display: none !important;
    visibility: hidden !important;
}
div[data-testid="stTextInputAdornment"],
div[data-baseweb="input"] button,
div[data-baseweb="input"] > div:last-child:not(:first-child) {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    overflow: hidden !important;
}

/* Checkbox olho senha — cor azul */
div[data-testid="stCheckbox"] { margin-top: -4px !important; margin-bottom: 8px !important; }
div[data-testid="stCheckbox"] label p { color: #5F82A8 !important; font-size: 11px !important; font-weight: 500 !important; }
/* Força cor azul no checkbox — múltiplos seletores para garantir */
div[data-testid="stCheckbox"] input[type="checkbox"] { accent-color: #185FA5 !important; }
input[type="checkbox"] { accent-color: #185FA5 !important; }
.st-emotion-cache-1pbsqtx, .st-emotion-cache-taue2i { accent-color: #185FA5 !important; }

/* Remove retângulo vazio acima do card */
div[data-testid="stVerticalBlock"] > div:empty { display: none !important; height: 0 !important; }
div.element-container:empty { display: none !important; }
div[data-testid="stVerticalBlock"] > div > div:empty { display: none !important; }

/* Remove espaço em branco acima do card */
div[data-testid="stForm"] > div:first-child { margin-top: 0 !important; padding-top: 0 !important; }
.login-card { margin-top: 0 !important; }

/* Badges compactos lado a lado */
.top-header { display: flex !important; flex-direction: row !important; gap: 8px !important; margin-bottom: 10px !important; }
.resort-badge { flex: 1 !important; text-align: left !important; }
.verified-badge { flex-shrink: 0 !important; }

div[data-testid="stForm"] button, .stButton button {
    background-color: #104A7E !important; color: #FFFFFF !important;
    border-radius: 12px !important; border: 1px solid #1A62A3 !important;
    font-weight: 800 !important; font-size: 16px !important; height: 50px !important;
    width: 100% !important; margin-top: 12px !important;
    box-shadow: 0 4px 15px rgba(16,74,126,0.4) !important;
}
div[data-testid="stForm"] button:hover { background-color: #165CA1 !important; }
div[data-testid="stNotification"] {
    background-color: #0C233C !important; border: 1px solid #1A446F !important;
    color: #8AB4F8 !important; border-radius: 10px !important; font-size: 12px !important;
}
.ssl-card-footer { text-align: center; color: #5F82A8; font-size: 10px; margin-top: 16px; }
"""

st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

col_esquerda, col_direita = st.columns([1.1, 1.0], gap="large")

# ── LADO ESQUERDO ──
with col_esquerda:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)
    html_net = """
    <div class="network-container">
        <svg class="network-lines">
            <line x1="35" y1="35" x2="265" y2="195" style="stroke:#1A446F; stroke-width:2.5" />
            <line x1="265" y1="35" x2="35" y2="195" style="stroke:#1A446F; stroke-width:2.5" />
        </svg>
        <div class="node-sat node-top-left">BIM</div>
        <div class="node-sat node-top-right">IA</div>
        <div class="node-sat node-bot-left">IoT</div>
        <div class="node-sat node-bot-right">O&M</div>
        <div class="pct-badge">88%<br><span>SLA</span></div>
        <div class="node-center">DT<br><span>Facilities</span></div>
    </div>
    """
    st.markdown(html_net, unsafe_allow_html=True)
    st.markdown('<div class="dt-title">DT FACILITIES</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-brand">O&M</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-brand">GESTÃO INTELIGENTE DE ATIVOS</div>', unsafe_allow_html=True)
    st.markdown('<div class="slogan">"Seu patrimônio sob controle, onde você estiver."</div>', unsafe_allow_html=True)
    st.markdown('<div class="tags-footer">Hospital &nbsp;•&nbsp; Resort &nbsp;•&nbsp; Supermercado &nbsp;•&nbsp; Facilities</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssl-footer">🔒 Conexão segura SSL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── LADO DIREITO ──
with col_direita:
    st.markdown('<div class="right-wrapper">', unsafe_allow_html=True)

    nome_cliente = "Acesso Uniforme"
    if st.session_state.usuario_validado in lista_usuarios:
        nome_cliente = lista_usuarios[st.session_state.usuario_validado]["cliente"]

    st.markdown(f"""
    <div class="top-header">
        <div class="resort-badge">🏢 {nome_cliente}</div>
        <div class="verified-badge">✓ Cliente verificado</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    # ── ETAPA 1: LOGIN ──
    if st.session_state.login_step == 1:
        st.markdown('<div class="login-title">Acesse sua conta</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Entre com seu e-mail e senha</div>', unsafe_allow_html=True)

        with st.form("form_etapa_1", clear_on_submit=False):
            email = st.text_input("E-mail", placeholder="seu.email@email.com")
            # Mostra como texto ou senha conforme checkbox
            if st.session_state.mostrar_senha:
                senha = st.text_input("Senha", placeholder="Digite sua senha")
            else:
                senha = st.text_input("Senha", placeholder="••••••••", type="password")
            mostrar = st.checkbox("👁️ Mostrar senha")
            st.info("🔵 Verificação em 2 etapas: Um código será enviado ao seu e-mail.")
            enviar = st.form_submit_button("Entrar", use_container_width=True)

        # Atualiza estado do olho FORA do form
        if mostrar != st.session_state.mostrar_senha:
            st.session_state.mostrar_senha = mostrar
            st.rerun()

        if enviar:
            if email in lista_usuarios and senha == lista_usuarios[email]["password"]:
                st.session_state.usuario_validado = email
                st.session_state.login_step = 2
                st.rerun()
            else:
                st.error("❌ E-mail ou senha incorretos.")

    # ── ETAPA 2: VERIFICAÇÃO 2FA ──
    elif st.session_state.login_step == 2:
        user_info = lista_usuarios[st.session_state.usuario_validado]
        st.markdown('<div class="login-title">Verificação</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="login-subtitle">Código enviado para {st.session_state.usuario_validado}</div>', unsafe_allow_html=True)
        st.info(f"🔐 Código simulado: **{user_info['token']}**")

        with st.form("form_etapa_2", clear_on_submit=False):
            codigo = st.text_input("Código de 6 dígitos", max_chars=6, placeholder="000000")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                voltar = st.form_submit_button("← Voltar", use_container_width=True)
            with col_b2:
                confirmar = st.form_submit_button("Confirmar ✓", use_container_width=True)

        if voltar:
            st.session_state.login_step = 1
            st.rerun()
        if confirmar:
            if codigo == user_info["token"]:
                st.success("✅ Acesso autorizado!")
                time.sleep(0.8)
                st.session_state.logged_in = True
                st.session_state.cliente_ativo = user_info["cliente"]
                st.session_state.login_step = 1
                st.rerun()
            else:
                st.error("❌ Código incorreto. Tente novamente.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssl-card-footer">🔒 Conexão segura SSL &nbsp;|&nbsp; © 2026 DT Facilities O&M</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
