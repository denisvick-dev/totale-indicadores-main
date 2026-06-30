import streamlit as st
import pandas as pd
import time
from streamlit_carousel import carousel

st.set_page_config(page_title="Home", page_icon="icons/totale.ico", layout="wide")

st.title("PAINEL DE PRODUÇÃO TOTALE")
st.write(
    "Bem-vindo(a) ao painel de produção da TOTALE! Aqui você pode acessar diversos indicadores e análises sobre a produção, além de atualizar os dados para manter tudo sempre atualizado."
)
st.info(
    "ℹ️ Para atualizar os dados, entre em 'Atualização de Dados' na barra lateral e siga as instruções."
)

st.divider()

st.subheader("Informativos e Dicas")

imgs_carrossel = [
    {"img": "images/informe_vagas.jpeg"},
    {"img": "images/consultivo_copa.jpg"},
    {"img": "images/desfile-msp.jpg"},
]

# =====================================
# INICIALIZANDO SESSION STATE
# =====================================

if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0
if "auto_play" not in st.session_state:
    st.session_state.auto_play = True

# =====================================
# CARROSSEL
# =====================================

# Exibição do slide atual
slide_atual = imgs_carrossel[st.session_state.slide_index]
st.image(slide_atual["img"], use_container_width="content")

st.write("")

esquerdo, info, direito = st.columns(3)

with esquerdo:
    if st.button("⏪ Anterior"):
        st.session_state.slide_index = (st.session_state.slide_index - 1) % len(
            imgs_carrossel
        )

with direito:
    if st.button("⏩ Próximo"):
        st.session_state.slide_index = (st.session_state.slide_index + 1) % len(
            imgs_carrossel
        )

with info:
    label_status = "⏸️ Pausar" if st.session_state.auto_play else "▶️ Iniciar"
    if st.button(label_status):
        st.session_state.auto_play = not st.session_state.auto_play
        st.rerun()

# Temporizador
if st.session_state.auto_play:
    # Tempo de espera em segundos entre as transições
    time.sleep(10)

    # Avança para a próxima imagem (retorna a 0 se chegar no final)
    st.session_state.slide_index = (st.session_state.slide_index + 1) % len(
        imgs_carrossel
    )

    # Força a atualização da página para mostrar o novo slide
    st.rerun()
