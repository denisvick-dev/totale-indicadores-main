import streamlit as st
import pandas as pd

# Inicializando o login
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

# Tela para teste
if not st.session_state.logado:
   st.title("🔑 Tela de Login")

   with st.form("form_login"):
      usuario = st.text_input("👷 User: ")
      senha = st.text_input("🔑 Pass: ")
      logar = st.form_submit_button("Logar")

      if logar:
        efetuar_login()
else:
   st.title("🚀 Bem-vindo ao Sistema Interno")
   st.write("Esta área só é visível para usuários autenticados.")

   # Botão de Logout na barra lateral
   if st.sidebar.button("Sair / Logout"):
      st.session_state.logado = False
      st.rerun()