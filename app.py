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

# 3. BARRA LATERAL (FILTROS CONSOLIDADOS)
st.sidebar.header("Filtros de Visão")

# Filtros por caixas de seleção
filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"])
filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])
filtro_tempo = st.sidebar.selectbox("Filtrar por Tempo Aberta:", ["Todos", "Menos de 24h", "Entre 2 e 7 dias", "Mais de 7 dias"])

st.sidebar.write("---")
st.sidebar.header("🔍 Localização de Ativos (BIM)")

# Texto do botão atualizado para corresponder perfeitamente à função comercial
ativar_visao_cromatica = st.sidebar.toggle("🎯 Identificar ID do Ativo no Modelo")

st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"])

# URL base do Speckle em modo embed
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
        st.session_state.os_selecionada = lista_os

# 5. CRIAÇÃO DAS ABAS (OS 3 MÓDULOS)
aba_modelo, aba_produtividade, aba_diagnostico = st.tabs([
    "📦 Modelo 3D (Speckle)", 
    "📊 Produtividade da Equipe", 
    "🧠 Centro de Diagnóstico (IA)"
])

# ==========================================
# ABA 1: MODELO 3D (SPECKLE DINÂMICO LIMPO)
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

    # ID reserva do resort para o app não abrir em branco
    if not id_bim_alvo or id_bim_alvo == "nan" or "Array" in id_bim_alvo:
        id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

    # AGORA SIM: Lógica de isolamento real e automático por URL
    if ativar_visao_cromatica and id_bim_alvo:
        # O parâmetro &isolate força o Speckle a esconder o resort e focar na peça automaticamente
        url_visualizador = f"{speckle_base_url}&isolate=%5B%22{id_bim_alvo}%22%5D"
        st.success(f"🎯 Isolamento Digital Ativo: Focando cirurgicamente no Ativo BIM `{id_bim_alvo}`")
    else:
        url_visualizador = speckle_base_url
        st.markdown("ℹ️ *Visualização padrão do modelo de engenharia.*")
        
    st.components.v1.iframe(url_visualizador, height=600, scrolling=False)

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
# ABA 3: CENTRO DE DIAGNÓSTICO AVANÇADO
# ==========================================
with aba_diagnostico:
    st.subheader("🧠 Centro de Diagnóstico Avançado (IA Preditiva)")
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.markdown("🔎 **Seleção de Ativo para Auditoria**")
        
        st.session_state.os_selecionada = st.selectbox(
            "Selecione a OS para análise da IA:", 
            lista_os, 
            index=lista_os.index(st.session_state.os_selecionada) if st.session_state.os_selecionada in lista_os else 0
        )
        
        resp, setor, status, data_ab = "Pedro", "Climatização", "Fechado", "20/06/2026"
        if not df.empty and 'OS' in df.columns:
            dados_os = df[df['OS'] == st.session_state.os_selecionada]
            if not dados_os.empty:
                col_t = next((c for c in df.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel']), None)
                resp = str(dados_os[col_t].values) if col_t else "Pedro"
                setor = str(dados_os['Setor'].values) if 'Setor' in df.columns else "Climatização"
                status = str(dados_os['Status'].values) if 'Status' in df.columns else "Fechado"
                data_ab = str(dados_os['Data_Abertura'].values) if 'Data_Abertura' in df.columns else "20/06/2026"

        html_ficha = '<div class="ficha-tecnica"><h4 style="margin-top:0; color:#1E3A8A;">📋 Ficha Técnica do Ativo</h4><ul>'
        html_ficha += f'<li><b>ID BIM:</b> {id_bim_alvo}</li>'
        html_ficha += f'<li><b>Responsável Técnico:</b> {resp}</li>'
        html_ficha += f'<li><b>Setor:</b> {setor}</li>'
        html_ficha += f'<li><b>Status Atual:</b> {status}</li>'
        html_ficha += f'<li><b>Data de Abertura:</b> {data_ab}</li>'
        html_ficha += '<li><b>Histórico de Quebras:</b> 3 recorrências registradas nos últimos 180 dias.</li></ul>'
        html_ficha += '<a href="#" style="color:#2563EB; font-weight:bold; text-decoration:none;">📄 Acessar Manual Técnico do Ativo</a></div>'
        st.markdown(html_ficha, unsafe_allow_html=True)
        
    with col_dir:
        st.markdown("⚡ **Análise de Engenharia Operacional da IA**")
        
        mensagem_ia = f"**ANÁLISE COMPLEMENTAR:** Ordem {st.session_state.os_selecionada}. Ativo BIM analisado sob status '{status}'. Plano recomendado para {setor}."
        st.success(mensagem_ia)
        
        df_ia = pd.DataFrame({'Métrica': ['Ordens Analisadas'], 'Valor': [1.0]})
        grafico_ia = alt.Chart(df_ia).mark_bar(color='#1f77b4', size=150).encode(
            x=alt.X('Métrica:N', title=''),
            y=alt.Y('Valor:Q', title='Status de Execução', scale=alt.Scale(domain=[0, 1.2])),
        ).properties(height=250)
        st.altair_chart(grafico_ia, use_container_width=True)
