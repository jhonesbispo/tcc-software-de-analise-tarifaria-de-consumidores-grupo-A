import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from PIL import Image
import numpy as np
import cv2
from PIL import ImageChops
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io
import os
import matplotlib.pyplot as plt
from sklearn import datasets
import yagmail
import sendgrid

pd.set_option("display.max_columns", 50)

st.set_page_config(page_title="Ferramenta Analitica de Consumo e Demanda", page_icon=":bar_chart:")

with st.sidebar:
    choose = option_menu("Navegação", ["Inicio", "Upload de arquivo", "Relatorio", "Contato"],
                         icons=['house', 'upload', 'kanban', 'person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={

                             "menu-title": {"color": "white"},
                             "container": {"padding": "important", "background-color": "#22142b"},
                             "icon": {"color": "#6F0D6D", "font-size": "25px"},
                             "nav-link": {"color": "white","font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#000"},
                             "nav-link-selected": {"background-color": "#02ab21"},
                         }
                         )



if choose == "Inicio":
    st.subheader(':bar_chart:Ferramenta Analitica de Consumo e Demanda')
elif choose == "Upload de arquivo":
    st.subheader(':bar_chart:Ferramenta Analitica de Consumo e Demanda')
    with st.form("my_form"):

        def save_uploadedfile(uploadedfile):
            with open(os.path.join("./", uploadedfile.name), "wb") as f:
                f.write(uploadedfile.getbuffer())
            return ()

        uploaded_file = st.file_uploader("Faça o upload do arquivo excel baixado da energisa",type=['csv'])

        submitted = st.form_submit_button("Enviar")
        if submitted:
            st.success('Enviado com sucesso')

    st.write('\n')
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        df = pd.read_csv(uploaded_file, encoding='utf-8', delimiter=';')
        st.dataframe(df)
        save_uploadedfile(uploaded_file)

elif choose == "Relatorio":

    dados = pd.read_csv("./documento_historico_original.csv",encoding='utf-8', delimiter=';')
    # st.write(dados)
    st.subheader(':bar_chart:Grafico de consumo')
    st.bar_chart(dados[[" Consumo",' Consumo Ponta'," Consumo Fora Ponta"]])


elif choose == "Contato":
    st.subheader(":mailbox: Entre em Contato Com os Desenvolvedores!")

    contact_form = """
        <form action="https://formsubmit.co/jhonesbispo@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Seu nome" required>
                <input type="email" name="email" placeholder="Seu email" required>
                 <textarea name="message" placeholder="Digite sua Mensagem Aqui Doidão"></textarea>
                <button type="submit">Enviar</button>
         </form>
            """
    st.markdown(contact_form, unsafe_allow_html=True,)
    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    local_css("style/style.css")

    # st.subheader(":mailbox: Entre em Contato Com os Desenvolvedores!")
    # with st.form("my_form1"):
    #     Nome = st.text_input("Seu nome")
    #     email = st.text_input("Seu email")
    #     mensagem = st.text_area("Sua mensagem")
    #     botao_enviar = st.form_submit_button("Enviar")
    #     if botao_enviar:
    #
    #         st.success('Enviado com sucesso')
