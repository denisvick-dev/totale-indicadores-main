import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ===========================================
# Inicializção da página
# ===========================================

st.set_page_config(
    page_title="Lista de Ativos TOTALE", page_icon="📊", layout="wide"
)

# ===========================================
# Processo de Login
# ===========================================
if "logado" not in st.session_state:
    st.session_state.logado = False

# Criando user para teste
user = "denis"
pwd = "admin"

# Função que faz o login
def efetuar_login():
    if usuario == user and senha == pwd:
        st.session_state.logado = True
        st.success("Login realizado com sucesso")
        st.rerun()  # Recarrega a página
    else:
        st.error("Usuário ou senha incorretos!")

# Criação da tela de login
if not st.session_state.logado:
    st.title("🔑 Tela de Login")

    with st.form("form_login"):
        usuario = st.text_input("👷 User: ")
        senha = st.text_input("🔑 Pass: ", type="password")  # Oculta a senha
        logar = st.form_submit_button("Logar")

        if logar:
            efetuar_login()
else:
    st.title("📊 Lista de Ativos TOTALE")
    st.subheader("Informação puxada via Google Sheets")

    # ===========================================
    # Conexão com Google Sheets
    # ===========================================

    # 1. Inicializa a conexão com o Google Sheets
    conexao = st.connection("gsheets", type=GSheetsConnection)
    URL_ATIVOS = "https://docs.google.com/spreadsheets/d/1LQKDcLshC6XSXLBVWaEYSpxrro6uydyU9pwDLc38pEg/edit"

    # 2. Leitura dos dados com cache e tratamento de erros
    try:
        # ttl=0 garante que os dados sejam buscados em tempo real sem travar no cache
        lista_ativos = conexao.read(spreadsheet=URL_ATIVOS, ttl=0)
        st.success(
            "⚡ Conexão estabelecida e dados sincronizados com o Google Sheets!"
        )
    except Exception as erro:
        st.error(f"❌ Falha crítica ao conectar com a planilha: {erro}")
        lista_ativos = pd.DataFrame()

    # 3. Bloco de exibição e inteligência de dados
    if not lista_ativos.empty:
        # Garante que espaços extras nos nomes das colunas não quebrem os filtros
        lista_ativos.columns = lista_ativos.columns.str.strip()

        # ===========================================
        # KPI's
        # ===========================================

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Registros", len(lista_ativos))
        with col2:
            # Conta quantos técnicos estão explicitamente com a Situação "ATIVO"
            ativos = (
                len(
                    lista_ativos[
                        lista_ativos["Situação"].str.upper() == "ATIVO"
                    ]
                )
                if "Situação" in lista_ativos.columns
                else 0
            )
            st.metric("Técnicos Ativos", ativos)
        with col3:
            # Conta quantos técnicos estão em "FÉRIAS"
            ferias = (
                len(
                    lista_ativos[
                        lista_ativos["Situação"].str.upper() == "FÉRIAS"
                    ]
                )
                if "Situação" in lista_ativos.columns
                else 0
            )
            st.metric("Em Férias", ferias)
        with col4:
            # Conta as bases operacionais distintas
            bases = (
                lista_ativos["Base"].nunique()
                if "Base" in lista_ativos.columns
                else 0
            )
            st.metric("Bases Operadas", bases)

        st.divider()

        # ===========================================
        # Filtros na barra lateral (Sidebars)
        # ===========================================

        st.sidebar.header("🎯 Filtros Avançados")

        # Filtro por Monitor
        if "Monitor" in lista_ativos.columns:
            opcoes_monitor = ["Todos"] + sorted(
                lista_ativos["Monitor"].dropna().unique().tolist()
            )
            monitor_selecionado = st.sidebar.selectbox(
                "Filtrar por Monitor:", opcoes_monitor
            )
            if monitor_selecionado != "Todos":
                lista_ativos = lista_ativos[
                    lista_ativos["Monitor"] == monitor_selecionado
                ]

        # Filtro por Situação (Ativo, Férias, Inoperante)
        if "Situação" in lista_ativos.columns:
            opcoes_situacao = ["Todas"] + sorted(
                lista_ativos["Situação"].dropna().unique().tolist()
            )
            situacao_selecionada = st.sidebar.selectbox(
                "Filtrar por Situação:", opcoes_situacao
            )
            if situacao_selecionada != "Todas":
                lista_ativos = lista_ativos[
                    lista_ativos["Situação"] == situacao_selecionada
                ]

        # --- TABELA FINAL ---
        st.subheader("📋 Dados Atuais Filtrados")
        st.dataframe(lista_ativos, use_container_width=True, hide_index=True)

    else:
        st.info("ℹ️ Nenhum dado foi carregado ou a planilha está vazia.")

# Botão de Logout na barra lateral
if st.sidebar.button("Logout"):
   st.session_state.logado = False
   st.rerun()