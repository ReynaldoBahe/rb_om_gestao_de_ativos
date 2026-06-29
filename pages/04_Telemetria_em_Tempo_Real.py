import streamlit as st
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# ⚡ SEÇÃO 1: MONITORAMENTO DE ENERGIA (VERTICAL)
# ==============================================================================
st.header("⚡ Monitoramento de Energia")

st.subheader("Parâmetros Elétricos (Potência, Corrente, Fator de Potência)")
# Seu gráfico de linha de energia original entra aqui (ocupando a largura total)

st.markdown("---")

# Filtros e Cartão de Consumo Acumulado de Energia
st.subheader("Consumo de Energia por Período")
col_eng_data1, col_eng_data2, col_eng_card = st.columns(3)

with col_eng_data1:
    data_ini_eng = st.date_input("Data Inicial (Energia)", datetime.date(2026, 6, 22), key="ini_eng")

with col_eng_data2:
    data_fim_eng = st.date_input("Data Final (Energia)", datetime.date(2026, 6, 29), key="fim_eng")

with col_eng_card:
    consumo_acumulado_eng = 1452.8 
    st.metric(label="Consumo Acumulado no Período", value=f"{consumo_acumulado_eng:,} kWh".replace(",", "."))

st.write("**Consumo Integrado (15 min):**")

# --- JANELA SUSPENSA PARA SELEÇÃO DA GRANDEZA ELÉTRICA ---
grandeza_selecionada = st.selectbox(
    "Selecione a grandeza elétrica para o gráfico:",
    ["Potência Ativa (kW)", "Corrente (A)", "Fator de Potência"],
    key="selectbox_grandeza_energia"
)

# Base de tempo simulada de 15 em 15 minutos
datas_simuladas = pd.date_range(start="2026-06-22", end="2026-06-29", freq="15min")
valores_grafico = np.zeros(48)

# Altera os dados simulados com base na grandeza escolhida na janela suspensa
if grandeza_selecionada == "Potência Ativa (kW)":
    valores_grafico = np.random.uniform(45, 60, 48)
    nome_legenda = "Potência (kW)"
elif grandeza_selecionada == "Corrente (A)":
    valores_grafico = np.random.uniform(200, 225, 48)
    nome_legenda = "Corrente (A)"
else:
    valores_grafico = np.random.uniform(0.92, 0.98, 48)
    nome_legenda = "Fator de Potência"

# Gráfico de Colunas de Energia (Laranja) que responde à janela suspensa
fig_colunas_energia = go.Figure()
fig_colunas_energia.add_trace(go.Bar(
    x=datas_simuladas[-48:], 
    y=valores_grafico,
    name=nome_legenda,
    marker_color="#FF4B4B"
))
fig_colunas_energia.update_layout(
    margin=dict(l=20, r=20, t=10, b=10),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=300
)
st.plotly_chart(fig_colunas_energia, use_container_width=True)
