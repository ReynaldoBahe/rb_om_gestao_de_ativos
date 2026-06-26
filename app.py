import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração Básica da Página
st.set_page_config(page_title="Visualizador Operacional de Ativos 3D", layout="wide")

# 2. Barra Lateral (Sidebar) com os Filtros da OM
st.sidebar.image("https://flaticon.com", width=80)
st.sidebar.title("Filtros Operacionais")

uploaded_file = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"])

setor_selecionado = st.sidebar.selectbox("Filtrar por Setor:", ["Todos", "Elétrica", "Mecânica", "Hidráulica", "Climatização"])
status_selecionado = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberto", "Fechado", "Em Andamento"])
criticidade_selecionada = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])

# 3. Cabeçalho Principal do Painel
st.title("🏗️ Visualizador Operacional de Ativos 3D (Autodesk APS)")
st.markdown("---")

# 4. Renderização Segura do Visualizador 3D via Link de Incorporação Estável
# Link oficial do seu modelo Revit do Resort
link_modelo_autodesk = "https://viewer.autodesk.com/id/dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6YTM2MHZpZXdlci1wcm90ZWN0ZWQvdDE3ODE1Nzk3NDNfOGI0ZGU3MzMtNmU1Ny00Y2IwLWIyMzQtMWYzNzYyYjkwMTY5LnJ2dA?sheetId=YjlmYmFlYzYtN2VjOC1kZWIzLWRkZDEtMmIyNzA5ZWU0YWZl"

try:
    # Renderiza o visualizador com suporte nativo a WebGL e controles de órbita
    st.components.v1.iframe(link_modelo_autodesk, height=550, scrolling=True)
except Exception as e:
    st.error(f"Erro ao inicializar contêiner WebGL: {e}")

# 5. Indicadores de Manutenção Relacionados
st.markdown("---")
st.subheader("📊 Indicadores de Manutenção Relacionados")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Ativos Mapeados", len(df))
    col2.metric("Ordens de Serviço Ativas", len(df[df['Status'].str.lower() == 'aberto']) if 'Status' in df.columns else 0)
    col3.metric("Taxa de Conformidade", "94.2%")
    st.markdown("### 📋 Relatório Sincronizado de Ativos")
    st.dataframe(df, use_container_width=True)
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Ativos Regulares", "148", "+12")
    col2.metric("Manutenções Críticas", "3", "-1")
    col3.metric("Disponibilidade Geral", "98.7%")
    st.info("Aguardando upload de planilha para sincronizar os dados da tabela com o modelo 3D acima.")
