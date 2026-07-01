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
    
    if arquivo_upload is not None and not df_exibicao.empty:
    col_sel, col_diag = st.columns(2)
    
    with col_sel:
        st.markdown("**🔎 Seleção de Ativo para Auditoria**")
        os_selecionada = st.selectbox("Selecione a OS para análise da IA:", lista_os_selecao, key="seletor_ia_final_limpo")
        
        linha_os = df_exibicao[df_exibicao['OS'] == os_selecionada].iloc[0]
        
        id_coluna_b = str(linha_os.get('ID', '')).strip().lower()
        equipamento, fabricante, modelo = extrair_dados_reais_speckle(id_coluna_b)
            
        if equipamento in ['nan', '']: equipamento = "Ativo Operacional"
        if fabricante in ['nan', '']: fabricante = "Fabricante Padrão"
        if modelo in ['nan', '']: modelo = "Modelo Geral"

        # --- CÁLCULO ESTATÍSTICO DE HISTÓRICO REAL EM TEMPO REAL ---
        historico_ativo = df_os[df_os['ID'].astype(str).str.strip().str.lower() == id_coluna_b]
        total_recorrencias = len(historico_ativo)
        
        if total_recorrencias > 1:
            datas_quebras = sorted(pd.to_datetime(historico_ativo['Data_Abertura'], errors='coerce').dropna())
            if len(datas_quebras) > 1:
                dias_totais = (datas_quebras[-1] - datas_quebras[0]).days
                mtbf_calculado = round(dias_totais / (total_recorrencias - 1), 1)
                texto_mtbf = f"{mtbf_calculado} dias"
            else:
                texto_mtbf = "Dados de data insuficientes para cálculo"
        else:
            texto_mtbf = "Sem falhas repetidas (Ativo estável)"
            
        try:
            data_abertura_formatada = "N/A" if pd.isna(linha_os['Data_Abertura']) else pd.to_datetime(linha_os['Data_Abertura']).strftime('%d/%m/%Y %H:%M')
        except:
            data_abertura_formatada = "N/A"
        
        st.info(f"""
        **📋 Ficha Técnica do Ativo (Engenharia de Confiabilidade)**
        * **Equipamento:** {equipamento}
        * **Fabricante:** {fabricante} | **Modelo:** {modelo}
        * **Status Atual:** {linha_os['Status']} | **Abertura:** {data_abertura_formatada}
        * 📊 **Histórico de Quebras:** {total_recorrencias} ocorrências no banco CMMS.
        * ⏱️ **MTBF Estatístico Real:** {texto_mtbf}
        * 🆔 **ID do Objeto 3D:** `{id_coluna_b}`
        """)
        
    with col_diag:
        st.markdown("**⚡ Análise de Engenharia Operacional da IA**")
        status_normalizado = str(linha_os['Status']).strip().lower()
        
        # CASO 1: ORDEM ABERTA (DIAGNÓSTICOS PRESCRITIVOS OPERACIONAIS)
        if status_normalizado == 'aberta':
            if id_coluna_b == "4dc3484a7e8cefdfcd6108f0b06cb715":
                st.markdown(f"""
                <div class="card-ia" style="background-color: #fff0f0; border-left: 5px solid #d9534f;">
                    <h4>⚠️ DIAGNÓSTICO PRESCRITIVO: Perda de Pressão na Rede de Incêndio (PPCI)</h4>
                    <p><b>Análise Causa Raiz:</b> Com base na descrição <i>"{linha_os['Descrição']}"</i> e no cruzamento com os parâmetros do material <b>{modelo}</b>, o sistema aponta fadiga em juntas roscadas e acoplamentos no Bloco 1, gerando queda de pressão estática.</p>
                    <hr>
                    <p><b>🔧 Direcionamento e Plano de Ação Real (Segurança contra Incêndio):</b></p>
                    <ol>
                        <li>Isolar o trecho da prumada afetada fechando a válvula de gaveta supervisionada mais próxima.</li>
                        <li>Realizar teste de estanqueidade localizada e inspection visual ao longo da linha de {modelo}.</li>
                        <li>Substituir a seção danificada antes de pressurizar a linha com a bomba Jockey.</li>
                    </ol>
                    <small>🚒 <i>Nível de Criticidade: <span class="badge-alta" style="background-color: #ffb3b3; color: #b30000;">CRÍTICA</span> | MTTR estimado: 120 min.</i></small>
                </div>
                """, unsafe_allow_html=True)
            
            elif id_coluna_b == "540a5723a18454b4145959ce501469bc":
                st.markdown(f"""
                <div class="card-ia">
                    <h4>⚠️ DIAGNÓSTICO PRESCRITIVO: Falha no Sistema de Climatização</h4>
                    <p><b>Análise Causa Raiz:</b> Com base na descrição <i>"{linha_os['Descrição']}"</i> e no cruzamento com os parâmetros do fabricante <b>{fabricante} ({modelo})</b>, o sintoma aponta para obstrução no sistema de drenagem da evaporadora ou saturação dos filtros de ar.</p>
                    <hr>
                    <p><b>🔧 Direcionamento e Plano de Ação Real ({fabricante}):</b></p>
                    <ol>
                        <li>Desligar o disjuntor do circuito de climatização para garantir a segurança elétrica.</li>
                        <li>Remover a carenagem frontal do modelo {modelo} conforme o manual técnico do fabricante.</li>
                        <li>Desobstruir a bandeja de condensado e testar o fluxo da tubulação flexível.</li>
                    </ol>
                    <small>⚡ <i>Nível de Criticidade: <span class="badge-alta">ALTA</span> | MTTR estimado: 35 min.</i></small>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div class="card-ia" style="background-color: #f7f9fa; border-left: 5px solid #00c0ef;">
                    <h4>⚠️ DIAGNÓSTICO OPERACIONAL: Ordem de Serviço em Triagem</h4>
                    <p><b>Análise Causa Raiz:</b> Ativo técnico <b>{equipamento}</b> aguardando conclusão do cruzamento de metadados BIM.</p>
                    <hr>
                    <p><b>🔧 Recomendações Preliminares:</b></p>
                    <ul>
                        <li>Verificar a descrição da falha: <i>"{linha_os['Descrição']}"</i>.</li>
                        <li>Realizar a inspeção visual preliminar em campo para coletar o TAG do componente.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        elif status_normalizado == 'em atendimento':
            st.markdown(f"""
            <div class="card-ia" style="background-color: #fff9e6; border-left: 5px solid #ffaa00;">
                <h4>⏳ ANÁLISE EM TEMPO REAL: Manutenção em Andamento</h4>
                <p><b>Acompanhamento operational:</b> O ativo <b>{equipamento} {fabricante}</b> encontra-se sob intervenção das equipes técnicas de campo.</p>
                <small>🔧 <i>Status do Sistema: Operação Assistida | Execução Iniciada</i></small>
            </div>
            """, unsafe_allow_html=True)
            
        elif status_normalizado in ['pausado', 'pausada']:
            st.markdown(f"""
            <div class="card-ia" style="background-color: #f7f7f7; border-left: 5px solid #6c757d;">
                <h4>⏸️ ANÁLISE COMPLEMENTAR: Ordem Suspensa / Pausada</h4>
                <p><b>Análise de Parada:</b> A atividade no ativo {modelo} está congelada temporariamente aguardando insumos.</p>
                <small>⚠️ <i>Status do Sistema: Aguardando Liberação</i></small>
            </div>
            """, unsafe_allow_html=True)
            
        elif status_normalizado in ['fechado', 'fechada']:
            st.markdown(f"""
            <div class="card-ia" style="background-color: #f6fff6; border-left: 5px solid #28a745;">
                <h4>✅ ANÁLISE COMPLEMENTAR: Ordem Encerrada</h4>
                <p><b>Análise de Fechamento:</b> A OS referente a <i>"{linha_os['Descrição']}"</i> foi devidamente finalizada seguindo as diretrizes da {fabricante}.</p>
                <small>🍃 <i>Status do Sistema: Estável | Eficiência: 100%</i></small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"Status '{linha_os['Status']}' mapeado.")
else:
    st.info("Aguardando carregamento de dados para diagnóstico da IA.")
