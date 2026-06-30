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

# NOVA CONDICIONAL: Se for ADMIN, ele ganha uma visão geral padrão (ex: Resort Boa Viagem)
if cliente_logado == "ADMIN":
    config = EMPREENDIMENTOS["Resort Boa Viagem"] # Defina qual projeto o Admin vê por padrão
    NOME_PROJETO = f"Visão Geral Administrador ({config['nome_exibicao']})"
    CAMINHO_CSV = config["arquivo_cmms"]

elif cliente_logado in EMPREENDIMENTOS:
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

st.markdown(f'<div class="main-title">⏱️ Indicadores de Tempo — {NOME_PROJETO}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Análise de Confiabilidade e Disponibilidade: {st.session_state.get("user_email")}</div>', unsafe_allow_html=True)

# =========================================================================
# 3. PAINEL DE CONTROLE LATERAL
# =========================================================================
st.sidebar.header("Painel de Controle de Tempo")
filtro_setor = st.sidebar.selectbox("Filtrar por Sistema/Setor:", ["Todos", "Mecânica", "Elétrica", "Climatização", "Civil"])
st.sidebar.write("---")
arquivo_upload = st.sidebar.file_uploader("📂 Importar dados/OM temporais", type=["csv", "xlsx"])

# =========================================================================
# 4. CARREGAMENTO E PARSING SEGURO DE DATAS
# =========================================================================
if arquivo_upload is not None:
    try:
        df = pd.read_csv(arquivo_upload) if arquivo_upload.name.endswith('.csv') else pd.read_excel(arquivo_upload)
    except Exception as e:
        st.error(f"Erro no arquivo enviado: {e}")
        df = pd.read_csv(CAMINHO_CSV)
else:
    try:
        df = pd.read_csv(CAMINHO_CSV)
    except Exception:
        df = pd.DataFrame()

# Variáveis globais de confiabilidade prontas caso a planilha esteja vazia
mtbf_geral = 0.0
mttr_geral = 0.0
disponibilidade_geral = 100.0

if not df.empty:
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    # Identifica dinamicamente colunas de tempo, setor e tipo
    col_abertura = [c for c in df.columns if 'abertura' in c.lower() or 'inicio' in c.lower()]
    col_fechamento = [c for c in df.columns if 'fechamento' in c.lower() or 'fim' in c.lower() or 'conclusao' in c.lower()]
    col_setor = [c for c in df.columns if 'setor' in c.lower() or 'sistema' in c.lower()]
    col_tipo = [c for c in df.columns if 'tipo' in c.lower()]
    col_descricao_ativo = [c for c in df.columns if 'desc' in c.lower() or 'ativo' in c.lower() or 'equip' in c.lower()]

    # Aplica filtro por setor se o usuário interagir na barra lateral
    if col_setor and filtro_setor != "Todos":
        df = df[df[col_setor[0]].astype(str).str.lower() == filtro_setor.lower()]

    # Conversão e cálculo do tempo se as colunas de data existirem
    if col_abertura and col_fechamento:
        df[col_abertura[0]] = pd.to_datetime(df[col_abertura[0]], errors='coerce')
        df[col_fechamento[0]] = pd.to_datetime(df[col_fechamento[0]], errors='coerce')
        
        # Calcula o Tempo de Reparo (MTTR) em horas para cada OS concluída
        df['Tempo_Reparo_Horas'] = (df[col_fechamento[0]] - df[col_abertura[0]]).dt.total_seconds() / 3600.0
        df['Tempo_Reparo_Horas'] = df['Tempo_Reparo_Horas'].fillna(0.0).apply(lambda x: max(x, 0.0))

        # --- CÁLCULO DO MTTR GERAL ---
        total_corretivas = len(df[df[col_tipo[0]].astype(str).str.lower().str.contains('corr', na=False)]) if col_tipo else len(df)
        tempo_total_reparo = df['Tempo_Reparo_Horas'].sum()
        mttr_geral = (tempo_total_reparo / total_corretivas) if total_corretivas > 0 else 0.0

        # --- CÁLCULO DO MTBF GERAL (Simulação Inteligente baseada no intervalo do período) ---
        data_min = df[col_abertura[0]].min()
        data_max = df[col_fechamento[0]].max()
        
        if pd.notnull(data_min) and pd.notnull(data_max):
            tempo_total_operacao_horas = (data_max - data_min).total_seconds() / 3600.0
            # Se o período gravado for muito curto ou zerado, assume o mês comercial padrão (720h)
            if tempo_total_operacao_horas <= 0:
                tempo_total_operacao_horas = 720.0
        else:
            tempo_total_operacao_horas = 720.0
            
        mtbf_geral = (tempo_total_operacao_horas / total_corretivas) if total_corretivas > 0 else tempo_total_operacao_horas

        # --- CÁLCULO DE DISPONIBILIDADEestrutural ---
        if (mtbf_geral + mttr_geral) > 0:
            disponibilidade_geral = (mtbf_geral / (mtbf_geral + mttr_geral)) * 100.0

