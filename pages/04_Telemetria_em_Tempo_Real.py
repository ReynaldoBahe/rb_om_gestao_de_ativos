import streamlit as st
import datetime

# Garanta que a página esteja configurada como "wide" no início do arquivo
# st.set_page_config(layout="wide")

# ==============================================================================
# SEÇÃO DOS BLOCOS LADO A LADO
# ==============================================================================
coluna_esquerda_energia, coluna_direita_agua = st.columns(2)

# ------------------------------------------------------------------------------
# ⚡ LADO ESQUERDO: SETOR DE ENERGIA (Com Filtro e Consumo Integrado)
# ------------------------------------------------------------------------------
with coluna_esquerda_energia:
    st.header("⚡ Monitoramento de Energia")
    
    # Divide o espaço interno: Filtro na esquerda, Gráfico de Barras na direita
    col_eng_filtro, col_eng_grafico = st.columns()
    
    with col_eng_filtro:
        st.subheader("Período")
        data_ini_eng = st.date_input("Data Inicial (Energia)", datetime.date(2026, 6, 22), key="ini_eng")
        data_fim_eng = st.date_input("Data Final (Energia)", datetime.date(2026, 6, 29), key="fim_eng")

    with col_eng_grafico:
        st.subheader("Consumo Integrado (15 min)")
        # Seu gráfico de barras LARANJA (kWh) entra aqui
        # st.bar_chart(dados_energia_filtrados, color="#FF4B4B")


# ------------------------------------------------------------------------------
# 💧 LADO DIREITO: SETOR DE ÁGUA (Apenas monitoramento padrão/histórico)
# ------------------------------------------------------------------------------
with coluna_direita_agua:
    st.header("💧 Monitoramento de Água")
    
    # Aqui entra o seu gráfico ou indicadores originais de água, sem o bloco de 15 min
    st.subheader("Indicadores de Água")
    # Exemplo: st.line_chart(dados_agua_vazao)
