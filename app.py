import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt
# 🔐 CREDENCIAIS OPERACIONAIS AUTODESK APS
CLIENT_ID = "X1BzZjM5NSSJAYUGlCkY6FFoFCQv1GXIzZDY6Y6TwKBRAVKFT"
CLIENT_SECRET = "d2q3uGtYPYKBjiqfFpFd5OWArAhcoBuWtZwGi0fiY25TTyTjmXPConmmOFzSMo4X"
URN_MODELO = "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6YTM2MHZpZXdlci1wcm90ZWN0ZWQvdDE3ODE1Nzk3NDNfOGI0ZGU3MzMtNmU1Ny00Y2IwLWIyMzQtMWYzNzYyYjkwMTY5LnJ2dA"

import requests

# Função oficial para obter o Token v2 da Autodesk
@st.cache_data(ttl=3500)
def obter_token_autodesk(client_id, client_secret):
    url_auth = "https://autodesk.com"
    payload = {
        "grant_type": "client_credentials",
        "scope": "viewables:read",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(url_auth, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except:
        return None


# 1. Configuração Básica da Página
st.set_page_config(page_title="Portal de Manutenção e Ativos 3D", layout="wide")

# 2. Barra Lateral (Sidebar) com as Configurações do Cliente
st.sidebar.image("https://flaticon.com", width=80)
st.sidebar.title("Configurações do Painel")

# 🔗 Campo dinâmico para colar o link do Speckle do cliente em tempo real
with aba_speckle:
    st.markdown("### Modelo Renderizado via Speckle")
    if link_cliente:
        try:
            components.iframe(link_cliente, height=550, scrolling=False)
        except Exception as e:
            st.error(f"Erro ao carregar o visualizador Speckle: {e}")
    else:
        st.info("💡 Insira o link do Speckle do cliente na barra lateral para ativar o modelo 3D.")

with aba_autodesk:
    st.markdown("### Modelo Renderizado via Autodesk APS (Nativo)")
    access_token = obter_token_autodesk(CLIENT_ID, CLIENT_SECRET)
    
    if access_token and URN_MODELO:
        autodesk_html = f"""
        <div id="forgeViewer" style="width: 100%; height: 500px; background-color: #f8f9fa; border-radius: 10px; border: 1px solid #dee2e6;"></div>
        <link rel="stylesheet" href="https://autodesk.com" type="text/css">
        <script src="https://autodesk.com"></script>
        <script>
            var viewer;
            var options = {{
                env: 'AutodeskProduction2', api: 'streamingV2',
                getAccessToken: function(onTokenReady) {{ onTokenReady("{access_token}", 3600); }}
            }};
            Autodesk.Viewing.Initializer(options, function() {{
                var htmlDiv = document.getElementById('forgeViewer');
                viewer = new Autodesk.Viewing.GuiViewer3D(htmlDiv);
                viewer.start();
                var documentId = 'urn:{URN_MODELO}';
                Autodesk.Viewing.Document.load(documentId, function(doc) {{
                    var viewables = doc.getRoot().getDefaultGeometry();
                    viewer.loadDocumentNode(doc, viewables);
                }}, null);
            }});
        </script>
        """
        components.html(autodesk_html, height=520)
    else:
        st.error("❌ Falha na geração do token. Verifique as credenciais da Autodesk no topo do arquivo.")

with aba_speckle:
    st.markdown("### Modelo Renderizado via Speckle")
    if link_cliente:
        try:
            components.iframe(link_cliente, height=550, scrolling=False)
        except Exception as e:
            st.error(f"Erro ao carregar o visualizador Speckle: {e}")
    else:
        st.info("💡 Insira o link do Speckle do cliente na barra lateral para ativar o modelo 3D.")

with aba_autodesk:
    st.markdown("### Modelo Renderizado via Autodesk APS (Nativo)")
    access_token = obter_token_autodesk(CLIENT_ID, CLIENT_SECRET)
    
    if access_token and URN_MODELO:
        autodesk_html = f"""
        <div id="forgeViewer" style="width: 100%; height: 500px; background-color: #f8f9fa; border-radius: 10px; border: 1px solid #dee2e6;"></div>
        <link rel="stylesheet" href="https://autodesk.com" type="text/css">
        <script src="https://autodesk.com"></script>
        <script>
            var viewer;
            var options = {{
                env: 'AutodeskProduction2', api: 'streamingV2',
                getAccessToken: function(onTokenReady) {{ onTokenReady("{access_token}", 3600); }}
            }};
            Autodesk.Viewing.Initializer(options, function() {{
                var htmlDiv = document.getElementById('forgeViewer');
                viewer = new Autodesk.Viewing.GuiViewer3D(htmlDiv);
                viewer.start();
                var documentId = 'urn:{URN_MODELO}';
                Autodesk.Viewing.Document.load(documentId, function(doc) {{
                    var viewables = doc.getRoot().getDefaultGeometry();
                    viewer.loadDocumentNode(doc, viewables);
                }}, null);
            }});
        </script>
        """
        components.html(autodesk_html, height=520)
    else:
        st.error("❌ Falha na geração do token. Verifique os limites de API na sua conta Autodesk.")


# 5. Indicadores de Manutenção Relacionados
st.markdown("---")
st.subheader("📊 Indicadores de Manutenção Relacionados")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # KPIs dinâmicos baseados na planilha carregada
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Ativos Mapeados", len(df))
    col2.metric("Ordens de Serviço Ativas", len(df[df['Status'].str.lower() == 'aberto']) if 'Status' in df.columns else 0)
    col3.metric("Taxa de Conformidade", "94.2%")
    
    # 📉 Gráfico de Produtividade Corrigido com Altair (Separando os técnicos sem pular ninguém)
    st.markdown("### 📊 Produtividade por Responsável Técnico")
    df_fechadas_resp = df[df['Status'].str.strip().str.lower().isin(['fechado', 'fechada'])]
    
    if not df_fechadas_resp.empty:
        df_fechadas_resp['Responsavel'] = df_fechadas_resp['Responsavel'].astype(str).str.strip()
        produtividade = df_fechadas_resp['Responsavel'].value_counts().reset_index()
        produtividade.columns = ['Responsável', 'Quantidade']
        
        chart = alt.Chart(produtividade).mark_bar(color='#1f77b4').encode(
            x=alt.X('Responsável:N', sort='-y', title='Técnico Responsável'),
            y=alt.Y('Quantidade:Q', title='Ordens Fechadas')
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Nenhuma ordem fechada encontrada na planilha para listar no gráfico de produtividade.")
        
    st.markdown("### 📋 Relatório Sincronizado de Ativos")
    st.dataframe(df, use_container_width=True)
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Ativos Regulares", "148", "+12")
    col2.metric("Manutenções Críticas", "3", "-1")
    col3.metric("Disponibilidade Geral", "98.7%")
    st.info("Aguardando upload de planilha para sincronizar os dados da tabela com o modelo 3D acima.")
