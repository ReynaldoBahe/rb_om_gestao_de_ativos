import streamlit as st
import pandas as pd

# Configuração padrão da página para manter a identidade visual da RB Consultoria
st.set_page_config(layout="wide", page_title="CMMS Nativo - RB Consultoria")

st.markdown('### 🛠️ CMMS Proprietário — Gestão de Ordens de Serviço')
st.write("Abra e controle ordens de serviço de forma nativa e integrada ao ecossistema.")

# 🔗 CONEXÃO COM O BANCO DE DADOS EM MEMÓRIA OU ARQUIVO LOCAL
df_base = pd.DataFrame()

for chave in ['dados_os', 'df_filtrado', 'df', 'df_os']:
    if chave in st.session_state and isinstance(st.session_state[chave], pd.DataFrame):
        if not st.session_state[chave].empty:
            df_base = st.session_state[chave]
            break

if df_base.empty:
    for nome_arq in ["CMMS_Export_RB - CMMS_RB.csv", "CMMS_Export_RB.csv"]:
        try:
            df_base = pd.read_csv(nome_arq)
            st.session_state['dados_os'] = df_base
            break
        except Exception:
            continue

if df_base.empty:
    dados_padrao = [{
        'OS': 'OS-2026-001', 'ID': '29e456...', 'Data_Abertura': '26/06/2026 08:00:00',
        'Data_Fechamento': '', 'Descrição': 'Inicialização padrão.',
        'Status': 'Aberta', 'Setor': 'Climatização', 'Tipo_manutencao': 'Preventiva',
        'Responsavel': 'Pedro', 'Criticidade': 'Alta', 'Sintoma_detalhado': 'Sistema ativo.',
        'Pecas_substituidas': '', 'link_manual_tecnico': '', 'Custo_Material': 0.0,
        'Custo_Mao_Obra': 0.0, 'ID_Sonoff': 'Não Vinculado', 'Tempo_Parado_Horas': 0, 'Causa_Raiz': 'Pendente'
    }]
    df_base = pd.DataFrame(dados_padrao)

if 'dados_os' not in st.session_state or st.session_state['dados_os'].empty:
    st.session_state['dados_os'] = df_base

df = st.session_state['dados_os'].astype(object)

for col in ['Pecas_substituidas', 'Causa_Raiz', 'Data_Fechamento']:
    if col not in df.columns:
        df[col] = ""
    df[col] = df[col].fillna("").astype(str)

# --------------------------------------------------------
# CAIXA 1: REGISTRO DE NOVA OS (USANDO O FORMULÁRIO NATIVO SEGURO)
# --------------------------------------------------------
with st.form("form_nova_os", clear_on_submit=True):
    st.subheader("➕ Registrar Nova Ordem de Serviço")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Código da OS (Automático)", value=f"OS-2026-{len(df) + 1:03d}", disabled=True)
        id_bim = st.text_input("ID BIM do Ativo (Speckle)", value="29e456...")
        setor = st.selectbox("Setor Responsável", ["Climatização", "Elétrica", "Hidráulica", "Mecânica", "Civil"])
        tipo_manutencao = st.selectbox("Tipo de Manutenção", ["Corretiva", "Preventiva", "Preditiva"])
        responsavel = st.selectbox("Profissional Técnico", ["Pedro", "Marcos", "Tiago", "Francisco", "Joaquim"])
        
    with col2:
        criticidade = st.selectbox("Grau de Criticidade", ["Alta", "Média", "Baixa"])
        sintoma = st.text_area("Sintoma Detalhado / Descrição do Problema", placeholder="Descreva o comportamento anômalo encontrado...")
        link_manual = st.text_input("Link do Manual Técnico (URL)", value="")
        id_sonoff = st.text_input("ID do Sensor Sonoff Vinculado", value="Não Vinculado")
        
    btn_registrar = st.form_submit_button("💾 Registrar OS no Sistema")
    
    if btn_registrar:
        if not sintoma.strip():
            st.error("⚠️ Por favor, descreva o sintoma antes de registrar a Ordem de Serviço.")
        else:
            novo_registro = {
                'OS': f"OS-2026-{len(df) + 1:03d}", 'ID': id_bim,
                'Data_Abertura': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S'), 'Data_Fechamento': '',
                'Descrição': f"Atendimento nativo criado via portal para setor de {setor}.",
                'Status': 'Aberta', 'Setor': setor, 'Tipo_manutencao': tipo_manutencao,
                'Responsavel': responsavel, 'Criticidade': criticidade,
                'Sintoma_detalhado': sintoma, 'Pecas_substituidas': '',
                'link_manual_tecnico': link_manual, 'Custo_Material': 0.0,
                'Custo_Mao_Obra': 0.0, 'ID_Sonoff': id_sonoff, 'Tempo_Parado_Horas': 0, 'Causa_Raiz': 'Pendente de Análise'
            }
            
            # Grava na tabela mestre global compartilhada
            st.session_state['dados_os'] = pd.concat([st.session_state['dados_os'], pd.DataFrame([novo_registro])], ignore_index=True)
            st.success(f"✅ {novo_registro['OS']} registrada com sucesso!")
            st.rerun()

