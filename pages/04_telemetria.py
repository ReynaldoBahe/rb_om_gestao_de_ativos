import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# =========================================================
# TRAVA DE SEGURANÇA (Garantia do ecossistema multi-cliente)
# =========================================================
if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.error("🔒 Acesso negado. Por favor, faça o login na página inicial (00_Login).")
    st.stop()

# Captura os dados do cliente logado na sessão ativa
id_cliente = st.session_state.get("id_cliente", 1)
nome_cliente = st.session_state.get("nome_cliente", "Cliente")

# =========================================================
# CONTEÚDO PRINCIPAL DA PÁGINA
# =========================================================
st.header(f"⚡ Monitoramento de Recursos - {nome_cliente}")
st.caption("Dados de telemetria em tempo real para controle de insumos e metas.")

# Filtro de período temporal na barra lateral
st.sidebar.markdown("---")
st.sidebar.subheader("📅 Filtros do Painel")
dias = st.sidebar.slider("Período de análise (dias)", min_value=7, max_value=30, value=15)

# Simulação de dados gerados dinamicamente baseados no ID do cliente
np.random.seed(int(id_cliente))
datas = [datetime.now() - timedelta(days=i) for i in range(dias)]
datas.reverse()

dados = pd.DataFrame({
    "Data": datas,
    "Energia (kWh)": np.random.uniform(150, 300, size=dias),
    "Água (m³)": np.random.uniform(5, 12, size=dias)
})
dados["Custo Energia (R$)"] = dados["Energia (kWh)"] * 0.85
dados["Custo Água (R$)"] = dados["Água (m³)"] * 6.50

# Renderização dos cartões de métricas (KPIs)
tot_energia = dados["Energia (kWh)"].sum()
tot_agua = dados["Água (m³)"].sum()
custo_total = dados["Custo Energia (R$)"].sum() + dados["Custo Água (R$)"].sum()

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="⚡ Consumo Energia", value=f"{tot_energia:,.1f} kWh", delta="-3.2%")
with kpi2:
    st.metric(label="💧 Consumo Água", value=f"{tot_agua:,.1f} m³", delta="1.5%", delta_color="inverse")
with kpi3:
    st.metric(label="💰 Custo Estimado", value=f"R$ {custo_total:,.2f}")

st.markdown("---")

# Gráficos de consumo do painel
g1, g2 = st.columns(2)
with g1:
    st.subheader("⚡ Evolução de Energia")
    st.bar_chart(dados, x="Data", y="Energia (kWh)", color="#2674f1")
with g2:
    st.subheader("💧 Evolução de Água")
    st.line_chart(dados, x="Data", y="Água (m³)", color="#00d4ff")

st.markdown("---")
st.subheader("⚠️ Alertas Operacionais")

alertas = [
    {"Data": (datetime.now() - timedelta(hours=2)).strftime("%d/%m/%Y %H:%M"), "Insumo": "⚡ Energia", "Evento": "Pico de demanda acima do limite.", "Status": "Crítico"},
    {"Data": (datetime.now() - timedelta(hours=14)).strftime("%d/%m/%Y %H:%M"), "Insumo": "💧 Água", "Evento": "Fluxo contínuo detectado na madrugada.", "Status": "Aviso"}
]
st.dataframe(pd.DataFrame(alertas), use_container_width=True, hide_index=True)
