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

for col in ['Pecas_substituidas', 'Causa_Raiz', 'Data_Fechamento', 'Setor', 'Tipo_manutencao', 'Responsavel']:
    if col not in df.columns:
        df[col] = ""
    df[col] = df[col].fillna("").astype(str)

# --------------------------------------------------------
# CAIXA 1: REGISTRO DE NOVA OS (MENUS DINÂMICOS COMPLETOS)
# --------------------------------------------------------
st.subheader("➕ Registrar Nova Ordem de Serviço")

# 1. Montagem dinâmica do Setor
setores_existentes = sorted([s for s in df['Setor'].unique() if s.strip() != ""])
if not setores_existentes: setores_existentes = ["Climatização", "Elétrica", "Hidráulica", "Mecânica", "Civil"]
opcoes_setor = setores_existentes + ["➕ Cadastrar Outro Setor..."]

# 2. Montagem dinâmica do Tipo de Manutenção
tipos_existentes = sorted([t for t in df['Tipo_manutencao'].unique() if t.strip() != ""])
if not tipos_existentes: tipos_existentes = ["Corretiva", "Preventiva", "Preditiva"]
opcoes_tipo = tipos_existentes + ["➕ Cadastrar Outro Tipo..."]

# 3. 🔥 NOVIDADE: Montagem dinâmica do Profissional Técnico
tecnicos_existentes = sorted([r for r in df['Responsavel'].unique() if r.strip() != ""])
if not tecnicos_existentes: tecnicos_existentes = ["Pedro", "Marcos", "Tiago", "Francisco", "Joaquim"]
opcoes_tecnico = tecnicos_existentes + ["➕ Cadastrar Outro Técnico..."]

