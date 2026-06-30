import streamlit as st
import pandas as pd

st.title("📁 CARREGAR ARQUIVO DA PRODUÇÃO")
st.write("Suba o seu arquivo Excel aqui para visualizá-lo nas próximas páginas.")

# Inicializa a variável no session_state se ela não existir
if "df_producao" not in st.session_state:
    st.session_state["df_producao"] = None

# Componente de upload de arquivo
arquivo_enviado = st.file_uploader(
    "Escolha um arquivo Excel", type=["xlsx", "xls"])

if arquivo_enviado is not None:
    try:
        # Lendo o arquivo Excel
        df = pd.read_excel(arquivo_enviado)

        # Salvando no session_state para acessar em outras páginas
        st.session_state["df_producao"] = arquivo_enviado

        st.success(
            "✅ Arquivo carregado com sucesso! Vá para a página de Visualização na barra lateral."
        )

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")