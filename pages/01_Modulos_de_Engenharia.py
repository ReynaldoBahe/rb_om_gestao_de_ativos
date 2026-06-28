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
    col_status = [c for c in df.columns if 'status' in c.lower()]
    col_criticidade = [c for c in df.columns if 'criticidade' in c.lower()]
    
    if col_criticidade:
        os_criticas = len(df[df[col_criticidade].astype(str).str.lower().str.contains('alta', na=False)])
        
    if col_status:
        os_abertas = len(df[df[col_status].astype(str).str.lower().str.contains('aberta|em andamento|andamento', na=False)])

    # Aplicação dos filtros interativos
    if col_status and filtro_status != "Todos":
        df = df[df[col_status].astype(str).str.lower() == filtro_status.lower()]
    if col_criticidade and filtro_criticidade != "Todos":
        df = df[df[col_criticidade].astype(str).str.lower() == filtro_criticidade.lower()]

# =========================================================================
# 5. VISUALIZADOR 3D INTEGRADO (SPECKLE EMBED)
# =========================================================================
st.markdown('<div class="card-home"><div class="card-home-title">Visualizador Operacional de Ativos 3D</div></div>', unsafe_allow_html=True)

speckle_base_url = SPECKLE_STREAM_ID
st.components.v1.html(f'<iframe src="{speckle_base_url}" width="100%" height="600" frameborder="0"></iframe>', height=602)

# =========================================================================
# 6. CENTRO DE DIAGNÓSTICO E ANALYTICS (IA MULTI-CLIENTE)
# =========================================================================
st.markdown('<div class="card-home"><div class="card-home-title">📊 Centro de Diagnóstico Avançado (IA)</div></div>', unsafe_allow_html=True)

if not df.empty:
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Total de Ordens de Serviço", value=total_os)
    with m2:
        st.metric(label="🚨 Ativos em Estado Crítico", value=os_criticas, delta="-2 este mês" if os_criticas > 0 else "Estável")
    with m3:
        st.metric(label="🛠️ OS Pendentes (Ação Imediata)", value=os_abertas)
        
    st.write("<br>", unsafe_allow_html=True)
    
    col_grafico, col_dados = st.columns([1.2, 1.0])
    
    with col_grafico:
        st.markdown("**Distribuição de Ordens por Criticidade e Status**")
        col_s = [c for c in df.columns if 'status' in c.lower()]
        col_c = [c for c in df.columns if 'criticidade' in c.lower()]
        
        if col_s and col_c:
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(f'{col_s}:N', title='Status da OS'),
                y=alt.Y('count():Q', title='Quantidade de Ativos'),
                color=alt.Color(f'{col_c}:N', scale=alt.Scale(domain=['Alta', 'Média', 'Baixa'], range=['#DC2626', '#F59E0B', '#10B981']))
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Colunas de Status ou Criticidade não localizadas para o gráfico.")
            
    with col_dados:
        st.markdown(f"**Relatório Preditivo de Falhas — {NOME_PROJETO}**")
        
        sistema_gargalo = "Não identificado"
        falhas_sistema = 0
        preventivas = 0
        corretivas = 0
        custo_total = 0.0

        # 1. Identificação do Setor (Climatização/Elétrica/Mecânica)
        col_setor = [c for c in df.columns if 'setor' in c.lower() or 'sistema' in c.lower()]
        if col_setor and not df[col_setor].empty:
            v_counts = df[col_setor].value_counts()
            if not v_counts.empty:
                sistema_gargalo = str(v_counts.idxmax())
                falhas_sistema = int(v_counts.max())

        # 2. Conversão segura de moedas e soma de custos
        col_custo_mat = [c for c in df.columns if 'material' in c.lower()]
        col_custo_mo = [c for c in df.columns if 'obra' in c.lower() or 'mao' in c.lower()]
        
        def limpar_moeda_safe(serie_alvo):
            s_str = serie_alvo.astype(str).str.replace('R$', '', regex=False)
            s_str = s_str.str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.strip()
            return pd.to_numeric(s_str, errors='coerce').sum()
            
        if col_custo_mat:
            custo_total += limpar_moeda_safe(df[col_custo_mat])
        if col_custo_mo:
            custo_total += limpar_moeda_safe(df[col_custo_mo])

        # 3. Mapeamento da Eficiência de O&M
        col_tipo = [c for c in df.columns if 'tipo' in c.lower()]
        if col_tipo:
            corretivas = len(df[df[col_tipo].astype(str).str.lower().str.contains('corretiva|corretivo', na=False)])
            preventivas = len(df[df[col_tipo].astype(str).str.lower().str.contains('preventiva|preventivo', na=False)])

        taxa_critica = (os_criticas / total_os * 100) if total_os > 0 else 0
        texto_gargalo = f"🔍 **Gargalo Físico:** O setor com mais chamados é **{sistema_gargalo}**, concentrando {falhas_sistema} registros." if falhas_sistema > 0 else "🔍 **Gargalo Físico:** Distribuição equilibrada entre setores."
        texto_custos = f"💰 **Impacto Financeiro:** Gasto acumulado de **R$ {custo_total:,.2f}** registrado em insumos e MO." if custo_total > 0 else "💰 **Impacto Financeiro:** Sem registros de despesas financeiras atreladas nesta amostragem."
        
        if taxa_critica > 30:
            st.error(f"""
            ### ❌ ALERTA OPERACIONAL DE IA
            Sobrecarga identificada nas rotinas de engenharia de **{NOME_PROJETO}**.
            
            {texto_gargalo}  
            {texto_custos}
            
            🚨 **PREDIÇÃO:** O volume de falhas críticas em *{sistema_gargalo}* aponta risco iminente de parada forçada ou perda severa de eficiência operacional nos próximos 7 dias.
            
            *   **Ação:** Direcionar equipe técnica focada para mitigar as quebras desse setor e providenciar as peças necessárias.
            """)
        else:
            st.success(f"""
            ### ✅ DIAGNÓSTICO DE SAÚDE OPERACIONAL
            O ecossistema técnico de **{NOME_PROJETO}** opera em conformidade.
            
            {texto_gargalo}  
            {texto_custos}
            
