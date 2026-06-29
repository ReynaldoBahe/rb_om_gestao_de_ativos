import streamlit as st
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Garanta que a página esteja configurada como "wide" no início do arquivo
# st.set_page_config(layout="wide")

# ==============================================================================
# 🕒 GERAÇÃO DE DADOS SIMULADOS (A CADA 15 MINUTOS)
# ==============================================================================
# Cria uma janela de tempo de 7 dias com intervalos de 15 minutos
datas_simuladas = pd.date_range(start="2026-06-22", end="2026-06-29", freq="15min")
total_pontos = len(datas_simuladas)

# ==============================================================================
# ⚡ SEÇÃO 1: MONITORAMENTO DE ENERGIA (VERTICAL)
# ==============================================================================
st.header("⚡ Monitoramento de Energia")

st.subheader("Parâmetros Elétricos (Potência, Corrente, Fator de Potência)")

# --- [NOVO] GRÁFICO DE LINHA SIMULADO - ENERGIA (15 MIN) ---
fig_linha_energia = go.Figure()
fig_linha_energia.add_trace(go.Scatter(
    x=datas_simuladas, 
    y=np.random.uniform(50, 65, total_pontos), 
    name="Potência (kW)", 
    line=dict(color="#1f77b4", width=2)
))
fig_linha_energia.add_trace(go.Scatter(
    x=datas_simuladas, 
    y=np.random.uniform(200, 225, total_pontos), 
    name="Corrente (A)", 
    line=dict(color="#636efa", width=1.5)
))
fig_linha_energia.add_trace(go.Scatter(
    x=datas_simuladas, 
    y=np.random.uniform(0.92, 0.98, total_pontos), 
    name="Fator de Potência", 
    line=dict(color="#00cc96", width=1.5)
))
fig_linha_energia.update_layout(
    margin=dict(l=20, r=20, t=10, b=10),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=300
)
st.plotly_chart(fig_linha_energia, use_container_width=True)

st.markdown("---")

# Filtros e Cartão de Consumo Acumulado de Energia (IGUAL AO SEU LAYOUT)
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
# Gráfico de Barras Laranja Mantido Abaixo
fig_barra_energia = go.Figure(go.Bar(
    x=datas_simuladas[-48:], # exibe as últimas 12 horas para fins visuais
    y=np.random.uniform(5, 15, 48), 
    marker_color="#FF4B4B"
))
fig_barra_energia.update_layout(margin=dict(l=20, r=20, t=10, b=10), height=200)
st.plotly_chart(fig_barra_energia, use_container_width=True)


st.markdown("<br><br><br>", unsafe_allow_html=True) # Espaçamento separador


# ==============================================================================
# 💧 SEÇÃO 2: MONITORAMENTO DE ÁGUA (VERTICAL)
# ==============================================================================
st.header("💧 Monitoramento de Água")

st.subheader("Vazão e Parâmetros Hidráulicos")

# --- [NOVO] GRÁFICO DE LINHA SIMULADO - ÁGUA (15 MIN) ---
fig_linha_agua = go.Figure()
fig_linha_agua.add_trace(go.Scatter(
    x=datas_simuladas, 
    y=np.random.uniform(2.5, 4.5, total_pontos), 
    name="Vazão (m³/h)", 
    line=dict(color="#00a3e0", width=2)
))
fig_linha_agua.add_trace(go.Scatter(
    x=datas_simuladas, 
    y=np.random.uniform(1.8, 2.8, total_pontos), 
    name="Pressão (mca)", 
    line=dict(color="#005587", width=1.5)
))
fig_linha_agua.update_layout(
    margin=dict(l=20, r=20, t=10, b=10),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=300
)
st.plotly_chart(fig_linha_agua, use_container_width=True)

st.markdown("---")

# Filtros e Cartão de Consumo Acumulado de Água (IGUAL AO SEU LAYOUT)
st.subheader("Consumo de Água por Período")
col_agua_data1, col_agua_data2, col_agua_card = st.columns(3)

with col_agua_data1:
    data_ini_agua = st.date_input("Data Inicial (Água)", datetime.date(2026, 6, 22), key="ini_agua")

with col_agua_data2:
    data_fim_agua = st.date_input("Data Final (Água)", datetime.date(2026, 6, 29), key="fim_agua")

with col_agua_card:
    consumo_acumulado_agua = 34.5 
    st.metric(label="Consumo Acumulado no Período", value=f"{consumo_acumulado_agua:,} m³".replace(",", "."))
