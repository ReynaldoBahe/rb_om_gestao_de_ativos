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
            
            st.subheader("Filtros de Visão")
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

# 3. Layout de Tela: Área Central (Maquete 3D Panorâmica do Speckle)
st.title("Visualizador Operacional de Ativos 3D")

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

def extrair_dados_reais_speckle(object_id):
    try:
        from specklepy.api.client import SpeckleClient
        from specklepy.api.wrapper import StreamWrapper
        
        url_stream = "https://speckle.systems"
        wrapper = StreamWrapper(url_stream)
        client = wrapper.get_client()
        
        objeto_BIM = client.object.get(stream_id=wrapper.stream_id, object_id=object_id)
        propriedades = objeto_BIM.data.get("properties", {})
        categoria_bim = str(objeto_BIM.data.get("category", "")).lower()
        
        if "pipes" in categoria_bim or "pipe" in categoria_bim:
            equipamento = "Tubulação Hidráulica de Combate a Incêndio"
            fabricante = propriedades.get("family", "Rede Geral - PPCI")
            modelo = propriedades.get("type", "Aço Galvanizado")
        elif "mechanical" in categoria_bim:
            equipamento = "Sistema de Climatização / Ar Condicionado"
            familia_texto = propriedades.get("family", "Fabricante Homologado")
            fabricante = familia_texto.split('_') if '_' in familia_texto else familia_texto
            modelo = propriedades.get("type", "Modelo de Campo")
        else:
            equipamento = propriedades.get("category", "Ativo Operacional")
            fabricante = propriedades.get("family", "Fabricante Padrão")
            modelo = propriedades.get("type", "Modelo Geral")
        return equipamento, fabricante, modelo
    except:
        return "Ativo em Auditoria", "Fabricante Padrão", "Modelo de Engenharia"

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
            
        data_abertura_formatada = "N/A" if pd.isna(linha_os['Data_Abertura']) else linha_os['Data_Abertura'].strftime('%d/%m/%Y')
        
        # --- BUSCA DO HISTÓRICO DO ATIVO VIA PANDAS ---
        df_historico_ativo = df_os[(df_os['ID'].astype(str).str.strip().str.lower() == id_coluna_b) & (df_os['OS'] != os_selecionada)]
        
        texto_historico_ia = ""
        if not df_historico_ativo.empty:
            for _, row_hist in df_historico_ativo.iterrows():
                try:
                    data_hist = row_hist['Data_Abertura'].strftime('%d/%m/%Y') if not pd.isna(row_hist['Data_Abertura']) else "N/A"
                except:
                    data_hist = str(row_hist['Data_Abertura'])
                texto_historico_ia += f"- OS {row_hist['OS']} ({data_hist}): {row_hist['Descrição']} | Status: {row_hist['Status']}\n"
        else:
            texto_historico_ia = "Nenhuma ocorrência anterior registrada para este ativo nos últimos meses."

        st.info(f"""
        **📋 Ficha Técnica do Ativo (Parâmetros Speckle/BIM)**
        * **Equipamento:** {equipamento}
        * **Fabricante:** {fabricante}
        * **Modelo:** {modelo}
        * **Status Atual:** {linha_os['Status']}
        * **Data de Abertura:** {data_abertura_formatada}
        * **ID do Objeto 3D:** `{id_coluna_b}`
        """)
        
        with st.expander("📊 Ver Histórico Completo do Ativo (Coluna B)"):
            if not df_historico_ativo.empty:
                st.dataframe(df_historico_ativo[['OS', 'Data_Abertura', 'Descrição', 'Status']], use_container_width=True)
            else:
                st.caption("Este ativo não possui ordens de serviço anteriores.")
        
    with col_diag:
        st.markdown("**⚡ Análise de Engenharia Operacional da IA**")
        status_normalizado = str(linha_os['Status']).strip().lower()
        
        if status_normalizado == 'aberta':
            from google import genai
            from google.genai import types
            
