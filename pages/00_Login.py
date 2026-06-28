import streamlit as st
import time

# --- CONTROLE DE SESSÃO INTERNO ---
if "login_step" not in st.session_state:
    st.session_state.login_step = 1

# --- CREDENCIAIS SEGURAS VIA STREAMLIT SECRETS ---
try:
    USER_CORRETO = st.secrets["auth"]["user_email"]
    SENHA_CORRETA = st.secrets["auth"]["user_password"]
    CODIGO_2FA_CORRETO = st.secrets["auth"]["token_2fa"]
except KeyError:
    USER_CORRETO = "engenharia@empresa.com"
    SENHA_CORRETA = "senha123"
    CODIGO_2FA_CORRETO = "123456"

# --- INJEÇÃO DE CSS COMPLETA (DARK MODE CORPORATIVO) ---
st.markdown("""
    <style>
        /* Ajuste do fundo global da página para o tom escuro do layout */
        .stApp { background-color: #031525; color: #FFFFFF; }
        
        /* Estilização da Coluna da Esquerda (Painel Visual) */
        .left-panel { padding: 40px 20px; text-align: center; }
        .dt-badge { background-color: #0F3B66; border-radius: 50%; width: 100px; height: 100px; line-height: 100px; margin: 0 auto 20px auto; font-weight: bold; color: #00D2FF; box-shadow: 0 0 15px rgba(0,210,255,0.3); }
        .dt-title { font-size: 14px; letter-spacing: 2px; color: #8AB4F8; margin-bottom: 5px; }
        .main-brand { font-size: 42px; font-weight: 900; color: #FFFFFF; margin-bottom: 20px; line-height: 1; }
        .sub-brand { font-size: 13px; letter-spacing: 3px; color: #8AB4F8; font-weight: bold; margin-bottom: 25px; }
        .slogan { font-style: italic; color: #9EBBDE; font-size: 15px; margin-bottom: 30px; }
        
        /* Estilização da Coluna da Direita (Card de Login) */
        .login-card { background-color: #07223D; padding: 35px; border-radius: 16px; border: 1px solid #10385F; box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
        .login-title { font-size: 28px; font-weight: bold; color: #FFFFFF; text-align: center; margin-bottom: 5px; }
        .login-subtitle { font-size: 14px; color: #9EBBDE; text-align: center; margin-bottom: 30px; }
        
        /* Ajustes nos inputs padrão do Streamlit para combinar com o tema */
        div[data-baseweb="input"] { background-color: #0E355A !important; border: 1px solid #1C4E7D !important; border-radius: 8px !important; color: white !important; }
        input { color: white !important; }
        label { color: #9EBBDE !important; font-weight: 500 !important; }
        
        /* Badge Customizado do Topo */
        .top-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
        .resort-badge { background: #0E355A; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 13px; border: 1px solid #1A4D7C; }
        .verified-badge { background: rgba(0,210,255,0.1); color: #00D2FF; padding: 6px 14px; border-radius: 20px; font-size: 12px; border: 1px solid rgba(0,210,255,0.3); }
        
        /* Rodapé de Segurança */
        .ssl-footer { color: #8AB4F8; font-size: 12px; margin-top: 20px; display: flex; align-items: center; gap: 6px; justify-content: center; }
    </style>
""", unsafe_allow_html=True)

# --- DIVISÃO DA INTERFACE EM 2 COLUNAS (MIMIC DO LAYOUT) ---
col_esquerda, col_direita = st.columns([1.1, 1.0], gap="large")

with col_esquerda:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)
    # Representação simplificada do core do diagrama em HTML
    st.markdown('<div class="dt-badge">DT<br><span style="font-size:10px;">Facilities</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="dt-title">DT FACILITIES</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-brand">O&M</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-brand">GESTÃO INTELIGENTE DE ATIVOS</div>', unsafe_allow_html=True)
    st.markdown('<div class="slogan">"Seu patrimônio sob controle, onde você estiver."</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px; color:#537BAB; word-spacing: 10px;">Hospital Resort Supermercado Facilities</p>', unsafe_allow_html=True)
    st.markdown('<div class="ssl-footer" style="justify-content:flex-start; margin-top:60px;">🔒 Conexão segura SSL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_direita:
    # Cabeçalho do Card de Login
    st.markdown('<div class="top-header">', unsafe_allow_html=True)
    st.markdown('<div class="resort-badge">🏨 Resort Boa Viagem</div>', unsafe_allow_html=True)
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
            # Simulação do aviso visual de 2FA ativado no seu layout
            st.info("🔵 **Verificação em 2 etapas:** Um código será enviado ao seu e-mail.")
            
            # Botão de Ação estilizado nativo do Streamlit (Configurado via CSS global do Streamlit)
            botao_entrar = st.form_submit_button("Entrar", use_container_width=True)
            
            if botao_entrar:
                if email == USER_CORRETO and senha == SENHA_CORRETA:
                    st.session_state.login_step = 2
                    st.rerun()
                else:
                    st.error("Credenciais inválidas. Tente engenharia@empresa.com / senha123")

    # --- ETAPA 2: TOKEN 2FA ---
    elif st.session_state.login_step == 2:
        st.markdown('<div class="login-title">Verificação</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Insira o código enviado por e-mail</div>', unsafe_allow_html=True)
        
        with st.form("form_etapa_2", clear_on_submit=False):
            codigo = st.text_input("Código de 6 dígitos", max_chars=6, placeholder="000000")
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                botao_voltar = st.form_submit_button("Voltar")
            with col_b2:
                botao_confirmar = st.form_submit_button("Confirmar", use_container_width=True)
                
            if botao_confirmar:
                if codigo == CODIGO_2FA_CORRETO:
                    st.success("Acesso autorizado!")
                    time.sleep(0.5)
                    st.session_state.logged_in = True
                    st.session_state.login_step = 1
                    st.rerun()
                else:
                    st.error("Código incorreto. Use: 123456")
                    
            if botao_voltar:
                st.session_state.login_step = 1
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssl-footer">🔒 Conexão segura SSL <span style="color:#537BAB; margin-left:20px;">© 2026 DT Facilities O&M</span></div>', unsafe_allow_html=True)
