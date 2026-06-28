import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="Acesso", page_icon="🔐", layout="centered")

# --- CONFIGURAÇÃO DO BANCO DE DADOS REAL (PERMANENTE) ---
DB_FILE = "usuarios.db"

def inicializar_banco():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            usuario TEXT PRIMARY KEY,
            senha TEXT
        )
    """)
    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES ('admin', '1234')")
    conn.commit()
    conn.close()

inicializar_banco()

# --- INTERFACE ---
st.title("Acesso ao Sistema")

# Estilização do checkbox ciano
st.markdown(
    """
    <style>
    div[data-testid="stCheckbox"] label p {
        color: #00ffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    div[data-testid="stCheckbox"] input[type="checkbox"]:checked + div {
        background-color: #00ffff !important;
        border-color: #00ffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

aba_login, aba_cadastro = st.tabs(["🔒 Entrar na Conta", "📝 Criar Nova Conta"])

# --- ABA 1: LOGIN ---
with aba_login:
    with st.form(key="login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário", key="login_user")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha", key="login_pass")
        lembrar = st.checkbox("Lembrar de mim")
        submit_button = st.form_submit_button(label="Entrar")

    if submit_button:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (username, password))
        usuario_valido = cursor.fetchone()
        conn.close()

        if usuario_valido:
            st.success("Login realizado com sucesso! Entrando...")
            # Salva o usuário ativo na memória global
            st.session_state["usuario_logado"] = username
            
            # Atualiza o app para que a navegação do app.py libere o portal
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

# --- ABA 2: CADASTRO PERMANENTE ---
with aba_cadastro:
    st.subheader("Cadastro de Novo Usuário")
    with st.form(key="register_form", clear_on_submit=True):
        novo_usuario = st.text_input("Escolha um Usuário (E-mail)", placeholder="Ex: seu_email@gmail.com")
        nova_senha = st.text_input("Escolha uma Senha", type="password", placeholder="Digite sua senha")
        confirma_senha = st.text_input("Confirme a Senha", type="password", placeholder="Digite novamente")
        register_button = st.form_submit_button(label="Cadastrar")
        
    if register_button:
        if not novo_usuario or not nova_senha:
            st.error("Preencha todos os campos.")
        elif nova_senha != confirma_senha:
            st.error("As senhas não coincidem.")
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (novo_usuario,))
            if cursor.fetchone():
                st.warning("Este usuário já está cadastrado.")
            else:
                cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (novo_usuario, nova_senha))
                conn.commit()
                st.success("Conta criada com sucesso! Pode mudar de aba e fazer o login.")
            conn.close()
