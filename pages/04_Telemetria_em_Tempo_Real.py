import streamlit as st
import datetime

# Garanta que a página esteja configurada como "wide" no início do arquivo
# st.set_page_config(layout="wide")

# ==============================================================================
# ⚡ SEÇÃO 1: MONITORAMENTO DE ENERGIA (VERTICAL)
# ==============================================================================
st.header("⚡ Monitoramento de Energia")

st.subheader("Parâmetros Elétricos (Potência, Corrente, Fator de Potência)")
# 1. Seu gráfico de linha de energia original entra aqui (ocupando a largura total)
# Exemplo: st.line_chart(dados_eletricos_classicos)

st.markdown("---")

# Filtros e Cartão de Consumo Acumulado de Energia
st.subheader("Consumo de Energia por Período")
col_eng_data1, col_eng_data2, col_eng_card = st.columns([1, 1, 2])

with col_eng_data1:
    data_ini_eng = st.date_input("Data Inicial (Energia)", datetime.date(2026, 6, 22), key="ini_eng")

with col_eng_data2:
    data_fim_eng = st.date_input("Data Final (Energia)", datetime.date(2026, 6, 29), key="fim_eng")

with col_eng_card:
    # Substitua o valor '1452.8' pelo cálculo da soma do seu dataframe de energia filtrado
    consumo_acumulado_eng = 1452.8 
    st.metric(label="Consumo Acumulado no Período", value=f"{consumo_acumulado_eng:,} kWh".replace(",", "."))

st.write("**Consumo Integrado (15 min):**")
# O seu gráfico de barras LARANJA (kWh) entra aqui ocupando a largura inteira abaixo do cartão
# Exemplo: st.bar_chart(dados_energia_filtrados, color="#FF4B4B")


st.markdown("<br><br><br>", unsafe_allow_html=True) # Espaçamento para separar bem as seções


# ==============================================================================
# 💧 SEÇÃO 2: MONITORAMENTO DE ÁGUA (VERTICAL)
# ==============================================================================
st.header("💧 Monitoramento de Água")

st.subheader("Vazão e Parâmetros Hidráulicos")
# 2. Seu gráfico de linha de água original entra aqui (ocupando a largura total)
# Exemplo: st.line_chart(dados_agua_classicos)

st.markdown("---")

# Filtros e Cartão de Consumo Acumulado de Água
st.subheader("Consumo de Água por Período")
col_agua_data1, col_agua_data2, col_agua_card = st.columns([1, 1, 2])

with col_agua_data1:
    data_ini_agua = st.date_input("Data Inicial (Água)", datetime.date(2026, 6, 22), key="ini_agua")

with col_agua_data2:
    data_fim_agua = st.date_input("Data Final (Água)", datetime.date(2026, 6, 29), key="fim_agua")

with col_agua_card:
    # Substitua o valor '34.5' pelo cálculo da soma do seu dataframe de água filtrado
    consumo_acumulado_agua = 34.5 
    st.metric(label="Consumo Acumulado no Período", value=f"{consumo_acumulado_agua:,} m³".replace(",", "."))
