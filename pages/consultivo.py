import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import datetime
import calendar
import numpy as np
import time
from streamlit_gsheets import GSheetsConnection

# =========================================
# CONFIGURAÇÃO
# =========================================

st.set_page_config(
    page_title="Consultivos",
    page_icon="📋",
    layout="wide",
)

st.title("📋 Total de Consultivos")

st.divider()

# =========================================
# LEITURA E TRATAMENTO DAS ABAS
# =========================================

if "dados_cons" not in st.session_state:
    st.warning("⚠️ Carregue os dados na página principal primeiro.")
    st.stop()

dados = st.session_state["dados_cons"]

try:
    consultivo = dados["Consultivo"].copy()
except KeyError as erro:
    st.error(f"❌ Aba não encontrada: {erro}")
    st.stop()

consultivo["Qtde. Cons."] = pd.to_numeric(
    consultivo["QTDE_CONSULTIVO"], errors="coerce"
).fillna(0).astype(int)

consultivo["Qtde. Prod."] = pd.to_numeric(
    consultivo["QTDE_PRODUTOS"], errors="coerce"
).fillna(0).astype(int)

df = pd.DataFrame(consultivo)

# =========================================
# Conexão com o Google Sheets
# =========================================
barra_progresso = st.progress(0)

conexao = st.connection("gsheets", type=GSheetsConnection)

# Link da planilha de Ativos
URL_ATIVOS = "https://docs.google.com/spreadsheets/d/1LQKDcLshC6XSXLBVWaEYSpxrro6uydyU9pwDLc38pEg/edit"

try:
    barra_progresso.progress(50)
    with st.spinner("🔁 Sincronizando dados com o Google Sheets..."):
        # Puxa Ativos utilizando o driver gsheets nativo
        df_ativos = conexao.read(spreadsheet=URL_ATIVOS, ttl=0)
        df_ativos.columns = df_ativos.columns.str.strip()
        barra_progresso.progress(100)
        time.sleep(0.5)
        barra_progresso.empty()
except Exception as erro:
    st.error(f"❌ Falha crítica ao conectar com as planilhas: {erro}")
    barra_progresso.empty()
    st.stop()

# =========================================
# MERGE COM OS DADOS DO GOOGLE SHEETS
# =========================================
df["LOGIN NETSALES"] = df["LOGIN NETSALES"].astype(str).str.strip()
df_ativos["Login"] = df_ativos["Login"].astype(str).str.strip()

df_ativos_subset = df_ativos[["Login", "Monitor", "Base"]].drop_duplicates(subset=[
                                                                        "Login"])

df = df.drop(columns=["Monitor", "Base"], errors="ignore")

df = pd.merge(
    df,
    df_ativos_subset,
    left_on="LOGIN NETSALES",
    right_on="Login",
    how="left"
)

df["Monitor"] = df["Monitor"].fillna("Não Identificado").astype(str)
df["Base"] = df["Base"].fillna("Não Identificado").astype(str)

# =========================================
# FILTROS (SIDEBAR)
# =========================================

# Injeção de CSS para personalizar a aparência da Sidebar e dos widgets
st.html("""
    <style>
    /* 1. Altera a cor do texto "Filtros" no topo da Sidebar */
    .stSidebar h2 {
        color: #012869 !important; /* Azul escuro */
        font-size: 26px !important;
        font-weight: 700 !important;
    }

    /* 2. Altera a cor das etiquetas (labels) dos widgets na Sidebar */
    .stSidebar [data-testid="stWidgetLabel"] p {
        color: #000047 !important; /* Azul escuro */
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* 3. Altera a cor de fundo e do texto das TAGS SELECIONADAS no multiselect */
    .stSidebar [data-baseweb="tag"] {
        background-color: #012869 !important; /* Fundo laranja */
        color: #FFFFFF !important; /* Texto branco */
        border-radius: 4px !important;
    }

    /* 4. Altera a cor do ícone de "X" para fechar a tag */
    .stSidebar [data-baseweb="tag"] svg {
        fill: #FFFFFF !important;
    }
    [data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, #FEDBB9, #A15202);
        color: white;
    }
    </style>
    """)

# =========================================
# FILTROS (SIDEBAR) - VERSÃO CORRIGIDA
# =========================================

for coluna in ["Base", "Monitor"]:
    if coluna in df.columns:
        df[coluna] = df[coluna].astype(str).str.strip()
    if coluna in df_ativos.columns:
        df_ativos[coluna] = df_ativos[coluna].astype(str).str.strip()

st.sidebar.header("Filtros")

# FILTRO Base
if "Base" in df.columns:
    bases_disponiveis = sorted(df["Base"].dropna().unique())
    bases_selecionados = st.sidebar.multiselect(
        "Base", options=bases_disponiveis, default=bases_disponiveis
    )
    df = df[df["Base"].isin(bases_selecionados)]
    if "Base" in df_ativos.columns:
        df_ativos = df_ativos[df_ativos["Base"].isin(bases_selecionados)]

# FILTRO Monitor
if "Monitor" in df.columns:
    monitores_disponiveis = sorted(df["Monitor"].dropna().unique())
    monitores_selecionados = st.sidebar.multiselect(
        "Monitor", options=monitores_disponiveis, default=monitores_disponiveis
    )
    df = df[df["Monitor"].isin(monitores_selecionados)]
    if "Monitor" in df_ativos.columns:
        df_ativos = df_ativos[df_ativos["Monitor"].isin(monitores_selecionados)]

