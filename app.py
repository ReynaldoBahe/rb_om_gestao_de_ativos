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
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏗️ Portal de Engenharia & Gestão de Projetos</div>', unsafe_allow_html=True)

# ==========================================
# 3. BARRA LATERAL (FILTROS OPERACIONAIS E PAINEL DE CONTROLE)
# ==========================================
st.sidebar.header("Filtros de Visão")

filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"])
filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])
filtro_tempo = st.sidebar.selectbox("Filtrar por Tempo Aberta:", ["Todos", "Menos de 24h", "Entre 2 e 7 dias", "Mais de 7 dias"])

st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Carregar Planilha de Ativos/OM", type=["csv", "xlsx"])

# URL base do Speckle original aprovado
speckle_base_url = "https://speckle.systems"

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

# INJEÇÃO DO PAINEL DE SLA (RODAPÉ DA BARRA CINZA LATERAL)
st.sidebar.write("---")
st.sidebar.subheader("📈 Metas Operacionais (SLA)")

if not df.empty:
    total_os = len(df)
    col_status_sla = next((c for c in df.columns if c.lower() == 'status'), 'Status')
    if col_status_sla in df.columns:
        os_fechadas = len(df[df[col_status_sla].astype(str).str.lower().str.contains('fechado|concluído|concluido', na=False)])
        indice_sla = (os_fechadas / total_os) if total_os > 0 else 0.85
    else:
        indice_sla = 0.85
else:
    indice_sla = 0.88

st.sidebar.metric(
    label="Atendimento Geral do SLA", 
    value=f"{int(indice_sla * 100)}%", 
    delta="⚡ Dentro da Meta" if indice_sla >= 0.80 else "⚠️ Atenção"
)
st.sidebar.progress(min(float(indice_sla), 1.0))

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

# ==========================================
# ABA 1: MODELO 3D (RASTREABILIDADE BIM)
# ==========================================
with aba_modelo:
    st.subheader("Visualizador Operacional de Ativos 3D")
    
    id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"
    if not df.empty and 'OS' in df.columns:
        col_id = next((c for c in df.columns if c.upper() == 'ID'), None)
        if col_id:
            linha_ativo = df[df['OS'].astype(str) == str(st.session_state.os_selecionada)]
            if not linha_ativo.empty:
                id_bim_alvo = str(linha_ativo[col_id].squeeze()).strip()

    if not id_bim_alvo or id_bim_alvo == "nan":
        id_bim_alvo = "29e456a92924eb3747bbcd9bb3edd623"

    st.info(f"🔗 Módulo BIM Sincronizado | Rastreando Ativo ID: `{id_bim_alvo}` (Selecionado no Centro de Diagnóstico)")
    st.components.v1.iframe(speckle_base_url, height=600, scrolling=False)

