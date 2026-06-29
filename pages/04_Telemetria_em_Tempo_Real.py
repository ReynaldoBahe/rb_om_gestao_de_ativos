import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Telemetria em Tempo Real", page_icon="📊", layout="wide")

# =========================================================================
# # TRAVA DE SEGURANÇA INTEGRADA AO SEU PORTAL
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, faça o login na página inicial.")
    st.stop()

nome_cliente = st.session_state.get("cliente_ativo", "Cliente")

st.markdown(f'<h2 style="color: #1E3A8A;">📊 Telemetria de Ativos & Utilidades — {nome_cliente}</h2>', unsafe_allow_html=True)
st.write("Monitoramento contínuo, histórico de grandezas elétricas e consumo integrado por período.")

st.markdown("---")

# =========================================================================
# # ESTRUTURAÇÃO DOS DADOS DE TELEMETRIA
# =========================================================================
horarios_eixo = pd.date_range(start='2026-06-29 08:00', periods=10, freq='15min')
ultimo_horario_dt = horarios_eixo[-1]
horario_formatado = ultimo_horario_dt.strftime('%H:%M')

valores_potencia = [45.2, 46.1, 44.8, 45.5, 47.2, 45.0, 44.2, 45.9, 45.1, 45.3]
valores_fp = [0.92, 0.92, 0.91, 0.91, 0.92, 0.91, 0.92, 0.92, 0.92, 0.92]
valores_corrente = [68.5, 69.8, 67.9, 68.9, 71.5, 68.2, 67.0, 69.5, 68.3, 68.6]

# Grandezas integradas (consumo acumulado dentro de cada bloco de 15 minutos)
valores_energia_kwh = [11.3, 11.5, 11.2, 11.4, 11.8, 11.2, 11.0, 11.5, 11.3, 11.3]
valores_agua_m3 = [0.3, 0.4, 0.2, 0.5, 0.8, 0.4, 0.3, 0.6, 0.4, 0.4]

potencia_instantanea = valores_potencia[-1]
fp_instantaneo = valores_fp[-1]
corrente_instantanea = valores_corrente[-1]
fluxo_agua_instantaneo = 3.4 # m³/h instantâneo no momento

st.info(f"⏱️ **Última Atualização dos Sensores:** Medições registradas e consolidadas às **{horario_formatado}**.")

# =========================================================================
# # METRICS DE TELEMETRIA AUTOMATIZADOS (INSTANTÂNEOS DO TOPO)
# =========================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Potência Ativa Atual", value=f"{potencia_instantanea} kW", delta="+0.2 kW")
with col2:
    st.metric(label="Fator de Potência Médio", value=f"{fp_instantaneo} cos φ", delta="⚡ Dentro do Limite")
with col3:
    st.metric(label="Corrente Instantânea", value=f"{corrente_instantanea} A", delta="Estável")
with col4:
    st.metric(label="Fluxo de Água Atual", value=f"{fluxo_agua_instantaneo} m³/h", delta="-0.2 m³/h (Economia)")

st.markdown("---")

# =========================================================================
# # SEÇÃO 1: ACOMPANHAMENTO DA GRANDEZA ELÉTRICA (LINHA - COMO ESTAVA ORIGINALMENTE)
# =========================================================================
st.subheader("⚡ 1. Acompanhamento de Grandezas Elétricas (Instantâneas)")

config_grandezas = {
    "Potência Ativa (kW)": {"titulo_y": "Potência Ativa (kW)", "valores": valores_potencia},
    "Potência Aparente (kVA)": {"titulo_y": "Potência Aparente (kVA)", "valores": [49.1, 50.2, 48.9, 49.6, 51.3, 49.0, 48.1, 49.9, 49.0, 49.2]},
    "Fator de Potência": {"titulo_y": "Fator de Potência (cos φ)", "valores": valores_fp},
    "Corrente (A)": {"titulo_y": "Corrente Nominal (A)", "valores": valores_corrente}
}

grandeza_selecionada = st.selectbox(
    "Selecione a grandeza elétrica instantânea para o gráfico de linhas:",
    list(config_grandezas.keys())
)

dados_grandeza = config_grandezas[grandeza_selecionada]

dados_eletricos = pd.DataFrame({
    'Tempo': horarios_eixo,
    'Valor': dados_grandeza["valores"]
})

grafico_eletrico = alt.Chart(dados_eletricos).mark_line(color='#1f77b4', point=True).encode(
    x=alt.X('Tempo:T', title='Horário da Leitura', axis=alt.Axis(format='%H:%M', values=list(dados_eletricos['Tempo']))),
    y=alt.Y('Valor:Q', title=dados_grandeza["titulo_y"], scale=alt.Scale(zero=False)),
    tooltip=[alt.Tooltip('Tempo:T', format='%H:%M', title='Horário'), alt.Tooltip('Valor:Q', title=grandeza_selecionada)]
).properties(height=280)