# FILTRO Data
if "DATA" in df.columns:
    df["DATA"] = pd.to_datetime(df["DATA"])

    datas_validas = df["DATA"].dropna()

    if not datas_validas.empty:
        data_minima = df["DATA"].min().date()
        data_maxima = df["DATA"].max().date()

        intervalo_datas = st.sidebar.date_input(
            "Selecione o período:",
            value=(data_minima, data_maxima),
            min_value=data_minima,
            max_value=data_maxima,
            format="DD/MM/YYYY"
        )
    
        if isinstance(intervalo_datas, tuple) and len(intervalo_datas) == 2:
            inicial, final = intervalo_datas
            mascara = (df["DATA"].dt.date >= inicial) & (df["DATA"].dt.date <= final)
            df = df.loc[mascara]
    else:
        st.sidebar.warning("**⚠️ Nenhuma data válida encontrada!!**")

# =========================================
# COLORINDO O DATAFRAME
# =========================================


def colorir_projecao(valor):
    # Fundo cinza com letra branca
    return "background-color: grey; color: white; font-weight: bold"


def colorir(valor):
    return "background-color: #F2F2F2; font-weight: bold"  # Fundo cinza claro e negrito

# =========================================
# CRIAÇÃO DA TABELA DE CONSULTIVOS
# =========================================


colunas_obrigatorias = ["LOGIN NETSALES", "VENDEDOR",
                        "Monitor", "Base", "Qtde. Cons.", "Qtde. Prod."]

if all(col in df.columns for col in colunas_obrigatorias):

    total_consultivos = (
        df.groupby(["LOGIN NETSALES", "VENDEDOR", "Monitor", "Base"])[
            ["Qtde. Cons.", "Qtde. Prod."]]
        .sum()
        .reset_index()
        .sort_values("Qtde. Cons.", ascending=False)
    )

    # Inserção da coluna de posição (Ranking)
    total_consultivos.insert(
        0, "Posição", range(1, len(total_consultivos) + 1))

    total_consultivos = total_consultivos.rename(columns={
        "Qtde. Cons.": "Total Consultivos",
        "Qtde. Prod.": "Total Produtos"
    })

    total_consultivos["LOGIN NETSALES"] = total_consultivos["LOGIN NETSALES"].astype(
        str)
    total_consultivos["VENDEDOR"] = total_consultivos["VENDEDOR"].astype(str)
    total_consultivos["Monitor"] = total_consultivos["Monitor"].astype(str)

    total_consultivos["Posição"] = total_consultivos["Posição"].astype(int)
    total_consultivos["Total Consultivos"] = total_consultivos["Total Consultivos"].astype(
        int)
    total_consultivos["Total Produtos"] = total_consultivos["Total Produtos"].astype(
        int)

else:
    st.error(
        "⚠️ As colunas necessárias para o ranking não foram encontradas na base de dados.")
    st.write("**Colunas esperadas:**", colunas_obrigatorias)
    st.write("**Colunas encontradas na sua base:**", list(df.columns))
    st.stop()

# =========================================
# KPIs
# =========================================

col1, col2, col3 = st.columns(3)
col4, col5, col6, col7, col8 = st.columns(5)

equipes_cons = df.groupby("VENDEDOR")["QTDE_CONSULTIVO"].sum().reset_index()
equipes_maiorquezero = equipes_cons[equipes_cons["QTDE_CONSULTIVO"] > 0].shape[0]

total_equipes = df_ativos_subset.shape[0]

qtde_cons = pd.to_numeric(
    consultivo["QTDE_CONSULTIVO"], errors="coerce"
).fillna(0).astype(int).shape[0]

qtde_prod = pd.to_numeric(
    consultivo["QTDE_PRODUTOS"], errors="coerce"
).fillna(0).astype(int).shape[0]

if "Login" in df_ativos.columns:
    total_equipes_filtrado = df_ativos["Login"].dropna().astype(str).str.strip().nunique()
else:
    total_equipes_filtrado = 0

qtde_cons_filtrado = (df[["PLANO TV", "PLANO INTERNET"]] != "-").sum().sum()
qtde_prod_filtrado = df["QTDE_PRODUTOS"] = df["LISTA_PRODUTOS"].apply(len).sum()

try:
    efic = 0
    efic = equipes_maiorquezero / total_equipes_filtrado
except ZeroDivisionError:
    st.sidebar.info("ℹ️ Divisão por zero")

col1.metric("Total de Equipes", f"{total_equipes:,.0f}")
col2.metric("Total Consultivos (Geral)", f"{qtde_cons:,.0f}")
col3.metric("Total Produtos (Geral)", f"{qtde_prod:,.0f}")
col4.metric("Equipes que fizeram Consultivo", f"{equipes_maiorquezero:,.0f}")
col5.metric("Total de Equipes (Filtrado)", f"{total_equipes_filtrado:,.0f}")
col6.metric("Eficiência", f"{efic:,.1%}")
col7.metric("Total Consultivos (Filtrado)", f"{qtde_cons_filtrado:,.0f}")
col8.metric("Total Produtos (Filtrado)", f"{qtde_prod_filtrado:,.0f}")

# =========================================
# EXIBIÇÃO DA TABELA DE CONSULTIVOS
# =========================================

st.subheader("👷 Visão por Técnico")

if not total_consultivos.empty:
    st.dataframe(
        total_consultivos.style.format({
            "Total Consultivos": "{:,.0f}",
            "Total Produtos": "{:,.0f}"
        })
        .map(colorir, subset=["Total Consultivos", "Total Produtos"]),
        use_container_width=False,
        height=500,
        hide_index=True,
        # column_config={
        #    "Posição": st.column_config.NumberColumn("Posição"),
        #    "Total Consultivos": st.column_config.NumberColumn("Qtd. Consultivos", alignment="right"),
        #    "Total Produtos": st.column_config.NumberColumn("Qtd. Produtos", alignment="right")
        # }
    )
else:
    st.info("ℹ️ Nenhum registro encontrado para os filtros selecionados.")
