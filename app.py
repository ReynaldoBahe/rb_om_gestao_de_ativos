import streamlit as st
import pandas as pd
import altair as alt

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Portal de Engenharia & Produtividade",
    page_icon="🏗️",
    layout="wide"
)

# 2. DESIGN E ESTILIZAÇÃO CUSTOMIZADA
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏗️ Portal de Engenharia & Gestão de Projetos</div>', unsafe_allow_html=True)

# 3. BASE DE DADOS SIMULADA (Substitua pelo carregamento da sua planilha se necessário)
@st.cache_data
def carregar_dados():
    dados = {
        'Técnico': ['Pedro', 'Pedro', 'Marcos', 'Tiago', 'Marcos', 'Pedro', 'Tiago', 'Lucas'],
        'Ordens':,
        'Status': ['Concluído', 'Em Andamento', 'Concluído', 'Pendente', 'Concluído', 'Concluído', 'Em Andamento', 'Concluído']
    }
    return pd.DataFrame(dados)

df = carregar_dados()

# 4. CRIAÇÃO DAS ABAS (Autodesk APS removida com sucesso)
aba_modelo, aba_produtividade = st.tabs(["📦 Modelo 3D (Speckle)", "📊 Produtividade da Equipe"])

# ==========================================
# ABA 1: MODELO 3D (SPECKLE INTERATIVO)
# ==========================================
with aba_modelo:
    st.subheader("Visualização do Modelo Digital do Resort")
    st.markdown("ℹ️ *Carregamento direto via infraestrutura aberta Speckle. Custo de API: $0.00.*")
    
    # URL do Viewer do Speckle (Substitua pela URL exata do seu stream/projeto se necessário)
    speckle_url = "https://speckle.xyz" 
    
    # Renderização do visualizador 3D fluido
    st.components.v1.iframe(speckle_url, height=600, scrolling=False)

# ==========================================
# ABA 2: PRODUTIVIDADE (MOTOR ALTAIR CORRIGIDO)
# ==========================================
with aba_produtividade:
    st.subheader("Controle de Ordens de Serviço por Técnico")
    
    # Agrupamento correto dos dados por profissional
    df_produtividade = df.groupby('Técnico')['Ordens'].sum().reset_index()
    
    # Construção do gráfico corrigido usando a biblioteca Altair
    grafico_altair = alt.Chart(df_produtividade).mark_bar(color='#1f77b4').encode(
        x=alt.X('Técnico:N', title='Profissional Técnico', sort='-y'),
        y=alt.Y('Ordens:Q', title='Total de Ordens de Serviço'),
        tooltip=['Técnico', 'Ordens']
    ).properties(
        width='container',
        height=400
    )
    
    # Exibe o gráfico corrigido na tela
    st.altair_chart(grafico_altair, use_container_width=True)
    
    # Resumo das Métricas abaixo do gráfico
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-box"><b>Total de Ordens:</b><br><span style="font-size:24px;">{df["Ordens"].sum()}</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box"><b>Líder de Produção:</b><br><span style="font-size:24px;">{df_produtividade.loc[df_produtividade["Ordens"].idxmax(), "Técnico"]}</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-box"><b>Status Ativo:</b><br><span style="font-size:24px;">100% Comercial</span></div>', unsafe_allow_html=True)
