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

st.markdown(f'<h2 style="color: #1E3A8A;">📊 Telemetria de Ativos — {nome_cliente}</h2>', unsafe_allow_html=True)
st.write("Monitoramento contínuo e histórico de grandezas elétricas de alta precisão.")

st.markdown("---")

# =========================================================================
# # CENTRAL DE SELEÇÃO DE GRANDEZAS ELÉTRICAS (JANELA SUSPENSA)
# =========================================================================
st.subheader("📈 Análise Histórica das Grandezas")

# Mapeamento dinâmico de cada grandeza com seus valores simulados baseados no tempo
config_grandezas = {
    "Potência Ativa (kW)": {
        "titulo_y": "Potência Ativa (kW)", 
        "valores": [45.2, 46.1, 44.8, 45.5, 47.2, 45.0, 44.2, 45.9, 45.1, 45.3]
    },
    "Potência Aparente (kVA)": {
        "titulo_y": "Potência Aparente (kVA)", 
        "valores": [49.1, 50.2, 48.9, 49.6, 51.3, 49.0, 48.1, 49.9, 49.0, 49.2]
    },
    "Fator de Potência": {
        "titulo_y": "Fator de Potência (cos φ)", 
        "valores": [0.92, 0.92, 0.91, 0.91, 0.92, 0.91, 0.92, 0.92, 0.92, 0.92]
    },
    "Corrente (A)": {
        "titulo_y": "Corrente Nominal (A)", 
        "valores": [68.5, 69.8, 67.9, 68.9, 71.5, 68.2, 67.0, 69.5, 68.3, 68.6]
    }
}

# Janela suspensa para escolha da grandeza
grandeza_selecionada = st.selectbox(
    "Selecione a grandeza elétrica para acompanhamento no gráfico:",
    list(config_grandezas.keys())
)

dados_grandeza = config_grandezas[grandeza_selecionada]

# Estrutura o DataFrame combinando os horários reais com a grandeza escolhida
# Estrutura o DataFrame combinando os horários reais com a grandeza escolhida
dados_sensores = pd.DataFrame({
    'Tempo': pd.date_range(start='2026-06-29 08:00', periods=10, freq='15min'),
    'Valor': dados_grandeza["valores"]
})

# =========================================================================
# # CONSTRUÇÃO DO GRÁFICO REATIVO EM ALTAIR
# =========================================================================
grafico = alt.Chart(dados_sensores).mark_line(color='#1f77b4', point=True).encode(
    x=alt.X('Tempo:T', title='Horário da Leitura'),
    y=alt.Y('Valor:Q', title=dados_grandeza["titulo_y"], scale=alt.Scale(zero=False)),
    tooltip=['Tempo:T', alt.Tooltip('Valor:Q', title=grandeza_selecionada)]
).properties(height=350)

st.altair_chart(grafico, use_container_width=True)
