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
        "nome_exibicao": "Resort Boa Viagem - Complexo Hoteleiro",
        "arquivo_cmms": "CMMS_Export_RB - CMMS_RB.csv"
    },
    "Hospital Central": {
        "nome_exibicao": "Hospital Central - Centro Médico Operacional",
        "arquivo_cmms": "CMMS_Export_Hospital.csv - CMMS_RB.csv"
    }
}

if cliente_logado in EMPREENDIMENTOS:
    config = EMPREENDIMENTOS[cliente_logado]
    NOME_PROJETO = config["nome_exibicao"]
    CAMINHO_CSV = config["arquivo_cmms"]
else:
    st.warning(f"⚠️ {cliente_logado}, os dados estão em processamento.")
    st.stop()

# =========================================================================
# 2. DESIGN E TITULOS
# =========================================================================
st.markdown(f"## 🛠️ Gestão da Manutenção (PCM) — {NOME_PROJETO}")
st.markdown(f"**Sessão segura:** {st.session_state.get('user_email')}")

# =========================================================================
# 3. PAINEL DE CONTROLE LATERAL
# =========================================================================
st.sidebar.header("Painel de Controle de PCM")
filtro_tipo_manut = st.sidebar.selectbox("Filtrar por Tipo:", ["Todos", "Preventiva", "Corretiva"])
st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Importar dados/OM operacionais", type=["csv", "xlsx"])

# =========================================================================
# 4. CARREGAMENTO DOS DADOS
# =========================================================================
if arquivo_upload is not None:
    try:
        df = pd.read_csv(arquivo_upload) if arquivo_upload.name.endswith('.csv') else pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro ao ler arquivo enviado: {e}")
        df = pd.read_csv(CAMINHO_CSV)
else:
    try:
        df = pd.read_csv(CAMINHO_CSV)
    except Exception:
        df = pd.DataFrame()

# =========================================================================
# 5. PROCESSAMENTO E INDICADORES
# =========================================================================
if not df.empty:
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    col_status = [c for c in df.columns if 'status' in c.lower()]
    col_tipo = [c for c in df.columns if 'tipo' in c.lower()]
    col_setor = [c for c in df.columns if 'setor' in c.lower() or 'sistema' in c.lower()]
    col_abertura = [c for c in df.columns if 'abertura' in c.lower() or 'inicio' in c.lower()]
    
    c_status = col_status[0] if col_status else ""
    c_tipo = col_tipo[0] if col_tipo else ""
    c_setor = col_setor[0] if col_setor else ""
    c_abertura = col_abertura[0] if col_abertura else ""

    # Aplica filtros básicos
    df_pcm = df.copy()
    if c_tipo and filtro_tipo_manut != "Todos":
        df_pcm = df[df[c_tipo].astype(str).str.lower().str.contains(filtro_tipo_manut.lower()[:4], na=False)].copy()

    # Contagens básicas
    total_om = len(df_pcm)
    om_abertas = 0
    if c_status:
        om_abertas = len(df_pcm[df_pcm[c_status].astype(str).str.lower().str.contains('aberta|em andamento|andamento', na=False)])

    # Cartões de Métricas
    m1, m2 = st.columns(2)
    with m1:
        st.metric(label="📋 Volume de Ordens", value=total_om)
    with m2:
        st.metric(label="⏳ Backlog Ativo (Ordens Abertas)", value=om_abertas)

    st.write("---")
    
    # Abas visuais de gráficos
    tab_setor, tab_tendencia = st.tabs(["📊 Carga por Ativo", "📈 Linha de Tendência"])
    
    with tab_setor:
        if c_setor and c_status:
            chart = alt.Chart(df_pcm).mark_bar().encode(
                x=alt.X('count():Q', title='Quantidade de Ordens'),
                y=alt.Y(f'{c_setor}:N', title='Setor / Sistema', sort='-x'),
                color=alt.Color(f'{c_status}:N', title='Status')
            ).properties(height=250)
            st.altair_chart(chart, use_container_width=True)
            
    with tab_tendencia:
        if c_abertura:
            df_pcm['Data_Conv'] = pd.to_datetime(df_pcm[c_abertura], errors='coerce')
            df_pcm['Mes_Ano'] = df_pcm['Data_Conv'].dt.to_period('M').astype(str)
            df_trend = df_pcm.groupby('Mes_Ano').size().reset_index(name='Volume')
            
            chart_line = alt.Chart(df_trend).mark_line(color='#1E3A8A', point=True).encode(
                x=alt.X('Mes_Ano:N', title='Mês/Ano', sort='x'),
                y=alt.Y('Volume:Q', title='Novas Ordens'),
                tooltip=['Mes_Ano', 'Volume']
            ).properties(height=250)
            st.altair_chart(chart_line, use_container_width=True)

    # Exibição da tabela final
    st.write("---")
    st.markdown("### Quadro de Ordens Filtrado")
    st.dataframe(df_pcm, use_container_width=True)
else:
    st.info("Nenhum dado cadastrado para exibição.")
