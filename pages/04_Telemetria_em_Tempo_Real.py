import streamlit as st

# Se houver um st.set_page_config, mantenha-o como a primeira linha.
# Logo em seguida, cole o bloco abaixo:

# 🔐 TRAVA DE SEGURANÇA
if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    st.error("Acesso negado. Por favor, faca o login na pagina inicial.")
    st.stop()

import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Garanta que a página esteja configurada como "wide" no início do arquivo
# st.set_page_config(layout="wide")
# 🔐 TRAVA DE SEGURANÇA
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Acesso negado. Por favor, faça o login na página inicial.")
    st.stop()


# ==============================================================================
# 🕒 BASE DE TEMPO SIMULADA (15 MINUTOS)
# ==============================================================================
datas_simuladas = pd.date_range(start="2026-06-22", end="2026-06-29", freq="15min")
pontos = 48  # Exibição das últimas 12 horas para fins de relatório visual

# Geração dos relatórios de valores simulados para cada grandeza elétrica
valores_fp = np.random.uniform(0.92, 0.98, pontos)
valores_corrente = np.random.uniform(200, 225, pontos)
valores_demanda = np.random.uniform(40, 58, pontos)
valores_reativa = np.random.uniform(15, 28, pontos)

# ==============================================================================
# ⚡ SEÇÃO 1: MONITORAMENTO DE ENERGIA (VERTICAL)
# ==============================================================================
st.header("⚡ Monitoramento de Energia")

st.subheader("Parâmetros Elétricos (Potência, Corrente, Fator de Potência)")
# Seu gráfico de linha de energia original entra aqui (ocupando a largura total)

st.markdown("---")

# Filtros de Energia
st.subheader("Consumo de Energia por Período")
col_eng_data1, col_eng_data2 = st.columns(2)

with col_eng_data1:
    data_ini_eng = st.date_input("Data Inicial (Energia)", datetime.date(2026, 6, 22), key="ini_eng")

with col_eng_data2:
    data_fim_eng = st.date_input("Data Final (Energia)", datetime.date(2026, 6, 29), key="fim_eng")

st.write("**Consumo Integrado (15 min):**")

# Caixa suspensa oficial de grandezas elétricas
grandeza_selecionada = st.selectbox(
    "Selecione a grandeza elétrica para o gráfico:",
    [
        "Potência Ativa (kW)", 
        "Corrente (A)", 
        "Fator de Potência", 
        "Demanda (kW)", 
        "Potência Reativa (kVAR)"
    ],
    key="selectbox_grandeza_energia"
)

# Lógica que associa a escolha da caixa suspensa aos dados correspondentes
if grandeza_selecionada == "Potência Ativa (kW)":
    valores_grafico = np.random.uniform(45, 60, pontos)
    nome_legenda = "Potência (kW)"
elif grandeza_selecionada == "Corrente (A)":
    valores_grafico = valores_corrente
    nome_legenda = "Corrente (A)"
elif grandeza_selecionada == "Fator de Potência":
    valores_grafico = valores_fp
    nome_legenda = "Fator de Potência"
elif grandeza_selecionada == "Demanda (kW)":
    valores_grafico = valores_demanda
    nome_legenda = "Demanda (kW)"
else:
    valores_grafico = valores_reativa
    nome_legenda = "Potência Reativa (kVAR)"

# RESTAURADO: Gráfico de colunas (barras) laranjas para Energia
fig_colunas_energia = go.Figure()

fig_colunas_energia.add_trace(go.Bar(
    x=datas_simuladas[-pontos:], 
    y=valores_grafico,
    name=nome_legenda,
    marker_color="#FF4B4B"
))

fig_colunas_energia.update_layout(
    margin=dict(l=20, r=20, t=10, b=10),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    height=320
)
st.plotly_chart(fig_colunas_energia, use_container_width=True)


# ==============================================================================
# ↕️ BLOCO DE ESPAÇAMENTO HTML AMPLIAÇÃO (ENTRE AS DUAS SEÇÕES)
# ==============================================================================
st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True) 


# ==============================================================================
# 💧 SEÇÃO 2: MONITORAMENTO DE ÁGUA (VERTICAL)
# ==============================================================================
st.header("💧 Monitoramento de Água")

st.subheader("Vazão e Parâmetros Hidráulicos")

st.markdown("---")

# Filtros de Água
st.subheader("Consumo de Água por Período")
col_agua_data1, col_agua_data2 = st.columns(2)

with col_agua_data1:
    data_ini_agua = st.date_input("Data Inicial (Água)", datetime.date(2026, 6, 22), key="ini_agua")

with col_agua_data2:
    data_fim_agua = st.date_input("Data Final (Água)", datetime.date(2026, 6, 29), key="fim_agua")

st.write("**Consumo Integrado (15 min):**")

# Lógica estritamente crescente mantida para o hidrômetro de água
consumos_pulso_agua = np.random.uniform(0.1, 0.5, pontos)
valores_crescentes_agua = np.cumsum(consumos_pulso_agua) + 20.0

# MODIFICADO: Gráfico de ÁREA preenchida azul e crescente para Água
fig_area_agua = go.Figure()

fig_area_agua.add_trace(go.Scatter(
    x=datas_simuladas[-pontos:], 
    y=valores_crescentes_agua, 
    name="Volume Acumulado (m³)",
    mode='lines',                     # Desenha a linha
    fill='tozeroy',                    # Preenche até o eixo zero
    line=dict(color="#00a3e0", width=2), # Linha do topo em azul
    fillcolor="rgba(0, 163, 224, 0.4)" # Área preenchida com azul translúcido
))

fig_area_agua.update_layout(
    margin=dict(l=20, r=20, t=10, b=10),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=300
)
st.plotly_chart(fig_area_agua, use_container_width=True)