with st.form("form_nova_os", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Código da OS (Automático)", value=f"OS-2026-{len(df) + 1:03d}", disabled=True)
        id_bim = st.text_input("ID BIM do Ativo (Speckle)", value="29e456...")
        
        # Seletor de Setor
        setor_selecionado = st.selectbox("Setor Responsável", opcoes_setor)
        novo_setor_input = ""
        if setor_selecionado == "➕ Cadastrar Outro Setor...":
            novo_setor_input = st.text_input("Digite o nome do NOVO Setor:", placeholder="Ex: Telecom, Incêndio...")
            
        # Seletor de Tipo de Manutenção
        tipo_selecionado = st.selectbox("Tipo de Manutenção", opcoes_tipo)
        novo_tipo_input = ""
        if tipo_selecionado == "➕ Cadastrar Outro Tipo...":
            novo_tipo_input = st.text_input("Digite o NOVO Tipo de Manutenção:", placeholder="Ex: Melhoria, Instalação...")
            
        # 🔥 Seletor Dinâmico de Profissional Técnico
        tecnico_selecionado = st.selectbox("Profissional Técnico", opcoes_tecnico)
        novo_tecnico_input = ""
        if tecnico_selecionado == "➕ Cadastrar Outro Técnico...":
            novo_tecnico_input = st.text_input("Digite o nome do NOVO Profissional Técnico:", placeholder="Ex: Lucas, André, Carlos...")
        
    with col2:
        criticidade = st.selectbox("Grau de Criticidade", ["Alta", "Média", "Baixa"])
        sintoma = st.text_area("Sintoma Detalhado / Descrição do Problema", placeholder="Descreva o comportamento anômalo encontrado...")
        link_manual = st.text_input("Link do Manual Técnico (URL)", value="")
        id_sonoff = st.text_input("ID do Sensor Sonoff Vinculado", value="Não Vinculado")
        
    btn_registrar = st.form_submit_button("💾 Registrar OS no Sistema")
    
    if btn_registrar:
        if not sintoma.strip():
            st.error("⚠️ Por favor, descreva o sintoma antes de registrar a Ordem de Serviço.")
        elif setor_selecionado == "➕ Cadastrar Outro Setor..." and not novo_setor_input.strip():
            st.error("⚠️ Por favor, digite o nome do novo setor.")
        elif tipo_selecionado == "➕ Cadastrar Outro Tipo..." and not novo_tipo_input.strip():
            st.error("⚠️ Por favor, digite o nome do novo tipo de manutenção.")
        elif tecnico_selecionado == "➕ Cadastrar Outro Técnico..." and not novo_tecnico_input.strip():
            st.error("⚠️ Por favor, digite o nome do novo profissional técnico.")
        else:
            setor_final = novo_setor_input.strip() if setor_selecionado == "➕ Cadastrar Outro Setor..." else setor_selecionado
            tipo_final = novo_tipo_input.strip() if tipo_selecionado == "➕ Cadastrar Outro Tipo..." else tipo_selecionado
            tecnico_final = novo_tecnico_input.strip() if tecnico_selecionado == "➕ Cadastrar Outro Técnico..." else tecnico_selecionado
            
            novo_registro = {
                'OS': f"OS-2026-{len(df) + 1:03d}", 'ID': id_bim,
                'Data_Abertura': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S'), 'Data_Fechamento': '',
                'Descrição': f"Atendimento nativo criado via portal para setor de {setor_final}.",
                'Status': 'Aberta', 'Setor': setor_final, 'Tipo_manutencao': tipo_final,
                'Responsavel': tecnico_final, 'Criticidade': criticidade,
                'Sintoma_detalhado': sintoma, 'Pecas_substituidas': '',
                'link_manual_tecnico': link_manual, 'Custo_Material': 0.0,
                'Custo_Mao_Obra': 0.0, 'ID_Sonoff': id_sonoff, 'Tempo_Parado_Horas': 0, 'Causa_Raiz': 'Pendente de Análise'
            }
            
            st.session_state['dados_os'] = pd.concat([st.session_state['dados_os'], pd.DataFrame([novo_registro])], ignore_index=True)
            st.success(f"✅ {novo_registro['OS']} registrada com sucesso!")
            st.rerun()

# --------------------------------------------------------
# CAIXA 2: PAINEL DE ATUALIZAÇÃO RÁPIDA (CAUSA RAIZ DINÂMICA)
# --------------------------------------------------------
st.markdown("---")
st.subheader("⚡ Atualização Rápida de Status (Operador)")

lista_os = df['OS'].unique()
os_selecionada = st.selectbox("Selecione uma OS para dar baixa ou alterar status:", lista_os)

condicao = df['OS'] == os_selecionada

if condicao.any():
    status_atual = str(df.loc[condicao, 'Status'].values).strip()
    pecas_atuais = df.loc[condicao, 'Pecas_substituidas'].values
    pecas_texto = "" if pd.isna(pecas_atuais) or str(pecas_atuais).lower() in ["nan", ""] else str(pecas_atuais)
    
    causa_atual = str(df.loc[condicao, 'Causa_Raiz'].values).strip()
    
    causas_na_planilha = [c for c in df['Causa_Raiz'].unique() if c.strip() not in ["", "nan", "Pendente de Análise"]]
    causas_base = ["Desgaste Natural", "Falha Elétrica", "Erro Operacional", "Falha Mecânica", "Corretiva por Vazamento"]
    causas_unificadas = sorted(list(set(causas_base + causas_na_planilha)))
    opcoes_causa = causas_unificadas + ["➕ Cadastrar Outra Causa Raiz..."]
    
    col_edit1, col_edit2, col_edit3 = st.columns(3)
    with col_edit1:
        status_padrao = ["Aberta", "Em Andamento", "Pausada", "Fechado"]
        idx_status = status_padrao.index(status_atual) if status_atual in status_padrao else 0
        novo_status = st.selectbox("Novo Status", status_padrao, index=idx_status)
    with col_edit2:
        pecas = st.text_input("Peças Substituídas", value=pecas_texto)
    with col_edit3:
        causa_selecionada = st.selectbox("Causa Raiz", opcoes_causa, index=opcoes_causa.index(causa_atual) if causa_atual in opcoes_causa else 0)
        
        nova_causa_input = ""
        if causa_selecionada == "➕ Cadastrar Outra Causa Raiz...":
            nova_causa_input = st.text_input("Digite a NOVA Causa Raiz:")
        
    if st.button("🔄 Atualizar Registro"):
        df_mestre = st.session_state['dados_os']
        condicao_mestre = df_mestre['OS'] == os_selecionada
        
        causa_final = nova_causa_input.strip() if causa_selecionada == "➕ Cadastrar Outra Causa Raiz..." else causa_selecionada
        
        if causa_selecionada == "➕ Cadastrar Outra Causa Raiz..." and not nova_causa_input.strip():
            st.error("⚠️ Por favor, digite o nome da nova causa raiz.")
        else:
            df_mestre.loc[condicao_mestre, 'Status'] = str(novo_status)
            df_mestre.loc[condicao_mestre, 'Pecas_substituidas'] = str(pecas)
            df_mestre.loc[condicao_mestre, 'Causa_Raiz'] = str(causa_final)
            
            if novo_status == "Fechado":
                df_mestre.loc[condicao_mestre, 'Data_Fechamento'] = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')
                
            st.session_state['dados_os'] = df_mestre
