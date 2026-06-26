import streamlit as st
import pandas as pd
import altair as alt

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Portal de Engenharia & Produtividade",
    page_icon="🏗️",
    layout="wide"
)

# 2. DESIGN E ESTILIZAÇÃO CUSTOMIZADA (CSS)
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
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏗️ Portal de Engenharia & Gestão de Projetos</div>', unsafe_allow_html=True)

# 3. BARRA LATERAL (FILTROS OPERACIONAIS LIMPOS)
st.sidebar.header("Filtros de Visão")

filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"])
filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])
filtro_tempo = st.sidebar.selectbox("Filtrar por Tempo Aberta:", ["Todos", "Menos de 24h", "Entre 2 e 7 dias", "Mais de 7 dias"])

st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"])

# URL base do Speckle em modo embed limpo
speckle_base_url = "https://app.speckle.systems/projects/a649da7292/models/815af390c7?embedToken=fd704d8c9c65c33217812bb9e35c7feb7c8d20314f"

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

# Mapeia dinamicamente a lista de OS disponíveis
if not df.empty and 'OS' in df.columns:
    lista_os = sorted(list(df['OS'].dropna().unique()))
else:
    lista_os = ["OS-2026-001", "OS-2026-002", "OS-2026-003"]

# 4. CONFIGURAÇÃO DO ESTADO DA SESSÃO (SESSION STATE)
if 'os_selecionada' not in st.session_state or st.session_state.os_selecionada not in lista_os:
    if lista_os:
        st.session_state.os_selecionada = lista_os[0]

# 5. CRIAÇÃO DAS ABAS (OS 3 MÓDULOS)
aba_modelo, aba_produtividade, aba_diagnostico = st.tabs([
    "📦 Modelo 3D (Speckle)", 
    "📊 Produtividade da Equipe", 
    "🧠 Centro de Diagnóstico (IA)"
])

# ==========================================
# ABA 1: MODELO 3D (RASTREABILIDADE BIM)
# ==========================================
with aba_modelo:
    st.subheader("Visualizador Operacional de Ativos 3D")
    
    id_bim_alvo = ""
    if not df.empty and 'OS' in df.columns:
        col_id = next((c for c in df.columns if c.upper() == 'ID'), None)
        if col_id:
            linha_ativo = df[df['OS'] == st.session_state.os_selecionada]
            if not linha_ativo.empty:
                id_bim_alvo = str(linha_ativo[col_id].values[0]).strip()

    if not id_bim_alvo or id_bim_alvo == "nan":
        id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

    # Exibição elegante da inteligência de cruzamento de dados (Sem botões que não funcionam)
    st.info(f"🔗 Módulo BIM Sincronizado | Rastreando Ativo ID: `{id_bim_alvo}` (Selecionado no Centro de Diagnóstico)")
    
    st.components.v1.iframe(speckle_base_url, height=600, scrolling=False)

# ==========================================
# ABA 2: PRODUTIVIDADE E RELATÓRIO
# ==========================================
with aba_produtividade:
    if not df.empty:
        df_filtrado = df.copy()
        if filtro_status != "Todos" and 'Status' in df_filtrado.columns:
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
        st.markdown('📋 **Relatório Sincronizado de Ordens de Serviço**')
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.info("💡 Por favor, certifique-se de que a planilha está carregada na barra lateral.")
# ==========================================
# 3. BARRA LATERAL E TRATAMENTO SEGURO DE DADOS
# ==========================================
# [Mantenha seus selectboxes de filtros da barra lateral aqui...]

# Lógica de carregamento de dados segura e inteligente
df = pd.DataFrame()
if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df = pd.read_csv(arquivo_upload)
        else:
            df = pd.read_excel(arquivo_upload)
        st.sidebar.success("📊 Planilha processada com sucesso!")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

# -------------------------------------------------------------------------
# MOTOR DE IDENTIFICAÇÃO DINÂMICA DE COLUNAS (FLEXIBILIDADE DE ENGENHARIA)
# -------------------------------------------------------------------------
# Dicionário global para armazenar os nomes reais das colunas da planilha
mapeamento_colunas = {
    "OS": "OS",
    "ID": "ID",
    "Status": "Status",
    "Criticidade": "Criticidade",
    "Setor": "Setor",
    "Tecnico": "Técnico"
}

if not df.empty:
    # Varre as colunas reais do arquivo para encontrar correspondências ignorando maiúsculas/acentos
    colunas_reais = list(df.columns)
    
    for col in colunas_reais:
        c_upper = col.upper().strip()
        if c_upper in ["OS", "ORDEM DE SERVIÇO", "NUMERO_OS"]:
            mapeamento_colunas["OS"] = col
        elif c_upper in ["ID", "ID BIM", "ID_BIM", "ELEMENTID", "CODIGO"]:
            mapeamento_colunas["ID"] = col
        elif c_upper in ["STATUS", "SITUACAO", "SITUAÇÃO"]:
            mapeamento_colunas["Status"] = col
        elif c_upper in ["CRITICIDADE", "GRAVIDADE", "RISCO"]:
            mapeamento_colunas["Criticidade"] = col
        elif c_upper in ["SETOR", "SUBSISTEMA", "DISCIPLINA", "AREA", "ÁREA"]:
            mapeamento_colunas["Setor"] = col
        elif c_upper in ["TÉCNICO", "TECNICO", "RESPONSÁVEL", "RESPONSAVEL", "OPERADOR"]:
            mapeamento_colunas["Tecnico"] = col

# Mapeia dinamicamente a lista de OS disponíveis com base na coluna identificada
if not df.empty and mapeamento_colunas["OS"] in df.columns:
    lista_os = sorted(list(df[mapeamento_colunas["OS"]].dropna().unique()))
else:
    # Fallback caso não haja arquivo carregado
    lista_os = ["OS-2026-001", "OS-2026-002", "OS-2026-003"]

# 4. CONFIGURAÇÃO DO ESTADO DA SESSÃO (SESSION STATE)
if 'os_selecionada' not in st.session_state or st.session_state.os_selecionada not in lista_os:
    if lista_os:
        st.session_state.os_selecionada = lista_os[0]

# 5. CRIAÇÃO DAS ABAS (OS 3 MÓDULOS)
aba_modelo, aba_produtividade, aba_diagnostico = st.tabs([
    "📦 Modelo 3D (Speckle)", 
    "📊 Produtividade da Equipe", 
    "🧠 Centro de Diagnóstico (IA)"
])
