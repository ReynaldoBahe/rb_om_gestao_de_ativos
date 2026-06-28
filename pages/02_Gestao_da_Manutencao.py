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

st.markdown(f'<div class="main-title">🛠️ Gestão da Manutenção (PCM) — {NOME_PROJETO}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Planejamento, Controle e Indicadores de Backlog: {st.session_state.get("user_email")}</div>', unsafe_allow_html=True)

# =========================================================================
# 3. PAINEL DE CONTROLE LATERAL (FILTROS DE PCM)
# =========================================================================
st.sidebar.header("Painel de Controle de PCM")
filtro_tipo_manut = st.sidebar.selectbox("Filtrar por Tipo:", ["Todos", "Preventiva", "Corretiva"])
st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Importar dados/OM operacionais", type=["csv", "xlsx"])

# =========================================================================
# 4. CARREGAMENTO ISOLADO DOS DADOS (PANDAS)
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

# Inicialização padrão das variáveis para evitar quebras visuais
total_om = 0
om_abertas_backlog = 0
taxa_cumprimento_prev = 100.0
df_pcm = df.copy() if not df.empty else pd.DataFrame()

col_status_name = ""
col_tipo_name = ""
col_setor_name = ""
col_abertura_name = ""

if not df.empty:
    # Padronização das colunas
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    # Identificação dinâmica com extração segura do primeiro item da lista
    col_status = [c for c in df.columns if 'status' in c.lower()]
    col_tipo = [c for c in df.columns if 'tipo' in c.lower()]
    col_setor = [c for c in df.columns if 'setor' in c.lower() or 'sistema' in c.lower()]
    col_abertura = [c for c in df.columns if 'abertura' in c.lower() or 'inicio' in c.lower()]
    
    col_status_name = col_status if col_status else ""
    col_tipo_name = col_tipo if col_tipo else ""
    col_setor_name = col_setor if col_setor else ""
    col_abertura_name = col_abertura if col_abertura else ""

    # Aplica filtro interativo por tipo se selecionado na sidebar
    if col_tipo_name and filtro_tipo_manut != "Todos":
        df_pcm = df[df[col_tipo_name].astype(str).str.lower().str.contains(filtro_tipo_manut.lower()[:4], na=False)].copy()
    else:
        df_pcm = df.copy()

    # --- MÉTRICAS DE PCM BLINDADAS ---
    total_om = len(df_pcm)
    
    if col_status_name:
        om_abertas_backlog = len(df_pcm[df_pcm[col_status_name].astype(str).str.lower().str.contains('aberta|em andamento|andamento', na=False)])
    
    if col_tipo_name and col_status_name:
        total_preventivas = len(df_pcm[df_pcm[col_tipo_name].astype(str).str.lower().str.contains('prev', na=False)])
        preventivas_concluidas = len(df_pcm[
            (df_pcm[col_tipo_name].astype(str).str.lower().str.contains('prev', na=False)) & 
            (df_pcm[col_status_name].astype(str).str.lower().str.contains('fechado|concluido|encerrado', na=False))
        ])
        taxa_cumprimento_prev = (preventivas_concluidas / total_preventivas * 100) if total_preventivas > 0 else 100.0

    # --- PROCESSAMENTO TEMPORAL PARA TENDÊNCIA ---
    if col_abertura_name:
        df_pcm['Data_Abertura_Convertida'] = pd.to_datetime(df_pcm[col_abertura_name], errors='coerce')
        # Cria um formato de ordenação string de ano e mês (Ex: 2026-06)
        df_pcm['Mes_Ano'] = df_pcm['Data_Abertura_Convertida'].dt.to_period('M').astype(str)

# =========================================================================
# 5. INTERFACE PRINCIPAL DO PCM
# =========================================================================
st.markdown('<div class="card-home"><div class="card-home-title">📋 Painel de Controle de Ordens e Backlog</div></div>', unsafe_allow_html=True)

