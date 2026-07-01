import streamlit as st
import pandas as pd

# 1. Configuração da Página (Layout Amplo e Corporativo)
st.set_page_config(
    page_title="RB Consultoria - Gestão de Ativos",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔐 TRAVA DE SEGURANÇA
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Acesso negado. Por favor, faça o login na página inicial.")
    st.stop()

# Estilização CSS para garantir a harmonia visual, tamanho do visualizador e design dos cards de IA
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    iframe { width: 100% !important; height: 1000px !important; border-radius: 12px; }
    .card-ia {
        background-color: #f0f7ff;
        border-left: 5px solid #0066cc;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .badge-alta { background-color: #ffcccc; color: #cc0000; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. Layout de Tela: Barra Lateral (Métricas Operacionais)
with st.sidebar:
    st.title("Painel de Controle")
    st.markdown("---")
    
    # Componente de Upload do arquivo CSV gerado pelo CMMS
    arquivo_upload = st.file_uploader("Carregar Planilha CMMS (.csv)", type=["csv"])
    
    st.markdown("---")
    
    # Inicialização global das variáveis para evitar escopo local isolado
    df_exibicao = pd.DataFrame()
    lista_os_selecao = ["Nenhuma OS selecionada"]
    contagem_status = {"Aberta": 0, "Em Atendimento": 0, "Pausada": 0, "Fechado": 0}
    
    if arquivo_upload is not None:
        try:
            # Lendo a planilha carregada pelo usuário
            df_os = pd.read_csv(arquivo_upload)
            df_os.columns = df_os.columns.str.strip()
            
            # Padronização e limpeza dos dados
            df_os['Data_Abertura'] = pd.to_datetime(df_os['Data_Abertura'], errors='coerce')
            df_os['Status'] = df_os['Status'].astype(str).str.strip()
            df_os['Setor'] = df_os['Setor'].astype(str).str.strip()
            df_os['OS'] = df_os['OS'].astype(str).str.strip()
            
            # Base de cálculo estrita: Mês de Junho/2026
            df_mes = df_os[df_os['Data_Abertura'].dt.strftime('%Y-%m') == '2026-06']
            
            # --- ATUALIZAÇÃO DIRETA NO ESCOPO GLOBAL DO DICIONÁRIO ---
            contagem_status["Aberta"] = len(df_mes[df_mes['Status'].str.lower() == 'aberta'])
            contagem_status["Em Atendimento"] = len(df_mes[df_mes['Status'].str.lower() == 'em atendimento'])
            contagem_status["Pausada"] = len(df_mes[df_mes['Status'].str.lower() == 'pausado'])
            contagem_status["Fechado"] = len(df_mes[df_mes['Status'].str.lower() == 'fechado'])
            
                       setores_validos = df_mes['Setor'].dropna().astype(str).unique()
            lista_setores = ["Todos"] + sorted(list(setores_validos))
            setor_selecionado = st.selectbox("Filtrar por Setor:", lista_setores)
            
            status_validos = df_mes['Status'].dropna().astype(str).unique()
            lista_status = ["Todos"] + sorted(list(status_validos))
            status_selecionado = st.selectbox("Filtrar por Status:", lista_status)

            
            # Aplicando os filtros na tabela de exibição
            df_exibicao = df_mes.copy()
            if setor_selecionado != "Todos":
                df_exibicao = df_exibicao[df_exibicao['Setor'] == setor_selecionado]
            if status_selecionado != "Todos":
                df_exibicao = df_exibicao[df_exibicao['Status'] == status_selecionado]
            
            # Lista de OS para o seletor da IA baseada no filtro ativo
            lista_os_selecao = sorted(list(df_exibicao['OS'].unique()))
            
            st.markdown("---")
            st.subheader("Métricas de Manutenção")
            
            total_abertas_mes = len(df_mes)
            if total_abertas_mes > 0:
                total_fechadas_filtradas = len(df_mes[df_mes['Status'].str.lower() == 'fechado'])
                sla_calculado = round((total_fechadas_filtradas / total_abertas_mes) * 100, 1)
                
                st.metric(
                    label="SLA de Atendimento (Meta: 95%)",
                    value=f"{sla_calculado}%",
                    delta=f"{round(sla_calculado - 95.0, 1)}% em relação à meta",
                    delta_color="normal" if sla_calculado >= 95 else "inverse"
                )
        except Exception as e:
            st.error(f"Erro ao processar as colunas: {e}")
    else:
        st.warning("Aguardando upload da planilha...")
        st.metric(label="SLA de Atendimento (Meta: 95%)", value="-- %", delta="Sem dados")

# 3. Layout de Tela: Área Central (Maquete 3D Panorâmica do Speckle Atualizada)
st.title("Visualizador Operacional de Ativos 3D")

# URL atualizada com o novo embedToken enviado pelo usuário
url_maquete_3d = "https://speckle.systems"
st.components.v1.iframe(url_maquete_3d, height=1000)

st.markdown("---")

# 4. Volumetria das Ordens de Serviço (KPIs)
st.subheader("📊 Volumetria das Ordens de Serviço")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric(label="🟢 Aberta", value=contagem_status["Aberta"])
with col2: st.metric(label="🔵 Em Atendimento", value=contagem_status["Em Atendimento"])
with col3: st.metric(label="🟡 Pausada", value=contagem_status["Pausada"])
with col4: st.metric(label="🔴 Fechado", value=contagem_status["Fechado"])

st.markdown("---")

# 5. Centro de Diagnóstico Avançado (IA Preditiva)
st.subheader("🧠 Centro de Diagnóstico Avançado (IA Preditiva)")

if arquivo_upload is not None and not df_exibicao.empty:
    col_sel, col_diag = st.columns(2)
    
    with col_sel:
        st.markdown("**🔎 Seleção de Ativo para Auditoria**")
        os_selecionada = st.selectbox("Selecione a OS para análise da IA:", lista_os_selecao)
        
        # Puxando a linha selecionada para simular o cruzamento de dados
        linha_os = df_exibicao[df_exibicao['OS'] == os_selecionada].iloc[0]
        
        # Formatação segura da data de abertura
        data_abertura_formatada = "N/A" if pd.isna(linha_os['Data_Abertura']) else linha_os['Data_Abertura'].strftime('%d/%m/%Y')
        
        st.info(f"""
        **📋 Ficha Técnico do Ativo**
        * **Setor:** {linha_os['Setor']}
        * **Status Atual:** {linha_os['Status']}
        * **Data de Abertura:** {data_abertura_formatada}
        * **Histórico de Quebras:** 3 recorrências registradas nos últimos 180 dias.
        * 📖 [Acessar Manual Técnico do Ativo](https://github.com)
        """)
        
    with col_diag:
        st.markdown("**⚡ Análise de Engenharia Operacional da IA**")
        
        status_normalizado = str(linha_os['Status']).strip().lower()
        
        # CASO 1: ORDEM ABERTA
        if status_normalizado == 'aberta':
            st.markdown(f"""
            <div class="card-ia">
                <h4>⚠️ DIAGNÓSTICO PRESCRITIVO: Risco de Parada Crítica</h4>
                <p><b>Análise Causa Raiz:</b> Com base na descrição <i>"{linha_os['Descrição']}"</i> e no cruzamento com o manual técnico, o sintoma apresentado aponta para fadiga por vibração excessiva nas prumadas de alimentação do Bloco B.</p>
                <hr>
                <p><b>🔧 Direcionamento e Plano de Ação para Campo:</b></p>
                <ol>
                    <li>Isolar a válvula reguladora de pressão hidráulica conforme Seção 4.2 do manual.</li>
                    <li>Verificar se há microfissuras na junta de expansão flexível.</li>
                    <li>Substituir anéis de vedação elastoméricos antes de reabrir o fluxo.</li>
                </ol>
                <small>⚡ <i>Nível de Criticidade: <span class="badge-alta">ALTA</span> | MTTR estimado: 45 min.</i></small>
            </div>
            """, unsafe_allow_html=True)
            
        # CASO 2: ORDEM EM ATENDIMENTO
        elif status_normalizado == 'em atendimento':
            st.markdown(f"""
            <div class="card-ia" style="background-color: #fff9e6; border-left: 5px solid #ffaa00;">
                <h4>⏳ ANÁLISE EM TEMPO REAL: Manutenção em Andamento</h4>
                <p><b>Acompanhamento operacional:</b> O ativo associado à atividade <i>"{linha_os['Descrição']}"</i> encontra-se sob intervenção das equipes técnicas de campo.</p>
                <hr>
                <p><b>💡 Recomendação de Monitoramento:</b></p>
                <ul>
                    <li>Garantir o registro de trocas de peças e insumos em tempo real para evitar gargalos de estoque.</li>
                    <li>Verificar se o tempo de atendimento está alinhado com o MTTR previsto no plano mestre.</li>
                </ul>
                <small>🔧 <i>Status do Sistema: Operação Assistida | Execução Iniciada</i></small>
            </div>
            """, unsafe_allow_html=True)
            
        # CASO 3: ORDEM PAUSADA
        elif status_normalizado == 'pausado' or status_normalizado == 'pausada':
            st.markdown(f"""
            <div class="card-ia" style="background-color: #f7f7f7; border-left: 5px solid #6c757d;">
                <h4>⏸️ ANÁLISE COMPLEMENTAR: Ordem Suspensa / Pausada</h4>
                <p><b>Análise de Parada:</b> A atividade <i>"{linha_os['Descrição']}"</i> está congelada temporariamente. O sistema indica pendência externa ou aguardo de insumos para continuidade.</p>
                <hr>
                <p><b>📋 Plano de Mitigação:</b></p>
                <ul>
                    <li>Confirmar no módulo de compras se a entrega de componentes/ferramental está agendada.</li>
                    <li>Avaliar se a pausa compromete a integridade estrutural do sistema em curto prazo.</li>
                </ul>
                <small>⚠️ <i>Status do Sistema: Aguardando Liberação | Cronograma Impactado</i></small>
            </div>
            """, unsafe_allow_html=True)
            
        # CASO 4: ORDEM FECHADA
        elif status_normalizado == 'fechado' or status_normalizado == 'fechada':
            st.markdown(f"""
            <div class="card-ia" style="background-color: #f6fff6; border-left: 5px solid #28a745;">
                <h4>✅ ANÁLISE COMPLEMENTAR: Ordem Encerrada</h4>
                <p><b>Análise de Fechamento:</b> A OS referente a <i>"{linha_os['Descrição']}"</i> foi devidamente finalizada. O histórico confirma que a intervenção seguiu os parâmetros padrão especificados pelo fabricante no manual técnico.</p>
                <hr>
                <p><b>📈 Recomendação Preditiva:</b></p>
                <ul>
                    <li>Agendar inspeção termográfica preventiva em 90 dias para garantir a estabilidade do ativo.</li>
                    <li>Registrar a conformidade dos componentes trocados no banco de dados do CMMS.</li>
                </ul>
                <small>🍃 <i>Status do Sistema: Estável | Eficiência de Execução: 100%</i></small>
            </div>
            """, unsafe_allow_html=True)
            
        # CASO DE SEGURANÇA (STATUS DESCONHECIDO)
        else:
            st.warning(f"Status '{linha_os['Status']}' identificado, mas nenhuma regra de IA correspondente foi mapeada.")
else:
    st.info("Aguardando carregamento de dados para diagnóstico da IA.")
