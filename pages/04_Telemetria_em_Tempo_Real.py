# ==============================================================================
# 📊 RODAPÉ: SEÇÃO TOTALMENTE SEPARADA LADO A LADO
# ==============================================================================
coluna_esquerda_energia, coluna_direita_agua = st.columns(2)

# ------------------------------------------------------------------------------
# ⚡ COLUNA DA ESQUERDA: APENAS ENERGIA (Filtro em cima, Barras Laranja embaixo)
# ------------------------------------------------------------------------------
with coluna_esquerda_energia:
    st.subheader("⚡ Consumo de Energia por Período")
    
    # Período organizado na parte superior do bloco para não espremer a tela
    st.write("**Período de Análise:**")
    data_ini_eng = st.date_input("Data Inicial (Energia)", datetime.date(2026, 6, 22), key="ini_eng")
    data_fim_eng = st.date_input("Data Final (Energia)", datetime.date(2026, 6, 29), key="fim_eng")
    
    st.write("**Consumo Integrado (15 min):**")
    # Seu gráfico de barras LARANJA (kWh) entra aqui e ganha toda a largura desta coluna
    # st.bar_chart(dados_energia_filtrados, color="#FF4B4B")


# ------------------------------------------------------------------------------
# 💧 COLUNA DA DIREITA: APENAS ÁGUA (Totalmente independente da esquerda)
# ------------------------------------------------------------------------------
with coluna_direita_agua:
    st.subheader("💧 Monitoramento de Água")
    
    # Seus componentes originais de água entram aqui de forma limpa e isolada
    st.write("Seus gráficos e parâmetros originais de água entram aqui.")
    # Exemplo: st.line_chart(dados_agua_classicos)
