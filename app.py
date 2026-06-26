import streamlit as st
import pandas as pd
import altair as alt

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Portal de Engenharia & Produtividade",
    page_icon="🏗️",
    layout="wide"
)

# ==========================================
# 2. DESIGN E ESTILIZAÇÃO CUSTOMIZADA (CSS)
# ==========================================
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; margin-bottom: 20px; }
    .ficha-tecnica { background-color: #EFF6FF; padding: 20px; border-radius: 8px; border: 1px solid #BFDBFE; }
    .vol-title { font-size: 20px; font-weight: bold; margin-top: 15px; }
    .status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
    .dot-aberta { background-color: #22C55E; }
    .dot-atendimento { background-color: #3B82F6; }
    .dot-pausada { background-color: #EAB308; }
    .dot-fechado { background-color: #EF4444; }
    .vol-number { font-size: 36px; font-weight: bold; margin-top: 5px; }
    .card-inspecao-local { background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-top: 10px; }
    .card-inspecao-local h4 { color: #1E3A8A; margin: 0 0 10px 0; font-size: 16px; font-family: sans-serif; }
    .card-inspecao-local p { margin: 6px 0; font-size: 13px; color: #334155; font-family: sans-serif; line-height: 1.4; }
    
    /* Remove a borda padrão do radio para simular abas perfeitamente */
    div[data-testid="stRadio"] > label { display: none; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏗️ Portal de Engenharia & Gestão de Projetos</div>', unsafe_allow_html=True)

# URL base do Speckle original aprovado
speckle_base_url = "https://speckle.systems"

# Persistência segura da planilha na sessão do usuário
if 'df_global' not in st.session_state:
    st.session_state.df_global = pd.DataFrame()

df = st.session_state.df_global

# ==========================================
# 3. SELETOR NATIVO DE NAVEGAÇÃO (SUBSTITUI ST.TABS POR SEGURANÇA VISUAL)
# ==========================================
if 'aba_ativa' not in st.session_state:
    st.session_state.aba_ativa = "📦 Modelo 3D (Speckle)"

opcoes_menu = ["📦 Modelo 3D (Speckle)", "📊 Produtividade da Equipe", "🧠 Centro de Diagnóstico (IA)"]
aba_selecionada = st.radio("", opcoes_menu, index=opcoes_menu.index(st.session_state.aba_ativa), horizontal=True)
st.session_state.aba_ativa = aba_selecionada

# Mapeia dinamicamente a lista de OS disponíveis
if not df.empty and 'OS' in df.columns:
    lista_os = sorted(list(df['OS'].dropna().astype(str).unique()))
else:
    lista_os = ["OS-2026-001", "OS-2026-002", "OS-2026-003"]

if 'os_selecionada' not in st.session_state or st.session_state.os_selecionada not in lista_os:
    if lista_os:
        st.session_state.os_selecionada = lista_os[0]

# -------------------------------------------------------------------------
# PROCESSAMENTO DE VARIÁVEIS GLOBAIS COM BASE NA PLANILHA CARREGADA
# -------------------------------------------------------------------------
id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"
resp = "Pedro"
setor = "Climatização"
status = "Fechado"
data_ab = "20/06/2026"
descricao_falha = "Aguardando verificação do sistema."
criticidade_ativo = "Média"

if not df.empty and 'OS' in df.columns:
    dados_os = df[df['OS'].astype(str) == str(st.session_state.os_selecionada)]
    if not dados_os.empty:
        col_id = next((c for c in df.columns if c.upper() == 'ID'), None)
        if col_id:
            id_bim_alvo = str(dados_os[col_id].values[0]).strip()
        col_t = next((c for c in df.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel']), None)
        resp = str(dados_os[col_t].values[0]) if col_t else "Pedro"
        setor = str(dados_os['Setor'].values[0]) if 'Setor' in df.columns else "Climatização"
        status = str(dados_os['Status'].values[0]) if 'Status' in df.columns else "Fechado"
        data_ab = str(dados_os['Data_Abertura'].values[0]) if 'Data_Abertura' in df.columns else "20/06/2026"
        descricao_falha = str(dados_os['Descrição'].values[0]) if 'Descrição' in df.columns else "Sem descrição."
        criticidade_ativo = str(dados_os['Criticidade'].values[0]) if 'Criticidade' in df.columns else "Média"

if not id_bim_alvo or id_bim_alvo == "nan":
    id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

# ==========================================
# 4. CONTROLE SEGURO DA BARRA LATERAL CONFORME A PÁGINA ATIVA
# ==========================================
st.sidebar.header("Painel de Visão")

if st.session_state.aba_ativa == "📦 Modelo 3D (Speckle)":
    # ABA 1: Barra lateral exibe APENAS o cartão de inspeção limpo, sem filtros
    st.sidebar.markdown(f"""
    <div class="card-inspecao-local">
        <h4>🔎 Inspeção Técnica</h4>
        <p><b>Ordem de Serviço:</b><br><code>{st.session_state.os_selecionada}</code></p>
        <p><b>ID do Elemento:</b><br><code>{id_bim_alvo}</code></p>
        <p><b>Subsistema:</b> {setor}</p>
        <p><b>Nível de Risco:</b> {criticidade_ativo}</p>
        <hr style="border:0; border-top:1px solid #E2E8F0; margin:10px 0;">
        <p style="font-size:12px; color:#64748B;"><b>Descrição do Problema:</b><br><i>{descricao_falha}</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.write("---")
    arquivo_upload = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"], key="up_m1")

else:
    # ABAS 2 E 3: Barra lateral exibe os filtros originais aprovados normalmente
    filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"])
    filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])
    filtro_tempo = st.sidebar.selectbox("Filtrar por Tempo Aberta:", ["Todos", "Menos de 24h", "Entre 2 e 7 dias", "Mais de 7 dias"])
    
    st.sidebar.write("---")
    arquivo_upload = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"], key="up_m23")

# Sincroniza o arquivo carregado de qualquer uma das origens
if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            st.session_state.df_global = pd.read_csv(arquivo_upload)
        else:
            st.session_state.df_global = pd.read_excel(arquivo_upload)
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

st.write("---")

# ==========================================
# 5. RENDERIZAÇÃO LÓGICA E ISOLADA DAS PÁGINAS
# ==========================================

# TELA 1: MODELO 3D
if st.session_state.aba_ativa == "📦 Modelo 3D (Speckle)":
    st.subheader("Visualizador Operacional de Ativos 3D")
    st.info(f"🔗 Módulo BIM Sincronizado | Rastreando Ativo ID: `{id_bim_alvo}` (Selecione outra OS na aba Centro de Diagnóstico para focar)")
    st.components.v1.iframe(speckle_base_url, height=600, scrolling=False)

# TELA 2: PRODUTIVIDADE DA EQUIPE
elif st.session_state.aba_ativa == "📊 Produtividade da Equipe":
    if not df.empty:
        df_filtrado = df.copy()
        if 'filtro_status' in locals() and filtro_status != "Todos" and 'Status' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
            
        st.markdown('<div class="vol-title">📊 Volumetria das Ordens de Serviço</div>', unsafe_allow_html=True)
        col_status_name = next((c for c in df.columns if c.lower() == 'status'), None)
        status_counts = df[col_status_name].value_counts() if col_status_name else {}
        
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        with v_col1:
            st.markdown('<div><span class="status-dot dot-aberta"></span>Aberta</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{int(status_counts.get("Aberta", 0))}</div>', unsafe_allow_html=True)
        with v_col2:
            st.markdown('<div><span class="status-dot dot-atendimento"></span>Em Atendimento</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{int(status_counts.get("Em Andamento", 0))}</div>', unsafe_allow_html=True)
        with v_col3:
            st.markdown('<div><span class="status-dot dot-pausada"></span>Pausada</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{int(status_counts.get("Pausada", 0))}</div>', unsafe_allow_html=True)
        with v_col4:
            st.markdown('<div><span class="status-dot dot-fechado"></span>Fechado</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="vol-number">{int(status_counts.get("Fechado", 0))}</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("Controle de Ordens de Serviço por Técnico")
        col_tecnico = next((c for c in df_filtrado.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel', 'técnico responsável']), df_filtrado.columns)
        df_produtividade = df_filtrado.groupby(col_tecnico).size().reset_index(name='Ordens')
        df_produtividade.columns = ['Técnico', 'Ordens']
        
        grafico_altair = alt.Chart(df_produtividade).mark_bar(color='#1f77b4').encode(
            x=alt.X('Técnico:N', title='Profissional Técnico', sort='-y'),
            y=alt.Y('Ordens:Q', title='Total de Ordens de Serviço'),
            tooltip=['Técnico', 'Ordens']
        ).properties(width='container', height=350)
        st.altair_chart(grafico_altair, use_container_width=True)
        
        st.markdown("---")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.info("💡 Por favor, certifique-se de que a planilha está carregada na barra lateral.")

