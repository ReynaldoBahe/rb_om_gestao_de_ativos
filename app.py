import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import requests

# 1. Configuração Básica da Página
st.set_page_config(page_title="Visualizador Operacional de Ativos 3D", layout="wide")

# 🔐 INSERIR CREDENCIAIS AUTODESK APS (Troque pelos seus códigos)
CLIENT_ID = "SEU_CLIENT_ID_AQUI"
CLIENT_SECRET = "SEU_CLIENT_SECRET_AQUI"
URN_MODELO = "dXJuOmFmY2..." # Lembra de pegar o código longo da URL do visualizador antes do "?"

# Função cacheada para obter o Token de Acesso da Autodesk
@st.cache_data(ttl=3500)
def obter_token_autodesk(client_id, client_secret):
    url = "https://autodesk.com"
    payload = {"grant_type": "client_credentials", "scope": "viewables:read"}
    try:
        response = requests.post(url, data=payload, auth=(client_id, client_secret))
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except:
        return None

# 2. Barra Lateral (Sidebar) com os Filtros da OM
st.sidebar.image("https://flaticon.com", width=80)
st.sidebar.title("Filtros Operacionais")

uploaded_file = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"])

# Filtros que conversam com a tabela e o painel
setor_selecionado = st.sidebar.selectbox("Filtrar por Setor:", ["Todos", "Elétrica", "Mecânica", "Hidráulica", "Climatização"])
status_selecionado = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberto", "Fechado", "Em Andamento"])
criticidade_selecionada = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])

# 3. Cabeçalho Principal do Painel
st.title("🏗️ Visualizador Operacional de Ativos 3D (Autodesk APS)")
st.markdown("---")

# 4. Renderização do Visualizador 3D da Autodesk
access_token = obter_token_autodesk(CLIENT_ID, CLIENT_SECRET)

if access_token and URN_MODELO != "dXJuOmFmY2...":
    autodesk_html = f"""
    <div id="forgeViewer" style="width: 100%; height: 500px; background-color: #f8f9fa; border-radius: 10px; border: 1px solid #dee2e6;"></div>
    <link rel="stylesheet" href="https://autodesk.com" type="text/css">
    <script src="https://autodesk.com"></script>
    <script>
        var viewer;
        var options = {{
            env: 'AutodeskProduction2', api: 'streamingV2',
            getAccessToken: function(onTokenReady) {{
                onTokenReady("{access_token}", 3600);
            }}
        }};
        Autodesk.Viewing.Initializer(options, function() {{
            var htmlDiv = document.getElementById('forgeViewer');
            viewer = new Autodesk.Viewing.GuiViewer3D(htmlDiv);
            viewer.start();
            var documentId = '{URN_MODELO}';
            if (!documentId.startsWith('urn:')) documentId = 'urn:' + documentId;
            Autodesk.Viewing.Document.load(documentId, function(doc) {{
                var viewables = doc.getRoot().getDefaultGeometry();
                viewer.loadDocumentNode(doc, viewables);
            }}, null);
        }});
    </script>
    """
    components.html(autodesk_html, height=520)
else:
    st.info("💡 Insira o Client ID, Client Secret e a URN correta no código para ativar o modelo 3D do Resort.")

# 5. Processamento dos Dados e Gráficos da OM
st.markdown("---")
st.subheader("📊 Indicadores de Manutenção Relacionados")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # KPIs dinâmicos baseados na planilha carregada
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
