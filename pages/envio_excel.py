import streamlit as st
import pandas as pd
import time
import re
from datetime import datetime, timezone, timedelta

# =========================================
# CONFIGURANDO HORÁRIO DE BRASÍLIA (GMT-3)
# =========================================

fuso = timezone(timedelta(hours=-3))

st.set_page_config(
    page_title="Atualização de Dados",
    page_icon="icons/atualizar-seta.png",
    layout="wide"
)

st.title("🔁 Atualização de Dados")

ID_PLANILHA_PROD = "11Dp9WdZYUrT_LBvfo07Mi8muKXZykU7v"
ID_PLANILHA_CONS = "1RD_A-otPHs40Sas6YNtaT271YqvkOu3W"
ID_PLANILHA_ATIVOS = "1LQKDcLshC6XSXLBVWaEYSpxrro6uydyU9pwDLc38pEg"

URL_EXPORTACAO_PROD = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{ID_PLANILHA_PROD}/export?format=xlsx"
)

URL_EXPORTACAO_CONS = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{ID_PLANILHA_CONS}/export?format=xlsx"
)

URL_EXPORTACAO_ATIVOS = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA_ATIVOS}/export?format=csv"

# -----------------------------
# Session State
# -----------------------------
if "dados_prod" not in st.session_state:
    st.session_state["dados_prod"] = None

if "dados_cons" not in st.session_state:
    st.session_state["dados_cons"] = None

if "dados_ativos" not in st.session_state:
    st.session_state["dados_ativos"] = None

if "ultima_atualizacao" not in st.session_state:
    st.session_state["ultima_atualizacao"] = None

# -----------------------------
# Carregamento
# -----------------------------


@st.cache_data(ttl=300)
def carregar_dados_prod():
    return pd.read_excel(
        URL_EXPORTACAO_PROD,
        sheet_name=None,
        engine="openpyxl"
    )


@st.cache_data(ttl=300)
def carregar_dados_cons():
    return pd.read_excel(
        URL_EXPORTACAO_CONS,
        sheet_name=None,
        engine="openpyxl"
    )


@st.cache_data(ttl=300)
def carregar_dados_ativos():
    df = pd.read_csv(URL_EXPORTACAO_ATIVOS)
    df.columns = df.columns.str.strip()  # Remove espaços extras nas colunas
    return df


def atualizar_dados():

    texto = st.empty()
    barra_progresso = st.progress(0)

    try:
        texto.markdown("⏳ Carregando produção...")
        barra_progresso.progress(20)
        dados_prod = carregar_dados_prod()

        texto.markdown("⏳ Carregando consultivos...")
        barra_progresso.progress(50)
        dados_cons = carregar_dados_cons()

        texto.markdown("⏳ Carregando lista de ativos...")
        barra_progresso.progress(75)
        dados_ativos = carregar_dados_ativos()

        texto.markdown("⚙️ Processando e salvando informações...")
        barra_progresso.progress(90)

        st.session_state["dados_prod"] = dados_prod
        st.session_state["dados_cons"] = dados_cons
        st.session_state["dados_ativos"] = dados_ativos
        st.session_state["ultima_atualizacao"] = datetime.now(fuso)

        barra_progresso.progress(100)
        time.sleep(0.5)
        texto.empty()
        barra_progresso.empty()
        return True

    except Exception as erro:
        texto.empty()
        barra_progresso.empty()
        st.error(f"Erro ao carregar dados: {erro}")
        return False


# Primeira carga automática
if (
    st.session_state["dados_prod"] is None
    and st.session_state["dados_cons"] is None
    and st.session_state["dados_ativos"] is None
):
    atualizar_dados()

# Atualização manual
if st.button("Atualizar Dados", icon="🔁"):

    carregar_dados_prod.clear()
    carregar_dados_cons.clear()
    carregar_dados_ativos.clear()

    if atualizar_dados():
        st.success("✅ Dados atualizados com sucesso!!")


dados_prod = st.session_state["dados_prod"]
dados_cons = st.session_state["dados_cons"]
dados_ativos = st.session_state["dados_ativos"]

prod = dados_prod["Prod"]
cons = dados_cons["Consultivo"]
cons.columns = cons.columns.str.strip()

# =========================================
# CRIAÇÃO DE VARIÁVEIS
# =========================================

# Consultivos
if {"PLANO TV", "PLANO INTERNET"}.issubset(cons.columns):
    cons["QTDE_CONSULTIVO"] = (cons[["PLANO TV", "PLANO INTERNET"]] != "-").sum(axis=1)

# Produtos
if "OBSERVACAO" in cons.columns:
   cons["LISTA_PRODUTOS"] = cons["OBSERVACAO"].astype(str).apply(
      lambda x: re.findall(r"\b\d{10}\b", x)
   )
   cons["QTDE_PRODUTOS"] = cons["LISTA_PRODUTOS"].apply(len)
else:
   cons["LISTA_PRODUTOS"] = [[]] * len(cons)
   cons["QTDE_PRODUTOS"] = 0

# =============================================
# MERGE DA LISTA DE ATIVOS PARA O CONSULTIVO
# =============================================

if "Login" in dados_ativos.columns and "LOGIN NETSALES" in cons.columns:
    cons = pd.merge(
        cons,
        dados_ativos[["Login", "Monitor", "U.N.", "Base"]],
        left_on="LOGIN NETSALES",
        right_on="Login",
        how="left",
    ).drop(columns=["Login"], errors="ignore")

# -----------------------------
# Indicadores - Bloco 1 (Prod)
# -----------------------------

with st.container(border=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Registros (Produção)", len(prod))

    with col2:
        st.metric("Total Colunas (Produção)", len(prod.columns))

    with col3:
        ultima = st.session_state["ultima_atualizacao"]
        st.metric(
            "Última Atualização",
            ultima.strftime("%d/%m/%Y %H:%M:%S")
            if ultima else "-"
        )

st.dataframe(
    prod,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Indicadores - Bloco 2 (Cons)
# -----------------------------

with st.container(border=True):
    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Total Registros (Consultivo)", len(cons))

    with col5:
        st.metric("Total Colunas (Consultivo)", len(cons.columns))

    with col6:
        ultima = st.session_state["ultima_atualizacao"]
        st.metric(
            "Última Atualização",
            ultima.strftime("%d/%m/%Y %H:%M:%S")
            if ultima else "-"
        )

st.dataframe(
    cons,
    use_container_width=True,
    hide_index=True

)