if not df_pcm.empty:
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="📋 Volume de Ordens no Escopo", value=total_om)
    with m2:
        st.metric(label="⏳ Backlog Ativo (Ordens Abertas)", value=om_abertas_backlog, delta="Ação Requerida" if om_abertas_backlog > 0 else "Zerado", delta_color="inverse" if om_abertas_backlog > 0 else "normal")
    with m3:
        st.metric(label="🎯 Cumprimento de Preventivas", value=f"{taxa_cumprimento_prev:.1f} %", delta="Conforme" if taxa_cumprimento_prev >= 90 else "Abaixo da Meta", delta_color="normal" if taxa_cumprimento_prev >= 90 else "inverse")

    st.write("<br>", unsafe_allow_html=True)
    col_grafico, col_dados = st.columns([1.2, 1.0])
    
    with col_grafico:
        # INCLUSÃO DA NOVA ABA DE TENDÊNCIA AQUI
        tab_setor, tab_tipo, tab_tendencia = st.tabs(["📊 Carga por Setor", "🔄 Mix de Manutenção", "📈 Tendência Temporal"])
        
        with tab_setor:
            st.markdown("**Ordens de Serviço por Setor Técnico**")
            if col_setor_name and col_status_name:
                chart_setor = alt.Chart(df_pcm).mark_bar().encode(
                    x=alt.X('count():Q', title='Quantidade de Ordens'),
                    y=alt.Y(f'{col_setor_name}:N', title='Setor / Sistema', sort='-x'),
                    color=alt.Color(f'{col_status_name}:N', title='Status')
                ).properties(height=250)
                st.altair_chart(chart_setor, use_container_width=True)
            else:
                st.info("Dados de setor indisponíveis para o gráfico.")
                
        with tab_tipo:
            st.markdown("**Proporção de Atividades no Período (Mix de O&M)**")
            if col_tipo_name:
                chart_mix = alt.Chart(df_pcm).mark_bar(color='#10B981').encode(
                    x=alt.X(f'{col_tipo_name}:N', title='Estratégia Técnico-Operacional'),
                    y=alt.Y('count():Q', title='Volume de Chamados')
                ).properties(height=250)
                st.altair_chart(chart_mix, use_container_width=True)
            else:
                st.info("Dados de estratégia de manutenção indisponíveis.")
                
        with tab_tendencia:
            st.markdown("**Evolução Mensal na Geração de Novas Ordens de Serviço**")
            if col_abertura_name and 'Mes_Ano' in df_pcm.columns:
                # Agrupa a quantidade total de chamados abertos mês a mês
                df_tendencia_pcm = df_pcm.groupby('Mes_Ano').size().reset_index(name='Volume_Ordens')
                
                chart_tendencia_linha = alt.Chart(df_tendencia_pcm).mark_line(color='#1E3A8A', point=True).encode(
                    x=alt.X('Mes_Ano:N', title='Período (Mês/Ano)', sort='x'),
                    y=alt.Y('Volume_Ordens:Q', title='Novos Chamados Registrados'),
                    tooltip=['Mes_Ano', 'Volume_Ordens']
                ).properties(height=250)
                st.altair_chart(chart_tendencia_linha, use_container_width=True)
            else:
                st.info("Datas de abertura indisponíveis para traçar a linha de tendência histórica.")
            
    with col_dados:
        st.markdown(f"**Parecer da IA sobre o Plano de PCM — {NOME_PROJETO}**")
        
        sistema_gargalo = "Não identificado"
        if col_setor_name and not df_pcm[col_setor_name].empty:
            v_counts = df_pcm[col_setor_name].value_counts()
            if not v_counts.empty:
                sistema_gargalo = str(v_counts.idxmax())

        if taxa_cumprimento_prev < 90.0:
            st.error(f"""
            ### ❌ ALERTA DE FLUXO DE PCM
            Plano de manutenção preventiva comprometido em **{NOME_PROJETO}**.
            
            *   **Diagnóstico:** A taxa de execução de preventivas está em **{taxa_cumprimento_prev:.1f}%**, ficando abaixo da meta regulatória (Meta >= 90%). 