# =========================================================================
# 5. INTERFACE PRINCIPAL DOS INDICADORES
# =========================================================================
st.markdown('<div class="card-home"><div class="card-home-title">📊 KPIs de Engenharia de Manutenção (MTBF, MTTR & Disponibilidade)</div></div>', unsafe_allow_html=True)

if not df.empty:
    # Cartões de Métricas de Confiabilidade
    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric(label="⏱️ MTBF (Tempo Médio Entre Falhas)", value=f"{mtbf_geral:.1f} horas", help="Quanto maior este tempo, mais confiável é o seu ativo.")
    with k2:
        st.metric(label="🛠️ MTTR (Tempo Médio de Reparo)", value=f"{mttr_geral:.1f} horas", delta="Alvo: < 4.0h" if mttr_geral > 4 else "Excelente", delta_color="inverse" if mttr_geral > 4 else "normal", help="Tempo médio gasto para consertar uma pane. Quanto menor, melhor.")
    with k3:
        st.metric(label="🔋 Disponibilidade Estrutural", value=f"{disponibilidade_geral:.2f} %", delta="Conforme" if disponibilidade_geral >= 95 else "Abaixo da Meta", delta_color="normal" if disponibilidade_geral >= 95 else "inverse")

    st.write("<br>", unsafe_allow_html=True)
    
    col_grafico, col_dados = st.columns([1.2, 1.0])
    
    with col_grafico:
        st.markdown("**⏳ Tempo de Intervenção Técnica por Ativo (Horas de Indisponibilidade)**")
        if col_descricao_ativo and 'Tempo_Reparo_Horas' in df.columns:
            # Agrupa os ativos para descobrir qual deles roubou mais tempo de operação da equipe técnica
            df_tempo_ativo = df.groupby(col_descricao_ativo[0])['Tempo_Reparo_Horas'].sum().reset_index()
            df_tempo_ativo = df_tempo_ativo.sort_values(by='Tempo_Reparo_Horas', ascending=False).head(5)
            
            chart_tempo = alt.Chart(df_tempo_ativo).mark_bar(color='#DC2626').encode(
                x=alt.X('Tempo_Reparo_Horas:Q', title='Tempo de Reparo Acumulado (Horas)'),
                y=alt.Y(f'{col_descricao_ativo[0]}:N', title='Ativo/Equipamento', sort='-x'),
                tooltip=[col_descricao_ativo[0], 'Tempo_Reparo_Horas']
            ).properties(height=280)
            st.altair_chart(chart_tempo, use_container_width=True)
        else:
            st.info("Colunas temporais ou de descrição indisponíveis para plotagem.")
            
    with col_dados:
        st.markdown(f"**Parecer da IA sobre Confiabilidade — {NOME_PROJETO}**")
        
        # Gera insights automáticos dependendo da meta internacional de manutenção
        if disponibilidade_geral < 95.0 or mttr_geral > 6.0:
            st.error(f"""
            ### ❌ ALERTA DE INDISPONIBILIDADE
            A IA detectou uma queda na eficiência de resposta da manutenção.
            
            * **Diagnóstico:** O MTTR atual de **{mttr_geral:.1f} horas** está acima da linha de controle internacional de engenharia. Os equipamentos estão demorando muito tempo parados durante os reparos.
            * **Causa Provável:** Falta de peças de reposição em estoque crítico ou atraso no despacho de equipes especializadas.
            
            🚨 **Ação Sugerida:** Mapear o ativo no topo do gráfico ao lado e criar um procedimento operacional padrão (POP) de manutenção emergencial para ele.
            """)
        else:
            st.success(f"""
            ### ✅ EQUILÍBRIO DE DISPONIBILIDADE
            O plano de metas temporais está operando na zona segura de conformidade.
            
            * **Diagnóstico:** A disponibilidade média acumulada de **{disponibilidade_geral:.2f}%** atende os critérios globais de O&M (Meta > 95%).
            * **Confiabilidade:** O intervalo médio entre quebras espontâneas (MTBF) confere fôlego operacional ao cronograma.
            
            👍 **Orientação:** Continue mantendo a rotina rígida de preventivas para garantir que o MTBF não encolha nos próximos ciclos.
            """)