# --------------------------------------------------------
# CAIXA 2: PAINEL DE ATUALIZAÇÃO RÁPIDA (BAIXA EM OS)
# --------------------------------------------------------
st.markdown("---")
st.subheader("⚡ Atualização Rápida de Status (Operador)")

lista_os = df['OS'].unique()
os_selecionada = st.selectbox("Selecione uma OS para dar baixa ou alterar status:", lista_os)

condicao = df['OS'] == os_selecionada

if condicao.any():
    status_atual = str(df.loc[condicao, 'Status'].values[0])
    pecas_atuais = df.loc[condicao, 'Pecas_substituidas'].values[0]
    pecas_texto = "" if pd.isna(pecas_atuais) or pecas_atuais == "nan" else str(pecas_atuais)
    
    col_edit1, col_edit2, col_edit3 = st.columns(3)
    with col_edit1:
        status_padrao = ["Aberta", "Em Andamento", "Pausada", "Fechado"]
        idx_status = status_padrao.index(status_atual) if status_atual in status_padrao else 0
        novo_status = st.selectbox("Novo Status", status_padrao, index=idx_status)
    with col_edit2:
        pecas = st.text_input("Peças Substituídas", value=pecas_texto)
    with col_edit3:
        causa = st.selectbox("Causa Raiz", ["Desgaste Natural", "Falha Elétrica", "Erro Operacional", "Falha Mecânica"], index=0)
        
    if st.button("🔄 Atualizar Registro"):
        df_mestre = st.session_state['dados_os']
        condicao_mestre = df_mestre['OS'] == os_selecionada
        
        df_mestre.loc[condicao_mestre, 'Status'] = str(novo_status)
        df_mestre.loc[condicao_mestre, 'Pecas_substituidas'] = str(pecas)
        df_mestre.loc[condicao_mestre, 'Causa_Raiz'] = str(causa)
        
        if novo_status == "Fechado":
            df_mestre.loc[condicao_mestre, 'Data_Fechamento'] = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')
            
        st.session_state['dados_os'] = df_mestre
        st.success(f"📊 Status da {os_selecionada} modificado para '{novo_status}' com sucesso!")
        st.rerun()

# --------------------------------------------------------
# CAIXA 3: EXPORTAÇÃO DOS DADOS ATUALIZADOS
# --------------------------------------------------------
st.markdown("---")
st.subheader("💾 Exportar Banco de Dados Atualizado")

csv_data = st.session_state['dados_os'].to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar Planilha CMMS Atualizada (.CSV)",
    data=csv_data,
    file_name="CMMS_Export_RB_Atualizado.csv",
    mime="text/csv"
)
