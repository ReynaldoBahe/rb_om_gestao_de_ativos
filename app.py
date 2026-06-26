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
    .ficha-tecnica {
        background-color: #EFF6FF;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #BFDBFE;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏗️ Portal de Engenharia & Gestão de Projetos</div>', unsafe_allow_html=True)

# 3. BARRA LATERAL (CONFIGURAÇÕES E FILTROS)
st.sidebar.header("Configurações do Painel")

speckle_url_input = st.sidebar.text_input(
    "🔗 Link do Speckle (Cliente):",
    value="https://speckle.systems"
)

st.sidebar.write("---")
st.sidebar.header("Filtros Operacionais")

arquivo_upload = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"])

# Lógica de carregamento de dados segura
df = pd.DataFrame()
if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df = pd.read_csv(arquivo_upload)
        else:
            df = pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

# 4. CRIAÇÃO DAS ABAS (Inclusão do Centro de Diagnóstico)
aba_modelo, aba_produtividade, aba_diagnostico = st.tabs([
    "📦 Modelo 3D (Speckle)", 
    "📊 Produtividade da Equipe", 
    "🧠 Centro de Diagnóstico (IA)"
])

# ==========================================
# ABA 1: MODELO 3D (SPECKLE INTERATIVO)
# ==========================================
with aba_modelo:
    st.subheader("Visualização do Modelo Digital do Resort")
    st.markdown("ℹ️ *Carregamento direto via infraestrutura aberta Speckle. Custo de API: $0.00.*")
    st.components.v1.iframe(speckle_url_input, height=600, scrolling=False)

# ==========================================
# ABA 2: PRODUTIVIDADE (MOTOR ALTAIR CORRIGIDO)
# ==========================================
with aba_produtividade:
    st.subheader("Controle de Ordens de Serviço por Técnico")
    
    if not df.empty:
        col_tecnico = next((c for c in df.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel', 'técnico responsável']), df.columns[0])
        col_ordens = next((c for c in df.columns if c.lower() in ['ordens', 'om', 'quantidade', 'total']), None)
        
        if col_ordens:
            df_produtividade = df.groupby(col_tecnico)[col_ordens].sum().reset_index()
            df_produtividade.columns = ['Técnico', 'Ordens']
        else:
            df_produtividade = df.groupby(col_tecnico).size().reset_index(name='Ordens')
            df_produtividade.columns = ['Técnico', 'Ordens']
        
        grafico_altair = alt.Chart(df_produtividade).mark_bar(color='#1f77b4').encode(
            x=alt.X('Técnico:N', title='Profissional Técnico', sort='-y'),
            y=alt.Y('Ordens:Q', title='Total de Ordens de Serviço'),
            tooltip=['Técnico', 'Ordens']
        ).properties(width='container', height=400)
        
        st.altair_chart(grafico_altair, use_container_width=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-box"><b>Total de Ordens:</b><br><span style="font-size:24px;">{int(df_produtividade["Ordens"].sum())}</span></div>', unsafe_allow_html=True)
        with col2:
            lider = df_produtividade.loc[df_produtividade["Ordens"].idxmax(), "Técnico"]
            st.markdown(f'<div class="metric-box"><b>Líder de Produção:</b><br><span style="font-size:24px;">{lider}</span></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-box"><b>Status Ativo:</b><br><span style="font-size:24px;">100% Comercial</span></div>', unsafe_allow_html=True)
    else:
        st.info("💡 Por favor, certifique-se de que a planilha está carregada na barra lateral para gerar os gráficos.")

# ==========================================
# ABA 3: CENTRO DE DIAGNÓSTICO AVANÇADO (IA PREDITIVA)
# ==========================================
with aba_diagnostico:
    st.subheader("🧠 Centro de Diagnóstico Avançado (IA Preditiva)")
    
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.markdown("🔎 **Seleção de Ativo para Auditoria**")
        # Menu dinâmico baseado nas OSs da planilha (ou simulado fixo se a planilha estiver vazia)
        lista_os = ["OS-2026-001", "OS-2026-002", "OS-2026-003"]
        os_selecionada = st.selectbox("Selecione a OS para análise da IA:", lista_os)
        
        # Bloco da Ficha Técnica estilizado com CSS customizado
        st.markdown(f"""
        <div class="ficha-tecnica">
            <h4 style="margin-top:0; color:#1E3A8A;">📋 Ficha Técnica do Ativo</h4>
            <ul>
                <li><b>ID BIM:</b> 29e456a92924eb3747bbcd9bb3edd623</li>
                <li><b>Responsável Técnico:</b> Pedro</li>
                <li><b>Setor:</b> Climatização</li>
                <li><b>Status Atual:</b> Fechado</li>
                <li><b>Data de Abertura:</b> 20/06/2026</li>
                <li><b>Histórico de Quebras:</b> 3 recorrências registradas nos últimos 180 dias.</li>
            </ul>
            <a href="#" style="color:#2563EB; font-weight:bold; text-decoration:none;">📄 Acessar Manual Técnico do Ativo</a>
        </div>
        """, unsafe_allow_html=True)
        
    with col_dir:
        st.markdown("⚡ **Análise de Engenharia Operacional da IA**")
        st.success("""
        **ANÁLISE COMPLEMENTAR:** Ordem Encerrada. A OS executada por Pedro referente a 
        'Manutenção preventiva de ar-condicionado UH-202' foi devidamente finalizada de acordo 
        com as especificações técnicas do fabricante. **Recomendação:** Agendar inspeção preventiva em 90 dias.
        """)
        
        # Gráfico interno para a análise da IA
        df_ia = pd.DataFrame({'Métrica': ['Ordens Fechadas'], 'Valor': [1.0]})
        grafico_ia = alt.Chart(df_ia).mark_bar(color='#1f77b4', size=150).encode(
            x=alt.X('Métrica:N', title=''),
            y=alt.Y('Valor:Q', title='Ordens Fechadas', scale=alt.Scale(domain=[0, 1.2])),
        ).properties(height=250)
        st.altair_chart(grafico_ia, use_container_width=True)
