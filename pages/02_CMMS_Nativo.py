import streamlit as st
import pandas as pd

# Configuração padrão da página para manter a identidade visual da RB Consultoria
st.set_page_config(layout="wide", page_title="CMMS Nativo - RB Consultoria")

st.markdown('### 🛠️ CMMS Proprietário — Gestão de Ordens de Serviço')
st.write("Abra e controle ordens de serviço de forma nativa e integrada ao ecossistema.")

# 🔗 CONEXÃO COM O BANCO DE DADOS EM MEMÓRIA DO PORTAL
# 🔗 CONEXÃO COM O BANCO DE DADOS EM MEMÓRIA OU ARQUIVO LOCAL
df_base = pd.DataFrame()

# 1. Tenta buscar das variáveis de sessão conhecidas
for chave in ['dados_os', 'df_filtrado', 'df', 'df_os']:
    if chave in st.session_state and isinstance(st.session_state[chave], pd.DataFrame):
        if not st.session_state[chave].empty:
            df_base = st.session_state[chave]
            break

# 2. SE CONTINUAR VAZIO: Lê direto o arquivo físico do seu repositório para nunca quebrar
if df_base.empty:
    try:
        # Lê o seu CSV padrão que está na raiz do GitHub
        df_base = pd.read_csv("CMMS_Export_RB.csv")
        # Alimenta a sessão global para sincronizar com as outras abas
        st.session_state['dados_os'] = df_base
    except Exception:
        # Se falhar o CSV, tenta ler se por acaso tiver um Excel com o mesmo nome
        try:
            df_base = pd.read_excel("CMMS_Export_RB.xlsx")
            st.session_state['dados_os'] = df_base
        except Exception:
            pass

# 3. VERIFICAÇÃO FINAL DE SEGURANÇA (Se mesmo assim não achar o arquivo no GitHub)
if df_base.empty:
    st.warning("⚠️ Certifique-se de que o arquivo 'CMMS_Export_RB.csv' está na raiz do seu repositório GitHub para liberar o CMMS Nativo.")
else:
    # Cria uma cópia limpa para manipulação
    df = df_base.copy()

    # Cria uma cópia limpa para manipulação
    df = df_base.copy()

    # --------------------------------------------------------
    # FORMULÁRIO DE ABERTURA DE NOVA OS
    # --------------------------------------------------------
    with st.form("formulario_nova_os", clear_on_submit=True):
        st.subheader("➕ Registrar Nova Ordem de Serviço")
        
        col1, col2 = st.columns(2)
        with col1:
            nova_os = st.text_input("Código da OS", value=f"OS-2026-{len(df) + 1:03d}")
            id_bim = st.text_input("ID BIM do Ativo (Speckle)", value="29e456...")
            setor = st.selectbox("Setor Responsável", ["Climatização", "Elétrica", "Hidráulica", "Mecânica", "Civil"])
            tipo_manutencao = st.selectbox("Tipo de Manutenção", ["Corretiva", "Preventiva", "Preditiva"])
            responsavel = st.selectbox("Profissional Técnico", ["Pedro", "Marcos", "Tiago", "Francisco", "Joaquim"])
            
        with col2:
            criticidade = st.selectbox("Grau de Criticidade", ["Alta", "Média", "Baixa"])
            sintoma = st.text_area("Sintoma Detalhado / Descrição do Problema", placeholder="Descreva o comportamento anômalo...")
            link_manual = st.text_input("Link do Manual Técnico (URL)", value="")
            id_sonoff = st.text_input("ID do Sensor Sonoff Vinculado", value="Não Vinculado")
            
        btn_registrar = st.form_submit_button("💾 Registrar OS no Sistema")
        
        if btn_registrar:
            novo_registro = {
                'OS': nova_os, 'ID': id_bim,
                'Data_Abertura': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S'),
                'Data_Fechamento': '',
                'Descrição': f"Atendimento nativo criado via portal para setor de {setor}.",
                'Status': 'Aberta', 'Setor': setor, 'Tipo_manutencao': tipo_manutencao,
                'Responsavel': responsavel, 'Criticidade': criticidade,
                'Sintoma_detalhado': sintoma, 'Pecas_substituidas': '',
                'link_manual_tecnico': link_manual, 'Custo_Material': 0.0,
                'Custo_Mao_Obra': 0.0, 'ID_Sonoff': id_sonoff,
                'Tempo_Parado_Horas': 0, 'Causa_Raiz': 'Pendente de Análise'
            }
            
            # Injeta a nova linha diretamente na memória compartilhada do Streamlit
            st.session_state['dados_os'] = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
            st.success(f"✅ {nova_os} registrada com sucesso! Os gráficos e a IA das outras abas já foram atualizados.")
            st.rerun()

    # --------------------------------------------------------
    # PAINEL DE ATUALIZAÇÃO RÁPIDA (BAIXA EM OS)
    # --------------------------------------------------------
    st.markdown("---")
    st.subheader("⚡ Atualização Rápida de Status (Operador)")
    
    os_selecionada = st.selectbox("Selecione uma OS para dar baixa ou alterar status:", df['OS'].unique())
    
    # Extrai a linha específica correspondente à OS selecionada
    linha_os = df[df['OS'] == os_selecionada]
    
    if not linha_os.empty:
        dados_os_sel = linha_os.iloc[0]
        
        col_edit1, col_edit2, col_edit3 = st.columns(3)
        with col_edit1:
            status_padrao = ["Aberta", "Em Andamento", "Pausada", "Fechado"]
            status_atual = dados_os_sel.get('Status', 'Aberta')
            idx_status = status_padrao.index(status_atual) if status_atual in status_padrao else 0
            novo_status = st.selectbox("Novo Status", status_padrao, index=idx_status)
        with col_edit2:
            pecas_atuais = dados_os_sel.get('Pecas_substituidas', '')
            pecas = st.text_input("Peças Substituídas", value="" if pd.isna(pecas_atuais) else str(pecas_atuais))
        with col_edit3:
            causa = st.selectbox("Causa Raiz", ["Desgaste Natural", "Falha Elétrica", "Erro Operacional", "Falha Mecânica"], index=0)
            
        if st.button("🔄 Atualizar Registro"):
            # Localiza o índice numérico exato na tabela mestre do Session State
            idx_global = df[df['OS'] == os_selecionada].index
            
            st.session_state['dados_os'].at[idx_global[0], 'Status'] = novo_status
            st.session_state['dados_os'].at[idx_global[0], 'Pecas_substituidas'] = pecas
            st.session_state['dados_os'].at[idx_global[0], 'Causa_Raiz'] = causa
            
            if novo_status == "Fechado":
                st.session_state['dados_os'].at[idx_global[0], 'Data_Fechamento'] = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')
                
            st.success(f"📊 Status da {os_selecionada} modificado para '{novo_status}' com sucesso!")
            st.rerun()

    # --------------------------------------------------------
    # RECURSO ADICIONAL: EXPORTAÇÃO DOS DADOS ATUALIZADOS
    # --------------------------------------------------------
    st.markdown("---")
    st.subheader("💾 Exportar Banco de Dados Atualizado")
    st.write("Baixe as alterações feitas no portal de volta para o seu computador.")
    
    # Converte o DataFrame atual da memória para formato CSV pronto para download
    csv_data = st.session_state['dados_os'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Planilha CMMS Atualizada (.CSV)",
        data=csv_data,
        file_name="CMMS_Export_RB_Atualizado.csv",
        mime="text/csv"
    )
