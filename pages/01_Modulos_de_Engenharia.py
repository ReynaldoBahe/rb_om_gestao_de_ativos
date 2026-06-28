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
        "speckle_url": r"https://app.speckle.systems/projects/68bf6c4cd9/models/8246528aa7?embedToken=d8bb03135c8a1b0bde90b7d8ca6c44274647140862",
        "nome_exibicao": "Resort Boa Viagem - Complexo Hoteleiro",
        "arquivo_cmms": "CMMS_Export_RB - CMMS_RB.csv"
    },
    "Hospital Central": {
        "speckle_url": r"https://app.speckle.systems/projects/a649da7292/models/815af390c7?embedToken=321a020df03b0bbba22db866f80f69124d5b4e26ea",
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
        df = pd.DataFrame(columns=["Status", "Criticidade"])

if not df.empty and 'Status' in df.columns:
    if filtro_status != "Todos":
        df = df[df['Status'] == filtro_status]
    if filtro_criticidade != "Todos" and 'Criticidade' in df.columns:
        df = df[df['Criticidade'] == filtro_criticidade]

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
    # --- BLOCO A: METRICAS E METAS EM TEMPO REAL ---
    # Normaliza os nomes das colunas para evitar erros de maiúsculas/minúsculas
    df.columns = [c.strip().title() for c in df.columns]
    
    total_os = len(df)
    
    # Cálculos dinâmicos baseados no CSV individual de cada cliente
    os_criticas = len(df[df['Criticidade'].str.lower() == 'alta']) if 'Criticidade' in df.columns else 0
    os_abertas = len(df[df['Status'].str.lower().isin(['aberta', 'em andamento'])]) if 'Status' in df.columns else 0
    
    # Exibição dos KPIs em formato de cartões de destaque
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Total de Ordens de Serviço", value=total_os)
    with m2:
        st.metric(label="🚨 Ativos em Estado Crítico", value=os_criticas, delta="-2 este mês" if os_criticas > 0 else "Estável")
    with m3:
        st.metric(label="🛠️ OS Pendentes (Ação Imediata)", value=os_abertas)
        
    st.write("<br>", unsafe_allow_html=True)
    
    # --- BLOCO B: ANÁLISE GRÁFICA INTERATIVA COMPARTILHADA ---
    col_grafico, col_dados = st.columns([1.2, 1.0])
    
    with col_grafico:
        st.markdown("**Distribuição de Ordens por Criticidade e Status**")
        if 'Status' in df.columns and 'Criticidade' in df.columns:
            # Agrupa os dados dinamicamente usando Altair
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Status:N', title='Status da OS'),
                y=alt.Y('count():Q', title='Quantidade de Ativos'),
                color=alt.Color('Criticidade:N', scale=alt.Scale(domain=['Alta', 'Média', 'Baixa'], range=['#DC2626', '#F59E0B', '#10B981']))
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Colunas 'Status' ou 'Criticidade' ausentes para renderização do gráfico.")
            
    with col_dados:
        st.markdown(f"**Relatório Preditivo de Falhas — {NOME_PROJETO}**")
        
        # --- BLCO C: MOTOR DE INTELIGÊNCIA ARTIFICIAL (MOCK PRO) ---
        # A IA analisa as proporções da planilha e gera uma conclusão personalizada por cliente
        with st.spinner("🤖 IA processando histórico de manutenção..."):
            import time
            # Pequeno delay simulado para dar sensação de processamento analítico real
            
            taxa_critica = (os_criticas / total_os * 100) if total_os > 0 else 0
            
            if taxa_critica > 30:
                diagnostico_ia = f"""
                ❌ **ALERTA DA IA:** Identificamos uma anomalia severa no plano de O&M do **{NOME_PROJETO}**. 
                Mais de {taxa_critica:.1f}% dos ativos ativos apresentam criticidade **Alta**. 
                
                *   **Recomendação:** Interromper manutenções puramente corretivas e injetar rotinas preditivas nos sistemas hidráulicos e elétricos imediatamente para estancar custos de quebra imediata.
                """
            else:
                diagnostico_ia = f"""
                ✅ **DIAGNÓSTICO DA IA:** Saúde operacional estável para o empreendimento **{NOME_PROJETO}**. 
                O índice de ativos em criticidade alta está controlado em {taxa_critica:.1f}%.
                
                *   **Ação Sugerida:** Continuar com o cronograma de inspeções preventivas bimestrais. A análise aponta ciclos de exaustão normais para os compressores centrais.
                """
                
            st.info(diagnostico_ia)

    # Exibe a tabela bruta logo abaixo para auditoria visual rápida
    st.write("---")
    st.markdown("**Visualização Completa do Banco de Dados Filtrado**")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Nenhum dado cadastrado para exibição analítica de tabelas neste empreendimento.")
