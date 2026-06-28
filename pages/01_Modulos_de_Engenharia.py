import streamlit as st
import pandas as pd
import altair as alt

# =========================================================================
# 1. BARREIRA DE SEGURANÇA E MAPEAMENTO MULTI-CLIENTE
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, realize o login primeiro.")
    st.stop()

cliente_logado = st.session_state.get("cliente_ativo", "Nenhum")

EMPREENDIMENTOS = {
    "Resort Boa Viagem": {
        "speckle_url": r"https://speckle.systems",
        "nome_exibicao": "Resort Boa Viagem - Complexo Hoteleiro",
        "arquivo_cmms": "CMMS_Export_RB - CMMS_RB.csv"
    },
    "Hospital Central": {
        "speckle_url": r"https://speckle.systems",
        "nome_exibicao": "Hospital Central - Centro Médico Operacional",
        "arquivo_cmms": "CMMS_Export_Hospital.csv - CMMS_RB.csv"
    }
}

if cliente_logado in EMPREENDIMENTOS:
    config = EMPREENDIMENTOS[cliente_logado]
    SPECKLE_STREAM_ID = config["speckle_url"]
    NOME_PROJETO = config["nome_exibicao"]
    CAMINHO_CSV = config["arquivo_cmms"]
else:
    st.warning(f"⚠️ {cliente_logado}, os dados do seu empreendimento estão em processamento.")
    st.stop()