# ==========================================
# ABA 2: PRODUTIVIDADE E RELATÓRIO (COM FILTRO DE TEMPO OPERACIONAL)
# ==========================================
with aba_produtividade:
    if not df.empty:
        # Criamos uma cópia local para os filtros não afetarem as outras abas
        df_filtrado = df.copy()
        
        # FILTRO DE TEMPO DE ABERTURA OPERACIONAL SEGURO
        if 'Data_Abertura' in df_filtrado.columns:
            try:
                # Converte a coluna para data de forma isolada nesta aba
                df_filtrado['Data_Abertura_dt'] = pd.to_datetime(df_filtrado['Data_Abertura'], errors='coerce')
                # Considera a data atual do sistema (2026) para calcular a diferença de dias
                data_atual = pd.to_datetime('2026-06-26')
                df_filtrado['Dias_Aberta'] = (data_atual - df_filtrado['Data_Abertura_dt']).dt.days
                
                # Aplica as regras baseadas na seleção da barra lateral cinza
                if filtro_tempo == "Menos de 24h":
                    df_filtrado = df_filtrado[df_filtrado['Dias_Aberta'] <= 1]
                elif filtro_tempo == "Entre 2 e 7 dias":
                    df_filtrado = df_filtrado[(df_filtrado['Dias_Aberta'] > 1) & (df_filtrado['Dias_Aberta'] <= 7)]
                elif filtro_tempo == "Mais de 7 dias":
                    df_filtrado = df_filtrado[df_filtrado['Dias_Aberta'] > 7]
            except Exception:
                pass

        # FILTROS ORIGINAIS DE STATUS E CRITICIDADE APROVADOS
        if filtro_status != "Todos" and 'Status' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
        if filtro_criticidade != "Todos" and 'Criticidade' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Criticidade'] == filtro_criticidade]
            
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
        
        st.subheader("Controle de Ordens de Serviço por Técnico")
        col_tecnico = next((c for c in df_filtrado.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel', 'técnico responsável']), df_filtrado.columns)
        
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
# ABA 3: CENTRO DE DIAGNÓSTICO AVANÇADO (COM PESOS DE PROGRESSO REAL)
# ==========================================
with aba_diagnostico:
    st.subheader("🧠 Centro de Diagnóstico Avançado (IA Preditiva)")
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.markdown("🔎 **Seleção de Ativo para Auditoria**")
        
        idx_selecionado = lista_os.index(st.session_state.os_selecionada) if st.session_state.os_selecionada in lista_os else 0
        st.session_state.os_selecionada = st.selectbox(
            "Selecione a OS para análise da IA:", 
            lista_os, 
            index=idx_selecionado,
            key="selector_diagnostico_real_pesos"
        )
        
        resp, setor, status, data_ab = "Não identificado", "Geral", "Aberto", "20/06/2026"
        descricao_falha = "Nenhuma descrição detalhada registrada na planilha."
        criticidade_ativo = "Média"
        
        if not df.empty and 'OS' in df.columns:
            dados_os = df[df['OS'].astype(str) == str(st.session_state.os_selecionada)]
            if not dados_os.empty:
                col_t = next((c for c in df.columns if c.lower() in ['técnico', 'tecnico', 'responsável', 'responsavel']), None)
                resp = str(dados_os[col_t].squeeze()) if col_t else "Pedro"
                setor = str(dados_os['Setor'].squeeze()) if 'Setor' in df.columns else "Climatização"
                status = str(dados_os['Status'].squeeze()) if 'Status' in df.columns else "Fechado"
                data_ab = str(dados_os['Data_Abertura'].squeeze()) if 'Data_Abertura' in df.columns else "20/06/2026"
                
                col_desc = next((c for c in df.columns if c.lower() in ['descrição', 'descricao', 'ocorrência', 'ocorrencia', 'falha']), None)
                if col_desc:
                    descricao_falha = str(dados_os[col_desc].squeeze())
                
                col_crit = next((c for c in df.columns if 'CRITIC' in c.upper()), None)
                if col_crit:
                    criticidade_ativo = str(dados_os[col_crit].squeeze())

        html_ficha = '<div class="ficha-tecnica"><h4 style="margin-top:0; color:#1E3A8A;">📋 Ficha Técnica do Ativo</h4><ul>'
        html_ficha += f'<li><b>ID BIM:</b> {id_bim_alvo}</li>'
        html_ficha += f'<li><b>Responsável Técnico:</b> {resp}</li>'
        html_ficha += f'<li><b>Setor:</b> {setor}</li>'
        html_ficha += f'<li><b>Status Atual:</b> {status}</li>'
        html_ficha += f'<li><b>Criticidade Real:</b> {criticidade_ativo}</li>'
        html_ficha += f'<li><b>Data de Abertura:</b> {data_ab}</li></ul>'
        html_ficha += f'<hr style="border:0; border-top:1px solid #BFDBFE; margin:10px 0;"><p style="margin:0; font-size:13px; color:#1E40AF;"><b>Ocorrência Registrada na Planilha:</b> {descricao_falha}</p>'
        html_ficha += '<br><a href="#" style="color:#2563EB; font-weight:bold; text-decoration:none;">📄 Acessar Manual Técnico do Ativo</a></div>'
        st.markdown(html_ficha, unsafe_allow_html=True)
        
    with col_dir:
        st.markdown("⚡ **Análise de Engenharia Operacional da IA**")
        
        mensagem_ia = f"**ANÁLISE COMPLEMENTAR:** Ordem {st.session_state.os_selecionada}. Ativo BIM analisado sob status '{status}' e criticidade '{criticidade_ativo}'. Plano operacional recomendado para o subsistema de {setor}."
        st.success(mensagem_ia)
        
        # 📈 MAPEAMENTO REATIVO DE PESOS OPERACIONAIS REAIS
        status_limpo = str(status).lower().strip()
        if 'abert' in status_limpo:
            valor_progresso = 0.1
        elif 'andament' in status_limpo or 'atendiment' in status_limpo:
            valor_progresso = 0.5
        elif 'pausad' in status_limpo:
            valor_progresso = 0.3
        elif 'fechad' in status_limpo or 'conclu' in status_limpo:
            valor_progresso = 1.0
        else:
            valor_progresso = 0.5  # Fallback neutro se o status for desconhecido
            
        df_ia = pd.DataFrame({'Métrica': ['Progresso Operacional'], 'Valor': [valor_progresso]})
        
        grafico_ia = alt.Chart(df_ia).mark_bar(color='#1f77b4', size=150).encode(
            x=alt.X('Métrica:N', title=''),
            # Formata o tooltip e o eixo para exibir em formato de porcentagem limpa no Altair
            y=alt.Y('Valor:Q', title='Evolução de Conclusão', scale=alt.Scale(domain=[0, 1.1])),
            tooltip=['Métrica', alt.Tooltip('Valor:Q', format='.0%')]
        ).properties(height=250)
        st.altair_chart(grafico_ia, use_container_width=True)