st.altair_chart(grafico_eletrico, use_container_width=True)

st.markdown("---")

# =========================================================================
# # SEÇÃO 2: CONSUMO ACUMULADO POR PERÍODO LADO A LADO (BARRAS)
# =========================================================================
st.subheader("📊 2. Consumo Acumulado por Período de Medição (15 Minutos)")

# Criação das duas colunas na tela para exibir os gráficos lado a lado
col_esq, col_dir = st.columns(2)

with col_esq:
    st.markdown("🔌 **Consumo de Energia Ativa (kWh)**")
    dados_energia_periodo = pd.DataFrame({
        'Tempo': horarios_eixo,
        'Consumo': valores_energia_kwh
    })
    
    # Gráfico de barras para consumo elétrico acumulado no intervalo (ideal para dados do CCK90)
    grafico_energia_barra = alt.Chart(dados_energia_periodo).mark_bar(color='#F59E0B', cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X('Tempo:T', title='Período', axis=alt.Axis(format='%H:%M', values=list(dados_energia_periodo['Tempo']))),
        y=alt.Y('Consumo:Q', title='Energia Consumida (kWh)'),
        tooltip=[alt.Tooltip('Tempo:T', format='%H:%M', title='Período'), alt.Tooltip('Consumo:Q', title='Energia (kWh)')]
    ).properties(height=250)
    st.altair_chart(grafico_energia_barra, use_container_width=True)

with col_dir:
    st.markdown("💧 **Consumo de Volume Hídrico (m³)**")
    dados_agua_periodo = pd.DataFrame({
        'Tempo': horarios_eixo,
        'Consumo': valores_agua_m3
    })
    
    # Gráfico de barras para consumo de água acumulado no intervalo
    grafico_agua_barra = alt.Chart(dados_agua_periodo).mark_bar(color='#2563EB', cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X('Tempo:T', title='Período', axis=alt.Axis(format='%H:%M', values=list(dados_agua_periodo['Tempo']))),
        y=alt.Y('Consumo:Q', title='Volume Consumido (m³)'),
        tooltip=[alt.Tooltip('Tempo:T', format='%H:%M', title='Período'), alt.Tooltip('Consumo:Q', title='Volume (m³)')]
    ).properties(height=250)
    st.altair_chart(grafico_agua_barra, use_container_width=True)

st.set_page_config(page_title="Telemetria em Tempo Real", page_icon="📊", layout="wide")

# =========================================================================
# # TRAVA DE SEGURANÇA INTEGRADA AO SEU PORTAL
# =========================================================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Acesso negado. Por favor, faça o login na página inicial.")
    st.stop()

nome_cliente = st.session_state.get("cliente_ativo", "Cliente")

st.markdown(f'<h2 style="color: #1E3A8A;">📊 Telemetria de Ativos & Utilidades — {nome_cliente}</h2>', unsafe_allow_html=True)
st.write("Monitoramento contínuo e histórico de grandezas elétricas e consumo hídrico acumulado.")

st.markdown("---")

# =========================================================================
# # ESTRUTURAÇÃO DOS DADOS REAIS DE TELEMETRIA (A CADA 15 MINUTOS)
# =========================================================================
horarios_eixo = pd.date_range(start='2026-06-29 08:00', periods=10, freq='15min')
ultimo_horario_dt = horarios_eixo[-1]
horario_formatado = ultimo_horario_dt.strftime('%H:%M')

valores_potencia = [45.2, 46.1, 44.8, 45.5, 47.2, 45.0, 44.2, 45.9, 45.1, 45.3]
valores_fp = [0.92, 0.92, 0.91, 0.91, 0.92, 0.91, 0.92, 0.92, 0.92, 0.92]
valores_corrente = [68.5, 69.8, 67.9, 68.9, 71.5, 68.2, 67.0, 69.5, 68.3, 68.6]

# 💧 Valores discretos de consumo de água dentro de cada bloco de 15 minutos (m³)
valores_agua_periodo = [0.3, 0.4, 0.2, 0.5, 0.8, 0.4, 0.3, 0.6, 0.4, 0.4]
consumo_total_agua = sum(valores_agua_periodo) # Grandeza integrada (acumulada total)

potencia_instantanea = valores_potencia[-1]
fp_instantaneo = valores_fp[-1]
corrente_instantanea = valores_corrente[-1]

