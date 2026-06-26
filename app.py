import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import requests

# 1. Configuração Básica da Página
st.set_page_config(page_title="Visualizador Operacional de Ativos 3D", layout="wide")

# 🔐 CREDENCIAIS OPERACIONAIS AUTODESK APS
CLIENT_ID = "X1BzZjM5NSSJAYUGlCkY6FFoFCQv1GXIzZDY6Y6TwKBRAVKFT"
CLIENT_SECRET = "d2q3uGtYPYKBjiqfFpFd5OWArAhcoBuWtZwGi0fiY25TTyTjmXPConmmOFzSMo4X"
URN_MODELO = "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6YTM2MHZpZXdlci1wcm90ZWN0ZWQvdDE3ODE1Nzk3NDNfOGI0ZGU3MzMtNmU1Ny00Y2IwLWIyMzQtMWYzNzYyYjkwMTY5LnJ2dA"

# Função corrigida para obter o Token v2 da Autodesk
@st.cache_data(ttl=3500)
def obter_token_autodesk(client_id, client_secret):
    url_auth = "https://autodesk.com"
    payload = {
        "grant_type": "client_credentials",
        "scope": "viewables:read",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(url_auth, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            st.error(f"❌ Erro de Autenticação (Código {response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ Erro de Conexão com APS: {e}")
        return None

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

# 4. Processamento do Visualizador 3D
access_token = obter_token_autodesk(CLIENT_ID, CLIENT_SECRET)

if access_token and URN_MODELO:
    autodesk_html = f"""
    <div id="forgeViewer" style="width: 100%; height: 550px; background-color: #f8f9fa; border-radius: 10px; border: 1px solid #dee2e6;"></div>
    
    <link rel="stylesheet" href="https://autodesk.com" type="text/css">
    <script src="https://autodesk.com"></script>
    
    <script>
        var viewer;
        var options = {{
            env: 'AutodeskProduction2',
            api: 'streamingV2',
            getAccessToken: function(onTokenReady) {{
                onTokenReady("{access_token}", 3600);
            }}
        }};
        
        Autodesk.Viewing.Initializer(options, function() {{
            var htmlDiv = document.getElementById('forgeViewer');
            viewer = new Autodesk.Viewing.GuiViewer3D(htmlDiv);
            viewer.start();
            
            var documentId = 'urn:{URN_MODELO}';
            Autodesk.Viewing.Document.load(documentId, function(doc) {{
                var viewables = doc.getRoot().getDefaultGeometry();
                viewer.loadDocumentNode(doc, viewables);
            }}, function(errCode) {{
                console.error('Erro ao carregar o documento:', errCode);
            }});
        }});
    </script>
    """
    components.html(autodesk_html, height=570)
else:
    st.info("💡 Aguardando geração de token válido da Autodesk Platform Services.")

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
