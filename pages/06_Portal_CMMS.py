import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página corporativa
st.set_page_config(page_title="Portal CMMS", page_icon="🛠️", layout="wide")

st.title("🛠️ Portal CMMS - Gestão Ativa de Manutenção")
st.markdown("### Abertura e Monitoramento de Ordens de Serviço (OS)")

# Criando abas para organizar o fluxo de trabalho do cliente
tab1, tab2 = st.tabs(["📋 Abrir Nova Ordem de Serviço", "📊 Painel de Controle (OS)"])

with tab1:
    st.subheader("Registrar Ocorrência / Manutenção")
    
    # Formulário estruturado para engenharia de manutenção
    with st.form("form_cmms", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            ativo = st.selectbox("Selecione o Ativo Crítico:", ["Subestação Principal", "Transformador T01", "Gerador Auxiliar", "Painel de Telemetria"])
            tipo_manutencao = st.radio("Tipo de Intervenção:", ["Corretiva (Urgente)", "Preventiva", "Preditiva (Alerta Digital)"])
        
        with col2:
            solicitante = st.text_input("Nome do Engenheiro/Técnico Responsável:")
            prioridade = st.select_slider("Nível de Prioridade:", options=["Baixa", "Média", "Alta", "Crítica"])
            
        descricao = st.text_area("Descrição detalhada do problema observado (ou anomalia identificada no Gêmeo Digital):")
        
        # Botão de envio
        submetido = st.form_submit_button("Protocolar Ordem de Serviço")
        
        if submetido:
            if solicitante and descricao:
                st.success(f"✅ OS gerada com sucesso para o ativo **{ativo}**! Registrado sob protocolo #{datetime.now().strftime('%Y%m%d%H%M')}")
            else:
                st.error("❌ Por favor, preencha todos os campos obrigatórios (Responsável e Descrição).")

with tab2:
    st.subheader("Status das Manutenções Contratadas")
    
    # Simulando dados reais de ordens existentes para o cliente inspecionar
    dados_mock = {
        "Cód OS": ["#2026001", "#2026002", "#2026003"],
        "Data": ["28/06/2026", "29/06/2026", "01/07/2026"],
        "Ativo": ["Transformador T01", "Subestação Principal", "Gerador Auxiliar"],
        "Tipo": ["Preventiva", "Corretiva (Urgente)", "Preditiva"],
        "Status": ["Concluído", "Em Execução", "Aguardando Peças"],
        "Técnico Alocado": ["Carlos Silva", "Roberto Souza", "Aline Mendes"]
    }
    df_os = pd.DataFrame(dados_mock)
    
    # Exibindo os cartões de métricas (KPIs rápidos)
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total de Chamados", len(df_os))
    kpi2.metric("Em Aberto / Execução", "2", delta="-1 resolvido hoje")
    kpi3.metric("Tempo Médio de Atendimento", "2.4 horas")
    
    st.markdown("---")
    
    # Tabela interativa de dados
    st.dataframe(df_os, use_container_width=True)
    
    # Recurso de exportação (Essencial para relatórios de CMMS)
    csv = df_os.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar Relatório de OS (CSV)",
        data=csv,
        file_name="relatorio_manutencao_cmms.csv",
        mime="text/csv",
    )
