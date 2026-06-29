import streamlit as st

st.set_page_config(page_title="Acesso ao Sistema", page_icon="🔒", layout="wide")

# 1. Inicializa as variáveis de controle global se elas não existirem
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cliente_ativo" not in st.session_state:
    st.session_state.cliente_ativo = ""

# 2. Renderiza a interface visual limpa (sem cadastro aberto)
col_central, _ = st.columns([2, 1]) # Mantém alinhado à esquerda como no seu print

with col_central:
    st.title("Acesso ao Sistema")
    st.write("Insira suas credenciais para acessar o painel de engenharia e O&M.")
    
    # Caixa visual do formulário
    with st.container(border=True):
        usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
        senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        lembrar = st.checkbox("Lembrar de mim")
        
        botao_entrar = st.button("Entrar", use_container_width=True)

# 3. Lógica de validação temporária (Simulando o Banco de Dados)
if botao_entrar:
    # Lista de usuários autorizados (Você pode expandir isso depois)
    usuarios_validos = {
        "admin": "admin",
        "cliente_fiat": "fiat123",
        "cliente_ambev": "ambev123"
    }
    
    if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
        # Ativa o carimbo digital na memória global do Streamlit
        st.session_state.logged_in = True
        
        # Define dinamicamente o nome do cliente baseado no login dele
        if usuario == "admin":
            st.session_state.cliente_ativo = "Administrador Geral"
        else:
            st.session_state.cliente_ativo = usuario.replace("cliente_", "").upper()
            
        st.success("✅ Login realizado com sucesso! Navegue pelas páginas no menu lateral.")
        st.balloons()
    else:
        st.error("❌ Usuário ou senha incorretos. Verifique suas credenciais.")
