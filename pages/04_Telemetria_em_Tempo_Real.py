import streamlit as st
import datetime

# Força o Streamlit a usar a largura total da tela (essencial para o lado a lado)
# st.set_page_config(layout="wide")

# ==============================================================================
# SEÇÃO SUPERIOR: OS DOIS BLOCOS LADO A LADO
# ==============================================================================
coluna_esquerda_energia, coluna_direita_agua = st.columns(2)

# ------------------------------------------------------------------------------
# ⚡ LADO ESQUERDO: TODO O BLOCO DE ENERGIA
# ------------------------------------------------------------------------------
with coluna_esquerda_energia:
    st.header("⚡ Monitoramento de Energia")
    
    # Divide o espaço interno: 1 parte para o Período, 2 partes para o Gráfico
    col_eng_filtro, col_eng_grafico = st.columns([1, 2])
    
    with col_eng_filtro:
        st.subheader("Período")
        data_ini_eng = st.date_input("Data Inicial (Energia)", datetime.date(2026, 6, 22), key="ini_eng")
        data_fim_eng = st.date_input("Data Final (Energia)", datetime.date(2026, 6, 29), key="fim_eng")

    with col_eng_grafico:
        st.subheader("Consumo Integrado (15 min)")
        # Insira aqui o seu gráfico de barras LARANJA (kWh)
        # Exemplo: st.bar_chart(dados_energia_filtrados, color="#FF4B4B")


# ------------------------------------------------------------------------------
# 💧 LADO DIREITO: TODO O BLOCO DE ÁGUA
# ------------------------------------------------------------------------------
with coluna_direita_agua:
    st.header("💧 Monitoramento de Água")
    
    # Divide o espaço interno da mesma forma: 1 parte para o Período, 2 partes para o Gráfico
    col_agua_filtro, col_agua_grafico = st.columns([1, 2])
    
    with col_agua_filtro:
        st.subheader("Período")
        data_ini_agua = st.date_input("Data Inicial (Água)", datetime.date(2026, 6, 22), key="ini_agua")
        data_fim_agua = st.date_input("Data Final (Água)", datetime.date(2026, 6, 29), key="fim_agua")

    with col_agua_grafico:
        st.subheader("Consumo Integrado (15 min)")
        # Insira aqui o seu gráfico de barras AZUL (m³)
        # Exemplo: st.bar_chart(dados_agua_filtrados, color="#0000FF")
