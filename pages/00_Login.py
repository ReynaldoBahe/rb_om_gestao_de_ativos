import streamlit as st

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

st.title("Acesso ao Sistema")

# CSS para estilizar nativamente o checkbox do Streamlit em ciano e aumentar a fonte
st.markdown(
    """
    <style>
    /* Altera a cor do texto do checkbox nativo e aumenta o tamanho */
    div[data-testid="stCheckbox"] label p {
        color: #00ffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    /* Opcional: Altera a cor da borda/fundo do quadrado do checkbox quando marcado */
    div[data-testid="stCheckbox"] input[type="checkbox"]:checked + div {
        background-color: #00ffff !important;
        border-color: #00ffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.form(key="login_form"):
    username = st.text_input("Usuário", placeholder="Digite seu usuário")
    password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
    
    # O checkbox agora já nasce com o texto grande e ciano integrado de forma nativa
    lembrar = st.checkbox("Lembrar de mim")
    
    submit_button = st.form_submit_button(label="Entrar")

if submit_button:
    if username == "admin" and password == "1234":
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha incorretos.")
