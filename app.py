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
# ABA 2: PRODUTIVIDADE E RELATÓRIO (COM FILTRO DE TEMPO ABERTO)
# ==========================================
with aba_produtividade:
    if not df.empty:
        df_filtrado = df.copy()
        
        # 1. TRATAMENTO INTELIGENTE DE DATAS E TEMPO DE ABERTURA
        if 'Data_Abertura' in df_filtrado.columns:
            try:
                # Converte a coluna para data de forma segura
                df_filtrado['Data_Abertura_dt'] = pd.to_datetime(df_filtrado['Data_Abertura'], errors='coerce')
                
                # Considera a data atual do sistema (2026) para calcular os dias aberta
                data_atual = pd.to_datetime('2026-06-26')
                df_filtrado['Dias_Aberta'] = (data_atual - df_filtrado['Data_Abertura_dt']).dt.days
                
                # Aplica a filtragem na tabela com base na escolha da barra lateral
                if filtro_tempo == "Menos de 24h":
                    df_filtrado = df_filtrado[df_filtrado['Dias_Aberta'] <= 1]
                elif filtro_tempo == "Entre 2 e 7 days":
                    df_filtrado = df_filtrado[(df_filtrado['Dias_Aberta'] > 1) & (df_filtrado['Dias_Aberta'] <= 7)]
                elif filtro_tempo == "Mais de 7 dias":
                    df_filtrado = df_filtrado[df_filtrado['Dias_Aberta'] > 7]
            except Exception as e:
                st.warning(f"Aviso no cálculo de tempo operacional: {e}")

        # 2. APLICAÇÃO DOS FILTROS ORIGINAIS DE STATUS E CRITICIDADE
        if filtro_status != "Todos" and 'Status' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
        if filtro_criticidade != "Todos" and 'Criticidade' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Criticidade'] == filtro_criticidade]
            
        # 3. RENDERIZAÇÃO DA VOLUMETRIA ATUALIZADA
        st.markdown('<div class="vol-title">📊 Volumetria das Ordens de Serviço</div>', unsafe_allow_html=True)
        col_status_name = next((c for c in df.columns if c.lower() == 'status'), None)
        status_counts = df_filtrado[col_status_name].value_counts() if col_status_name else {}
        
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
        
        # 4. GRÁFICO ALTAIR REATIVO AO TEMPO ABERTO
        st.subheader("Controle de Ordens de Serviço por Técnico")
        col_tecnico = next((c for c in df_filtrado.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel', 'técnico responsável']), df_filtrado.columns[0])
        
        if not df_filtrado.empty:
            df_produtividade = df_filtrado.groupby(col_tecnico).size().reset_index(name='Ordens')
            df_produtividade.columns = ['Técnico', 'Ordens']
            
            grafico_altair = alt.Chart(df_produtividade).mark_bar(color='#1f77b4').encode(
                x=alt.X('Técnico:N', title='Profissional Técnico', sort='-y'),
                y=alt.Y('Ordens:Q', title='Total de Ordens de Serviço'),
                tooltip=['Técnico', 'Ordens']
            ).properties(width='container', height=350)
            st.altair_chart(grafico_altair, use_container_width=True)
        else:
            st.info("Nenhuma ordem encontrada para a combinação de filtros selecionada.")
        
        st.markdown("---")
        st.markdown('📋 **Relatório Sincronizado de Ordens de Serviço**')
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.info("💡 Por favor, certifique-se de que a planilha está carregada na barra lateral.")

# ==========================================
# 3. BARRA LATERAL (MENU ÚNICO, FIXO E ESTÁVEL NAS 3 ABAS)
# ==========================================
st.sidebar.header("Painel de Controle")

# Campo de carregamento unificado no topo da área cinza
arquivo_upload = st.sidebar.file_uploader("📂 Carregar Planilha CMMS (.csv)", type=["csv", "xlsx"])

st.sidebar.write("---")
st.sidebar.subheader("Filtros de Visão")

filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"])
filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])
filtro_tempo = st.sidebar.selectbox("Filtrar por Tempo Aberta:", ["Todos", "Menos de 24h", "Entre 2 e 7 dias", "Mais de 7 dias"])

# URL base fixa do Speckle em modo embed limpo original aprovado
speckle_base_url = "https://speckle.systems"

# Lógica de carregamento de dados segura e silenciosa no backend
df = pd.DataFrame()
if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df = pd.read_csv(arquivo_upload)
        else:
            df = pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

# Mapeia dinamicamente a lista de OS disponíveis com base na planilha ativa
if not df.empty and 'OS' in df.columns:
    lista_os = sorted(list(df['OS'].dropna().astype(str).unique()))
else:
    lista_os = ["OS-2026-001", "OS-2026-002", "OS-2026-003"]

# Configuração estável do estado da sessão para sincronização de OS
if 'os_selecionada' not in st.session_state or st.session_state.os_selecionada not in lista_os:
    if lista_os:
        st.session_state.os_selecionada = lista_os[0]

# -------------------------------------------------------------------------
# EXTRAÇÃO REATIVA DE VARIÁVEIS COM BASE NA OS SELECIONADA
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
# 4. CRIAÇÃO DAS ABAS NATIVAS REATIVAS (ST.TABS)
# ==========================================
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
    st.info(f"🔗 Módulo BIM Sincronizado | Rastreando Ativo ID: `{id_bim_alvo}` (Selecione outra OS na aba Centro de Diagnóstico para alterar o foco)")
    st.components.v1.iframe(speckle_base_url, height=600, scrolling=False)

# ==========================================
# ABA 2: PRODUTIVIDADE E RELATÓRIO (CÓDIGO ORIGINAL INTEGRAL APROVADO)
# ==========================================
with aba_produtividade:
    if not df.empty:
        df_filtrado = df.copy()
        if filtro_status != "Todos" and 'Status' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
        if filtro_criticidade != "Todos" and 'Criticidade' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Criticidade'] == filtro_criticidade]
            
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
# ABA 3: CENTRO DE DIAGNÓSTICO (CÓDIGO ORIGINAL INTEGRAL APROVADO)
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
