import streamlit as st

st.set_page_config(page_title="Acesso ao Sistema", page_icon="🔒", layout="wide")

# Inicializa o estado de login caso não exista
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🔑 Acesso ao Sistema")

# Cria o formulário de login baseado no seu layout visual
with st.form("form_login"):
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    lembrar = st.checkbox("Lembrar de mim")
    botao_entrar = st.form_submit_button("Entrar")

if botao_entrar:
    # DEFINA USUÁRIO E SENHA DE TESTE AQUI
    if usuario == "admin" and senha == "admin":
        st.session_state.logged_in = True
        st.session_state.cliente_ativo = "Empresa ABC"
        st.success("✅ Login realizado com sucesso! Use o menu lateral para navegar.")
        st.balloons()
    else:
        st.error("❌ Usuário ou senha incorretos.")