st.info(f"⏱️ **Última Atualização dos Sensores:** Medições registradas e consolidadas às **{horario_formatado}**.")

# =========================================================================
# # METRICS DE TELEMETRIA AUTOMATIZADOS (INSTANTÂNEOS + ACUMULADO)
# =========================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Potência Ativa Atual", value=f"{potencia_instantanea} kW", delta="+0.2 kW")
with col2:
    st.metric(label="Fator de Potência Médio", value=f"{fp_instantaneo} cos φ", delta="⚡ Dentro do Limite")
with col3:
    st.metric(label="Corrente Instantânea", value=f"{corrente_instantanea} A", delta="Estável")
with col4:
    # 🎯 CARD DE GRANDEZA ACUMULADA TOTAL DO PERÍODO
    st.metric(label="Consumo Total Acumulado", value=f"{consumo_total_agua:.1f} m³", delta="Consolidação do Turno")

st.markdown("---")

# =========================================================================
# # SEÇÃO 1: ACOMPANHAMENTO DA GRANDEZA ELÉTRICA (LINHA)
# =========================================================================
st.subheader("⚡ 1. Acompanhamento de Grandezas Elétricas (Instantâneas)")

config_grandezas = {
    "Potência Ativa (kW)": {"titulo_y": "Potência Ativa (kW)", "valores": valores_potencia},
    "Potência Aparente (kVA)": {"titulo_y": "Potência Aparente (kVA)", "valores": [49.1, 50.2, 48.9, 49.6, 51.3, 49.0, 48.1, 49.9, 49.0, 49.2]},
    "Fator de Potência": {"titulo_y": "Fator de Potência (cos φ)", "valores": valores_fp},
    "Corrente (A)": {"titulo_y": "Corrente Nominal (A)", "valores": valores_corrente}
}

grandeza_selecionada = st.selectbox(
    "Selecione a grandeza elétrica instantânea para o gráfico:",
    list(config_grandezas.keys())
)

dados_grandeza = config_grandezas[grandeza_selecionada]

dados_eletricos = pd.DataFrame({
    'Tempo': horarios_eixo,
    'Valor': dados_grandeza["valores"]
})

grafico_eletrico = alt.Chart(dados_eletricos).mark_line(color='#1f77b4', point=True).encode(
    x=alt.X('Tempo:T', title='Horário da Leitura', axis=alt.Axis(format='%H:%M', values=list(dados_eletricos['Tempo']))),
    y=alt.Y('Valor:Q', title=dados_grandeza["titulo_y"], scale=alt.Scale(zero=False)),
    tooltip=[alt.Tooltip('Tempo:T', format='%H:%M', title='Horário'), alt.Tooltip('Valor:Q', title=grandeza_selecionada)]
).properties(height=280)

st.altair_chart(grafico_eletrico, use_container_width=True)

st.markdown("---")

# =========================================================================
# # SEÇÃO 2: ACOMPANHAMENTO DE GRANDEZA ACUMULADA POR PERÍODO (BARRA)
# =========================================================================
st.subheader("💧 2. Consumo de Água Acumulado por Período")

# Janela suspensa para simular a mudança de agrupamento
janela_tempo = st.selectbox(
    "Agrupar consumo acumulado por:",
    ["Blocos de 15 Minutos (Leitura Direta)", "Consolidado por Hora (Soma Integrada)"]
)

if "Hora" in janela_tempo:
    # Simulação de agrupamento de dados somados por hora cheia
    dados_agua = pd.DataFrame({
        'Tempo': pd.date_range(start='2026-06-29 08:00', periods=3, freq='h'),
        'Consumo': [1.4, 1.7, 1.2] # Soma dos blocos de 15 minutos dentro de cada hora
    })
    formato_eixo = '%H:00'
else:
    # Blocos padrão de 15 minutos
    dados_agua = pd.DataFrame({
        'Tempo': horarios_eixo,
        'Consumo': valores_agua_periodo
    })
    formato_eixo = '%H:%M'

# 📊 Gráfico de barras: O modelo padrão internacional para registrar consumo por período
grafico_agua = alt.Chart(dados_agua).mark_bar(color='#2563EB', cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
    x=alt.X('Tempo:T', 
            title='Período de Medição',
            axis=alt.Axis(format=formato_eixo, values=list(dados_agua['Tempo']))),
    y=alt.Y('Consumo:Q', title='Volume Consumido no Intervalo (m³)'),
    tooltip=[alt.Tooltip('Tempo:T', format=formato_eixo, title='Período'), alt.Tooltip('Consumo:Q', title='Consumo (m³)')]
).properties(height=280)

st.altair_chart(grafico_agua, use_container_width=True)
