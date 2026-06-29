import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Telemetria em Tempo Real", page_icon="📊", layout="wide")

st.markdown('<h2 style="color: #1E3A8A;">📊 Telemetria de Ativos em Tempo Real</h2>', unsafe_allow_html=True)
st.write("Monitoramento contínuo de vibração, temperatura e corrente dos equipamentos hospitalares.")

# Simulação de dados de sensores (IoT)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Temperatura do Chiller", value="7.2 °C", delta="-0.4 °C (Estável)")
with col2:
    st.metric(label="Vibração Geral (MM/S)", value="1.8 mm/s", delta="⚡ Dentro do Limite")
with col3:
    st.metric(label="Corrente Nominal (A)", value="42 A", delta="⚠️ Pico Recente", delta_color="inverse")

st.markdown("---")
st.subheader("📈 Histórico Recente de Sensores")

# Dados simulados para o gráfico
dados_sensores = pd.DataFrame({
    'Tempo': pd.date_range(start='2026-06-29 08:00', periods=10, freq='min'),
    'Temperatura (°C)': [7.5, 7.4, 7.2, 7.3, 7.5, 7.2, 7.1, 7.3, 7.2, 7.2]
})

grafico = alt.Chart(dados_sensores).mark_line(color='#1f77b4', point=True).encode(
    x=alt.X('Tempo:T', title='Horário da Leitura'),
    y=alt.Y('Temperatura (°C):Q', title='Temperatura (°C)', scale=alt.Scale(domain=[6, 9])),
    tooltip=['Tempo:T', 'Temperatura (°C):Q']
).properties(height=300)

st.altair_chart(grafico, use_container_width=True)
