import calendar
import datetime
from io import BytesIO
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# =========================================
# CONFIGURAÇÃO
# =========================================

st.set_page_config(
    page_title="Consultivos e Ativos TOTALE",
    page_icon="📋",
    layout="wide",
)
st.title("📋 Painel de Controle Consultivos")
st.divider()

# Injeção de CSS para estilizar os Filtros
st.html("""
    <style>
    .stSidebar h2 { color: #012869 !important; font-size: 26px !important; font-weight: 700 !important; }
    .stSidebar [data-testid="stWidgetLabel"] p { color: #000047 !important; font-size: 16px !important; font-weight: 600 !important; }
    .stSidebar [data-baseweb="tag"] { background-color: #F37C04 !important; color: #FFFFFF !important; border-radius: 4px !important; }
    .stSidebar [data-baseweb="tag"] svg { fill: #FFFFFF !important; }
    </style>
    """)

# ===========================================
# Conexão com Google Sheets (Duas Planilhas)
# ===========================================
conexao = st.connection("gsheets", type=GSheetsConnection)

# Links das planilhas
URL_ATIVOS = "https://docs.google.com/spreadsheets/d/1LQKDcLshC6XSXLBVWaEYSpxrro6uydyU9pwDLc38pEg/edit"

# Substitua pelo ID real da sua planilha de Consultivo
ID_CONSULTIVO = "SEU_ID_DA_PLANILHA_CONSULTIVO_AQUI"
URL_CONSULTIVO = f"https://docs.google.com/spreadsheets/d/{ID_CONSULTIVO}/gviz/tq?tqx=out:csv&sheet=Consultivo"

try:
    with st.spinner("Sincronizando dados com o Google Sheets..."):
        # 1. Puxa Ativos utilizando o driver gsheets nativo
        df_ativos = conexao.read(spreadsheet=URL_ATIVOS, ttl=0)
        df_ativos.columns = df_ativos.columns.str.strip()

        # 2. Puxa Consultivos via CSV para ler a aba específica
        df_consultivo_raw = pd.read_csv(URL_CONSULTIVO)
        df_consultivo_raw.columns = df_consultivo_raw.columns.str.strip()

    st.success("⚡ Bases conectadas com sucesso!")
except Exception as erro:
    st.error(f"❌ Falha crítica ao conectar com as planilhas: {erro}")
    st.stop()

# =========================================
# TRATAMENTO DE DADOS & "PROCV" (MERGE)
# =========================================

# Conversão numérica das quantidades
df_consultivo_raw["Qtde. Cons."] = pd.to_numeric(
    df_consultivo_raw["CONSULTIVO"], errors="coerce"
).fillna(0)
df_consultivo_raw["Qtde. Prod."] = pd.to_numeric(
    df_consultivo_raw["PRODUTOS"], errors="coerce"
).fillna(0)

# --- O PROCV ACONTECE AQUI ---
if "Login" in df_ativos.columns and "LOGIN NETSALES" in df_consultivo_raw.columns:
    df_merge = pd.merge(
        df_consultivo_raw,
        df_ativos[["Login", "U.N.", "Base", "Situação"]],
        left_on="LOGIN NETSALES",
        right_on="Login",
        how="left",
    )
else:
    df_merge = df_consultivo_raw.copy()
    st.warning(
        "⚠️ Não foi possível realizar o cruzamento (PROCV). Verifique as colunas de Login."
    )

# =========================================
# FILTROS AVANÇADOS (SIDEBAR)
# =========================================
st.sidebar.header("Filtros")

# Filtro EPO / U.N.
col_epo = "EPO" if "EPO" in df_merge.columns else "U.N."
if col_epo in df_merge.columns:
    epos_disponiveis = sorted(df_merge[col_epo].dropna().unique())
    epos_selecionados = st.sidebar.multiselect(
        "EPO / U.N.", options=epos_disponiveis, default=epos_disponiveis
    )
    df_merge = df_merge[df_merge[col_epo].isin(epos_selecionados)]

# Filtro Monitor
if "MONITOR" in df_merge.columns:
    monitores_disponiveis = sorted(df_merge["MONITOR"].dropna().unique())
    monitores_selecionados = st.sidebar.multiselect(
        "MONITOR", options=monitores_disponiveis, default=monitores_disponiveis
    )
    df_merge = df_merge[df_merge["MONITOR"].isin(monitores_selecionados)]

# Filtro Situação
if "Situação" in df_merge.columns:
    situacoes_disponiveis = ["Todas"] + sorted(
        df_merge["Situação"].dropna().unique().tolist()
    )
    situacao_sel = st.sidebar.selectbox(
        "Filtrar por Situação:", situacoes_disponiveis
    )
    if situacao_sel != "Todas":
        df_merge = df_merge[df_merge["Situação"] == situacao_sel]

# =========================================
# KPI'S DINÂMICOS
# =========================================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Consultivos", f"{df_merge['Qtde. Cons.'].sum():,.0f}")
with col2:
    st.metric("Total Produtos", f"{df_merge['Qtde. Prod.'].sum():,.0f}")
with col3:
    tecnicos_unicos = (
        df_merge["LOGIN NETSALES"].nunique()
        if "LOGIN NETSALES" in df_merge.columns
        else 0
    )
    st.metric("Técnicos na Base", tecnicos_unicos)

st.divider()

# =========================================
# CRIAÇÃO DA TABELA DE RANKING
# =========================================


def colorir(valor):
    return "background-color: #F2F2F2; font-weight: bold"


colunas_obrigatorias = [
    "LOGIN NETSALES",
    "VENDEDOR",
    "MONITOR",
    "Qtde. Cons.",
    "Qtde. Prod.",
]

if all(col in df_merge.columns for col in colunas_obrigatorias):
    total_consultivos = (
        df_merge.groupby(["LOGIN NETSALES", "VENDEDOR", "MONITOR"])[
            ["Qtde. Cons.", "Qtde. Prod."]
        ]
        .sum()
        .reset_index()
        .sort_values("Qtde. Cons.", ascending=False)
    )

    total_consultivos.insert(0, "Posição", range(1, len(total_consultivos) + 1))
    total_consultivos = total_consultivos.rename(
        columns={
            "Qtde. Cons.": "Total Consultivos",
            "Qtde. Prod.": "Total Produtos",
        }
    )

    st.subheader("👷 Visão por Técnico")
    if not total_consultivos.empty:
        st.dataframe(
            total_consultivos.style.format(
                {"Total Consultivos": "{:,.0f}", "Total Produtos": "{:,.0f}"}
            ).map(colorir, subset=["Total Consultivos", "Total Produtos"]),
            use_container_width=True,
            height=500,
            hide_index=True,
        )
    else:
        st.info("ℹ️ Nenhum registro encontrado para os filtros aplicados.")
else:
    st.error("⚠️ Colunas estruturais para geração do ranking não encontradas.")