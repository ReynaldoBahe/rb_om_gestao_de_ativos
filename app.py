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
    /* Estilos para as bolinhas coloridas da volumetria */
    .vol-title { font-size: 20px; font-weight: bold; margin-top: 15px; }
    .status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
    .dot-aberta { background-color: #22C55E; }
    .dot-atendimento { background-color: #3B82F6; }
    .dot-pausada { background-color: #EAB308; }
    .dot-fechado { background-color: #EF4444; }
    .vol-number { font-size: 36px; font-weight: bold; margin-top: 5px; }
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

# 4. CRIAÇÃO DAS ABAS
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
# ABA 2: PRODUTIVIDADE (COM VOLUMETRIA E RELATÓRIO)
# ==========================================
with aba_produtividade:
    if not df.empty:
        # --- SEÇÃO 1: VOLUMETRIA DAS OSs ---
        st.markdown('<div class="vol-title">📊 Volumetria das Ordens de Serviço</div>', unsafe_allow_html=True)
        
        # Contagem dinâmica baseada na coluna 'Status' da sua planilha
        col_status_name = next((c for c in df.columns if c.lower() == 'status'), None)
        
        qtd_aberta = 0
        qtd_atendimento = 0
        qtd_pausada = 0
        qtd_fechado = 0
        
        if col_status_name:
            status_counts = df[col_status_name].value_counts()
            qtd_aberta = int(status_counts.get('Aberta', 0))
            qtd_atendimento = int(status_counts.get('Em Andamento', 0))
            qtd_pausada = int(status_counts.get('Pausada', 0))
            qtd_fechado = int(status_counts.get('Fechado', 0))
        
        # Renderização dos 4 cards de volumetria lado a lado
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        with v_col1:
            st.markdown(f'<div><span class="status-dot dot-aberta"></span>Aberta</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{qtd_aberta}</div>', unsafe_allow_html=True)
        with v_col2:
            st.markdown(f'<div><span class="status-dot dot-atendimento"></span>Em Atendimento</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{qtd_atendimento}</div>', unsafe_allow_html=True)
        with v_col3:
            st.markdown(f'<div><span class="status-dot dot-pausada"></span>Pausada</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{qtd_pausada}</div>', unsafe_allow_html=True)
        with v_col4:
            st.markdown(f'<div><span class="status-dot dot-fechado"></span>Fechado</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{qtd_fechado}</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        
        # --- SEÇÃO 2: GRÁFICO ALTAIR ---
        st.subheader("Controle de Ordens de Serviço por Técnico")
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
        ).properties(width='container', height=350)
        
        st.altair_chart(grafico_altair, use_container_width=True)
        
        st.markdown("---")
        
        # --- SEÇÃO 3: RELATÓRIO SINCRONIZADO (A TABELA) ---
        st.markdown('📋 **Relatório Sincronizado de Ordens de Serviço**')
        # Exibe a planilha formatada de forma nativa e elegante na tela
        st.dataframe(df, use_container_width=True, hide_index=False)
        
    else:
        st.info("💡 Por favor, certifique-se de que a planilha está carregada na barra lateral para gerar os gráficos e tabelas automaticamente.")

# ==========================================
# ABA 3: CENTRO DE DIAGNÓSTICO AVANÇADO (IA PREDITIVA)
# ==========================================
with aba_diagnostico:
    st.subheader("🧠 Centro de Diagnóstico Avançado (IA Preditiva)")
    
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.markdown("🔎 **Seleção de Ativo para Auditoria**")
        lista_os = ["OS-2026-001", "OS-2026-002", "OS-2026-003"]
        os_selecionada = st.selectbox("Selecione a OS para análise da IA:", lista_os)
        
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
        st.markdown("⚡ **Análise de Engenharia Operational da IA**")
        st.success("""
        **ANÁLISE COMPLEMENTAR:** Ordem Encerrada. A OS executada por Pedro referente a 
        'Manutenção preventiva de ar-condicionado UH-202' foi devidamente finalizada de acordo 
        com as especificações técnicas do fabricante. **Recomendação:** Agendar inspeção preventiva em 90 dias.
        """)
        
        df_ia = pd.DataFrame({'Métrica': ['Ordens Fechadas'], 'Valor': [1.0]})
        grafico_ia = alt.Chart(df_ia).mark_bar(color='#1f77b4', size=150).encode(
            x=alt.X('Métrica:N', title=''),
            y=alt.Y('Valor:Q', title='Ordens Fechadas', scale=alt.Scale(domain=[0, 1.2])),
        ).properties(height=250)
        st.altair_chart(grafico_ia, use_container_width=True)
