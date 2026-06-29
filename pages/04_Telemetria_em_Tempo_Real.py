import streamlit as st
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Garanta que a página esteja configurada como "wide" no início do arquivo
# st.set_page_config(layout="wide")

# ==============================================================================
# ⚡ SEÇÃO 1: MONITORAMENTO DE ENERGIA (VERTICAL)
# ==============================================================================
st.header("⚡ Monitoramento de Energia")

st.subheader("Parâmetros Elétricos (Potência, Corrente, Fator de Potência)")
# Seu gráfico de linha de energia original entra aqui (ocupando a largura total)
# Exemplo: st.line_chart(dados_eletricos_classicos)

st.markdown("---")

# Filtros e Cartão de Consumo Acumulado de Energia
st.subheader("Consumo de Energia por Período")
col_eng_data1, col_eng_data2, col_eng_card = st.columns(3)

with col_eng_data1:
    data_ini_eng = st.date_input("Data Inicial (Energia)", datetime.date(2026, 6, 22), key="ini_eng")

with col_eng_data2:
    data_fim_eng = st.date_input("Data Final (Energia)", datetime.date(2026, 6, 29), key="fim_eng")

with col_eng_card:
    # Substitua o valor '1452.8' pelo cálculo da soma do seu dataframe de energia filtrado
    consumo_acumulado_eng = 1452.8 
    st.metric(label="Consumo Acumulado no Período", value=f"{consumo_acumulado_eng:,} kWh".replace(",", "."))

st.write("**Consumo Integrado (15 min):**")

# --- [NOVO] GRÁFICO DE COLUNAS COM AS GRANDEZAS DE ENERGIA ---
# (Simulação dos dados de 15 em 15 minutos - Substitua pelas suas variáveis reais)
datas_energia = pd.date_range(start="2026-06-22", end="2026-06-29", freq="15min")
fig_colunas_energia = go.Figure()

# Adiciona as colunas (barras) para as grandezas elétricas
fig_colunas_energia.add_trace(go.Bar(
    x=datas_energia[-48:], # Exibe as últimas 12 horas para fins visuais
    y=np.random.uniform(45, 60, 48),
    name="Potência Ativa (kW)",
    marker_color="#FF4B4B" # Laranja padrão do seu layout de energia
))

fig_colunas_energia.update_layout(
    margin=dict(l=20, r=20, t=10, b=10),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=300
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
# Seu gráfico de linha de água original entra aqui (ocupando a largura total)
# Exemplo: st.line_chart(dados_agua_classicos)

st.markdown("---")

# Filtros e Cartão de Consumo Acumulado de Água
st.subheader("Consumo de Água por Período")
col_agua_data1, col_agua_data2, col_agua_card = st.columns(3)

with col_agua_data1:
    data_ini_agua = st.date_input("Data Inicial (Água)", datetime.date(2026, 6, 22), key="ini_agua")

with col_agua_data2:
    data_fim_agua = st.date_input("Data Final (Água)", datetime.date(2026, 6, 29), key="fim_agua")

with col_agua_card:
    # Substitua o valor '34.5' pelo cálculo da soma do seu dataframe de água filtrado
    consumo_acumulado_agua = 34.5 
    st.metric(label="Consumo Acumulado no Período", value=f"{consumo_acumulado_agua:,} m³".replace(",", "."))
