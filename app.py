import streamlit as st

# Configuração da página inicial
st.set_page_config(
    page_title="Portal de Engenharia & Produtividade",
    page_icon="🏗️",
    layout="wide"
)

# Estilização CSS dos Cards da Home
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 16px; color: #4B5563; margin-bottom: 25px; }
    .card-home { background-color: #F3F4F6; padding: 25px; border-radius: 8px; border: 1px solid #E5E7EB; min-height: 180px; }
    .card-home-title { font-size: 20px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏗️ Portal de Engenharia & Gestão de Projetos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Bem-vindo ao centro de controle operacional. Utilize o menu de navegação lateral à esquerda para acessar os módulos do sistema.</div>', unsafe_allow_html=True)

# Desenho dos Cards Informativos na Home
h_col1, h_col2, h_col3 = st.columns(3)

with h_col1:
    st.markdown("""
    <div class="card-home">
        <div class="card-home-title">📦 Gêmeo Digital BIM</div>
        <p style='color:#4B5563; font-size:14px;'>Acesse a maquete 3D interativa integrada via Speckle para realizar a rastreabilidade geográfica de falhas e conferir metadados técnicos dos ativos em tempo real.</p>
    </div>
    """, unsafe_allow_html=True)
    
with h_col2:
    st.markdown("""
    <div class="card-home">
        <div class="card-home-title">📊 KPIs & Produtividade</div>
        <p style='color:#4B5563; font-size:14px;'>Monitore volumetrias de Ordens de Serviço, distribua a carga de trabalho por equipe técnica e filtre gargalos operacionais por status, criticidade ou tempo de abertura.</p>
    </div>
    """, unsafe_allow_html=True)
    
with h_col3:
    st.markdown("""
    <div class="card-home">
        <div class="card-home-title">🧠 Diagnóstico por IA</div>
        <p style='color:#4B5563; font-size:14px;'>Audite ativos de forma preditiva. A nossa inteligência correlaciona dados da planilha, plota o progresso de execução e disponibiliza o link direto dos manuais técnicos.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")
st.info("💡 **Navegação:** Olhe para a barra lateral esquerda no seu navegador. O Streamlit gerou de forma automática um menu de páginas. Clique em **'01 Modulos de Engenharia'** para entrar nos painéis técnicos!")
