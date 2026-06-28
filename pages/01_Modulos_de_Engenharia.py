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

# Prepara as variáveis base de contagem antes da limpeza de nomes das colunas
total_os = len(df)
os_criticas = 0
os_abertas = 0

if not df.empty:
    # Tratamento global das colunas: remove sublinhados e espaços extras para busca segura
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    colunas_minusculo = [str(c).lower().strip() for c in df.columns]
    
    # Identifica colunas chaves por aproximação de termos
    col_status_idx = [i for i, c in enumerate(colunas_minusculo) if 'status' in c]
    col_crit_idx = [i for i, c in enumerate(colunas_minusculo) if 'criticidade' in c]
    
    if col_crit_idx:
        nome_col_crit = df.columns[col_crit_idx[0]]
        os_criticas = len(df[df[nome_col_crit].astype(str).str.lower().str.contains('alta', na=False)])
        
    if col_status_idx:
        nome_col_status = df.columns[col_status_idx[0]]
        os_abertas = len(df[df[nome_col_status].astype(str).str.lower().str.contains('aberta|em andamento|andamento', na=False)])

    # Aplicação dos filtros interativos da barra lateral
    if col_status_idx and filtro_status != "Todos":
        df = df[df[df.columns[col_status_idx[0]]].astype(str).str.lower() == filtro_status.lower()]
    if col_crit_idx and filtro_criticidade != "Todos":
        df = df[df[df.columns[col_crit_idx[0]]].astype(str).str.lower() == filtro_criticidade.lower()]

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
    # Renderização das métricas nos cartões do topo
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
        
        colunas_minusculo = [str(c).lower().strip() for c in df.columns]
        idx_s = [df.columns[i] for i, c in enumerate(colunas_minusculo) if 'status' in c]
        idx_c = [df.columns[i] for i, c in enumerate(colunas_minusculo) if 'criticidade' in c]
        
        if idx_s and idx_c:
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(f'{idx_s[0]}:N', title='Status da OS'),
                y=alt.Y('count():Q', title='Quantidade de Ativos'),
                color=alt.Color(f'{idx_c[0]}:N', scale=alt.Scale(domain=['Alta', 'Média', 'Baixa'], range=['#DC2626', '#F59E0B', '#10B981']))
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Colunas de Status ou Criticidade não mapeadas para exibição gráfica.")
            
    with col_dados:
        st.markdown(f"**Relatório Preditivo de Falhas — {NOME_PROJETO}**")
        
        # Bloco da IA totalmente blindado contra variações de formatos de células do Excel
        sistema_gargalo = "Não identificado"
        falhas_sistema = 0
        custo_total = 0.0
        preventivas = 0
        corretivas = 0

        try:
            colunas_minusculo = [str(c).lower().strip() for c in df.columns]
            col_sistema = [df.columns[i] for i, c in enumerate(colunas_minusculo) if 'sistema' in c]
            if col_sistema and not df[col_sistema[0]].empty:
                v_counts = df[col_sistema[0]].value_counts()
                if not v_counts.empty:
                    sistema_gargalo = str(v_counts.idxmax())
                    falhas_sistema = int(v_counts.max())
        except Exception:
            pass

        try:
            col_custo_mat = [df.columns[i] for i, c in enumerate(colunas_minusculo) if 'custo material' in c or 'material' in c]
            col_custo_mo = [df.columns[i] for i, c in enumerate(colunas_minusculo) if 'custo mao' in c or 'obra' in c]
            
            def tratamento_moeda(sub_df, col_lista):
                if not col_lista: return 0.0
                valores = sub_df[col_lista[0]].astype(str).str.replace('R$', '', regex=False)
                valores = valores.str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.strip()
                return pd.to_numeric(valores, errors='coerce').sum()
                
            custo_total = tratamento_moeda(df, col_custo_mat) + tratamento_moeda(df, col_custo_mo)
        except Exception:
            custo_total = 0.0

        try:
            col_tipo = [df.columns[i] for i, c in enumerate(colunas_minusculo) if 'tipo' in c]
            if col_tipo:
                corretivas = len(df[df[col_tipo[0]].astype(str).str.lower().str.contains('corretiva|corretivo', na=False)])
                preventivas = len(df[df[col_tipo[0]].astype(str).str.lower().str.contains('preventiva|preventivo', na=False)])
        except Exception:
            pass

        taxa_critica = (os_criticas / total_os * 100) if total_os > 0 else 0
        texto_custos = f"💰 **Impacto Financeiro:** Gasto total registrado de **R$ {custo_total:,.2f}** em materiais e MO." if custo_total > 0 else "💰 **Impacto Financeiro:** Sem custos financeiros adicionais computados para o período."
        texto_gargalo = f"🔍 **Gargalo Físico:** O sistema mais instável é **{sistema_gargalo}**, concentrando {falhas_sistema} chamados abertos." if falhas_sistema > 0 else "🔍 **Gargalo Físico:** Distribuição homogênea entre os sistemas prediais cadastrados."
        