# =========================================================================
# 2. DESIGN E ESTILIZAÇÃO CUSTOMIZADA (CSS)
# =========================================================================
st.markdown("""
    <style>
        .main-title { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
        .sub-title { font-size: 14px; color: #4B5563; margin-bottom: 20px; }
        .card-home { background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 15px; }
        .card-home-title { font-size: 16px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="main-title">🏗️ Módulos de Engenharia — {NOME_PROJETO}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Sessão operacional segura: {st.session_state.get("user_email")}</div>', unsafe_allow_html=True)

# =========================================================================
# 3. PAINEL DE CONTROLE LATERAL (FILTROS)
# =========================================================================
st.sidebar.header("Painel de controle")

filtro_status = st.sidebar.selectbox("Filtrar por Status:", ["Todos", "Aberta", "Em Andamento", "Pausada", "Fechado"])
filtro_criticidade = st.sidebar.selectbox("Filtrar por Criticidade:", ["Todos", "Alta", "Média", "Baixa"])

st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Importar dados/OM", type=["csv", "xlsx"])

# =========================================================================
# 4. CARREGAMENTO ISOLADO DOS DADOS (PANDAS)
# =========================================================================
if arquivo_upload is not None:
    try:
        if arquivo_upload.name.endswith('.csv'):
            df = pd.read_csv(arquivo_upload)
        else:
            df = pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao ler arquivo enviado: {e}")
        df = pd.read_csv(CAMINHO_CSV)
else:
    try:
        df = pd.read_csv(CAMINHO_CSV)
    except Exception:
        df = pd.DataFrame()

# Prepara as variáveis base de contagem
total_os = len(df)
os_criticas = 0
os_abertas = 0

if not df.empty:
    # Padronização limpa das colunas substituindo sublinhados por espaços
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    # Encontra os nomes exatos das colunas chaves de forma segura
    col_status_list = [c for c in df.columns if 'status' in c.lower()]
    col_criticidade_list = [c for c in df.columns if 'criticidade' in c.lower()]
    
    if col_criticidade_list:
        os_criticas = len(df[df[col_criticidade_list[0]].astype(str).str.lower().str.contains('alta', na=False)])
        
    if col_status_list:
        os_abertas = len(df[df[col_status_list[0]].astype(str).str.lower().str.contains('aberta|em andamento|andamento', na=False)])

    # Aplicação dos filtros interativos padrão da sidebar
    if col_status_list and filtro_status != "Todos":
        df = df[df[col_status_list[0]].astype(str).str.lower() == filtro_status.lower()]
    if col_criticidade_list and filtro_criticidade != "Todos":
        df = df[df[col_criticidade_list[0]].astype(str).str.lower() == filtro_criticidade.lower()]

# =========================================================================
# 5. VISUALIZADOR 3D INTEGRADO (SPECKLE EMBED)
# =========================================================================
st.markdown('<div class="card-home"><div class="card-home-title">Visualizador Operacional de Ativos 3D</div></div>', unsafe_allow_html=True)

speckle_base_url = SPECKLE_STREAM_ID
st.components.v1.html(f'<iframe src="{speckle_base_url}" width="100%" height="600" frameborder="0"></iframe>', height=602)

# =========================================================================
# 6. CENTRO DE DIAGNÓSTICO E ANALYTICS (IA MULTI-CLIENTE & FINANCEIRO)
# =========================================================================
if not df.empty:
    # Garante a busca exata pela coluna 'Os' para o seletor na sidebar
    col_id_os = [c for c in df.columns if c.lower() == 'os']
    if not col_id_os:
        col_id_os = [c for c in df.columns if 'os' in c.lower() or 'numero' in c.lower()]
    
    st.sidebar.write("---")
    st.sidebar.markdown("### 🎯 Foco da Análise (IA)")
    opcoes_os = ["Todas as Ordens (Análise Geral)"]
    
    if col_id_os:
        opcoes_os.extend(df[col_id_os[0]].dropna().astype(str).unique().tolist())
    
    os_selecionada = st.sidebar.selectbox("Selecione uma OS específica para auditoria:", opcoes_os)
    
    # Aplica o filtro de OS selecionada antes de calcular as métricas da IA
    df_analise = df.copy()
    analise_individual = False
    
    if os_selecionada != "Todas as Ordens (Análise Geral)" and col_id_os:
        df_analise = df[df[col_id_os[0]].astype(str) == os_selecionada]
        analise_individual = True

    # --- RECALCULA MÉTRICAS DINÂMICAS BASEADAS NA VISÃO DA IA ---
    total_os = len(df_analise)
    os_criticas = 0
    os_abertas = 0

    col_status = [c for c in df_analise.columns if 'status' in c.lower()]
    col_criticidade = [c for c in df_analise.columns if 'criticidade' in c.lower()]
    col_descricao_ativo = [c for c in df_analise.columns if 'desc' in c.lower() or 'ativo' in c.lower() or 'equip' in c.lower()]
    
    if col_criticidade:
        os_criticas = len(df_analise[df_analise[col_criticidade[0]].astype(str).str.lower().str.contains('alta', na=False)])
        
    if col_status:
        os_abertas = len(df_analise[df_analise[col_status[0]].astype(str).str.lower().str.contains('aberta|em andamento|andamento', na=False)])

    # Adiciona coluna de custos somados e limpos no dataframe de análise
    col_custo_mat = [c for c in df_analise.columns if 'material' in c.lower()]
    col_custo_mo = [c for c in df_analise.columns if 'obra' in c.lower() or 'mao' in c.lower()]
    df_analise['Custo_Total_Calculado'] = 0.0
    
    def limpar_coluna_moeda(series_ref):
        s_str = series_ref.astype(str).str.replace('R$', '', regex=False)
        s_str = s_str.str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.strip()
        return pd.to_numeric(s_str, errors='coerce').fillna(0.0)

    if col_custo_mat:
        df_analise['Custo_Total_Calculado'] += limpar_coluna_moeda(df_analise[col_custo_mat[0]])
    if col_custo_mo:
        df_analise['Custo_Total_Calculado'] += limpar_coluna_moeda(df_analise[col_custo_mo[0]])

# 6.2. INTERFACE PRINCIPAL DO CENTRO DE DIAGNÓSTICO
st.markdown('<div class="card-home"><div class="card-home-title">📊 Centro de Diagnóstico Avançado (IA & Custos)</div></div>', unsafe_allow_html=True)

if not df.empty:
    # Renderização dos cartões numéricos desafogados e limpos
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Total de Ordens de Serviço", value=total_os)
    with m2:
        if analise_individual and col_criticidade:
            criticidade_atual = str(df_analise[col_criticidade[0]].iloc[0])
            st.metric(label="🚨 Grau de Criticidade", value=criticidade_atual)
        else:
            st.metric(label="🚨 Ativos em Estado Crítico", value=os_criticas, delta="-2 este mês" if os_criticas > 0 else "Estável")
    with m3:
        if analise_individual and col_status:
            status_atual = str(df_analise[col_status[0]].iloc[0])
            st.metric(label="🛠️ Status Atual", value=status_atual)
        else:
            st.metric(label="🛠️ OS Pendentes (Ação Imediata)", value=os_abertas)
        
    st.write("<br>", unsafe_allow_html=True)
    
    col_grafico, col_dados = st.columns([1.2, 1.0])
    
    with col_grafico:
        # Cria abas para acomodar a Visão de Manutenção e a Visão Financeira lado a lado
        tab_operacional, tab_financeira = st.tabs(["📊 Visão Operacional", "💰 Visão Financeira"])
        
        with tab_operacional:
            st.markdown("**Distribuição de Ordens por Criticidade e Status**")
            if col_status and col_criticidade:
                chart = alt.Chart(df_analise).mark_bar().encode(
                    x=alt.X(f'{col_status[0]}:N', title='Status da OS'),
                    y=alt.Y('count():Q', title='Quantidade de Ativos'),
                    color=alt.Color(f'{col_criticidade[0]}:N', scale=alt.Scale(domain=['Alta', 'Média', 'Baixa'], range=['#DC2626', '#F59E0B', '#10B981']))
                ).properties(height=250)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Colunas de Status ou Criticidade não localizadas.")
                
        with tab_financeira:
            if col_descricao_ativo:
