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
speckle_base_url = "https://app.speckle.systems/projects/a649da7292/models/815af390c7?embedToken=5fc6fc722186f65bfe3c4be3286713af5a1ab94df3"

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
    lista_os = sorted(list(df['OS'].dropna().astype(str).unique()))
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

# PROCESSAMENTO SEGURO DE VARIÁVEIS GLOBAIS
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
            id_bim_alvo = str(dados_os[col_id].values).strip()
        col_t = next((c for c in df.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel']), None)
        resp = str(dados_os[col_t].values) if col_t else "Pedro"
        setor = str(dados_os['Setor'].values) if 'Setor' in df.columns else "Climatização"
        status = str(dados_os['Status'].values) if 'Status' in df.columns else "Fechado"
        data_ab = str(dados_os['Data_Abertura'].values) if 'Data_Abertura' in df.columns else "20/06/2026"
        descricao_falha = str(dados_os['Descrição'].values) if 'Descrição' in df.columns else "Sem descrição."
        criticidade_ativo = str(dados_os['Criticidade'].values) if 'Criticidade' in df.columns else "Média"

if not id_bim_alvo or id_bim_alvo == "nan":
    id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

# ==========================================
# ABA 1: MODELO 3D (MESA DE INSPEÇÃO NA BARRA LATERAL)
# ==========================================
with aba_modelo:
    # 1. Extração segura e limpa dos dados da OS selecionada (Evita arrays e códigos do Pandas)
    id_bim_alvo_local = "29e456a92924eb3747bbcd9bb3edd623"
    setor_local = "Climatização"
    criticidade_local = "Média"
    descricao_local = "Nenhuma descrição registrada."
    
    if not df.empty and 'OS' in df.columns:
        dados_os_local = df[df['OS'].astype(str) == str(st.session_state.os_selecionada)]
        if not dados_os_local.empty:
            col_id = next((c for c in df.columns if c.upper() == 'ID'), None)
            if col_id and col_id in df.columns:
                # O .iloc[0] extrai o valor puro de dentro da célula, eliminando o erro de array
                id_bim_alvo_local = str(dados_os_local[col_id].iloc[0]).strip()
            
            setor_local = str(dados_os_local['Setor'].iloc[0]) if 'Setor' in df.columns else "Climatização"
            criticidade_local = str(dados_os_local['Criticidade'].iloc[0]) if 'Criticidade' in df.columns else "Média"
            descricao_local = str(dados_os_local['Descrição'].iloc[0]) if 'Descrição' in df.columns else "Sem descrição."

    if not id_bim_alvo_local or id_bim_alvo_local == "nan":
        id_bim_alvo_local = "29e456a92924eb3747bbcd9bb3edd623"

    # 2. INJEÇÃO DE ESTILO CSS (Isolado em string comum, sem f-string para evitar o SyntaxError)
    css_sidebar_limpa = """
    <style>
        /* Limpa visualmente os filtros originais apenas na visualização da primeira aba */
        div[data-baseweb="tab-panel"]:nth-of-type(1) ~ div[data-testid="stSidebar"] div.stSelectbox,
        div[data-baseweb="tab-panel"]:nth-of-type(1) ~ div[data-testid="stSidebar"] div.stFileUploader,
        div[data-baseweb="tab-panel"]:nth-of-type(1) ~ div[data-testid="stSidebar"] hr {
            display: none !important;
        }
        .card-inspecao {
            background-color: #F8FAFC;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            margin-top: 10px;
        }
        .card-inspecao h4 { color: #1E3A8A; margin: 0 0 10px 0; font-size: 16px; font-family: sans-serif; }
        .card-inspecao p { margin: 6px 0; font-size: 13px; color: #334155; font-family: sans-serif; line-height: 1.4; }
    </style>
    """
    st.markdown(css_sidebar_limpa, unsafe_allow_html=True)
    
    # 3. RENDERIZAÇÃO DO CONTEÚDO TÉCNICO DENTRO DA BARRA LATERAL DA ABA 1
    st.sidebar.markdown(f"""
    <div class="card-inspecao">
        <h4>🔎 Inspeção Técnica</h4>
        <p><b>Ordem de Serviço:</b><br><code>{st.session_state.os_selecionada}</code></p>
        <p><b>ID do Elemento:</b><br><code>{id_bim_alvo_local}</code></p>
        <p><b>Subsistema:</b> {setor_local}</p>
        <p><b>Nível de Risco:</b> {criticidade_local}</p>
        <hr style="border:0; border-top:1px solid #E2E8F0; margin:10px 0;">
        <p style="font-size:12px; color:#64748B;"><b>Descrição do Problema:</b><br><i>{descricao_local}</i></p>
    </div>
    """, unsafe_allow_html=True)

    # 4. VISUALIZADOR DA MAQUETE DO RESORT
    st.subheader("Visualizador Operacional de Ativos 3D")
    st.info(f"🔗 Módulo BIM Sincronizado | Foco ativo no ID: `{id_bim_alvo_local}`")
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
        
        html_ficha = "<div class='ficha-tecnica'>"
        html_ficha += "<h4 style='margin-top:0; color:#1E3A8A;'>📋 Ficha Técnica do Ativo</h4>"
        html_ficha += "<ul>"
        html_ficha += f"<li><b>Ordem de Serviço:</b> {st.session_state.os_selecionada}</li>"
        html_ficha += f"<li><b>ID BIM:</b> {id_bim_alvo}</li>"
        html_ficha += f"<li><b>Responsável Técnico:</b> {resp}</li>"
        html_ficha += f"<li><b>Setor / Subsistema:</b> {setor}</li>"
        html_ficha += f"<li><b>Status Atual:</b> {status}</li>"
        html_ficha += f"<li><b>Criticidade:</b> {criticidade_ativo}</li>"
        html_ficha += f"<li><b>Data de Abertura:</b> {data_ab}</li>"
        html_ficha += "</ul>"
        html_ficha += "<hr style='border: 0; border-top: 1px solid #BFDBFE; margin: 10px 0;'>"
        html_ficha += f"<p style='margin:0; font-size:13px; color:#1E40AF;'><b>Ocorrência Relatada:</b> {descricao_falha}</p>"
        html_ficha += "</div>"
        
        st.markdown(html_ficha, unsafe_allow_html=True)
        
    with col_dir:
        st.markdown("⚡ **Análise de Engenharia Operacional da IA**")
        
        mensagem_ia = f"**ANÁLISE DE FALHAS PREDITIVA:** A Ordem de Serviço **{st.session_state.os_selecionada}** associada ao Ativo ID `{id_bim_alvo}` foi mapeada sob criticidade **'{criticidade_ativo}'**. Recomenda-se auditoria imediata no subsistema de **{setor}** utilizando os manuais técnicos."
        st.success(mensagem_ia)
        
        valor_grafico = 1.0 if status == "Fechado" else 0.5
        df_ia = pd.DataFrame({'Indicador': ['Índice de Conclusão'], 'Valor': [valor_grafico]})
        
        # Estrutura unilinear do Altair corrigida e blindada contra SyntaxError de fechamento
