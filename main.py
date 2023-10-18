import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import pandas as pd
import os

pd.set_option("display.max_columns", 50)

st.set_page_config(page_title="Ferramenta Analitica de Consumo e Demanda", page_icon=":bar_chart:")

with st.sidebar:
    choose = option_menu("Navegação", ["Tutorial", "Upload de arquivo", "Relatório", "Contato"],
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
    st.subheader(':bar_chart:Tutorial')


elif choose == "Upload de arquivo":
    st.subheader(':bar_chart:Ferramenta Analítica de Consumo e Demanda')
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



elif choose == "Relatório":

    #dados = pd.read_csv("./documento_historico_original.csv",encoding='utf-8', delimiter=';')
    #st.write(dados)
    #st.subheader(':bar_chart:Gráfico de consumo')
    #st.bar_chart(dados[[" Consumo",' Consumo Ponta'," Consumo Fora Ponta"]])

    #Leitura de arquivos
    dados = pd.read_csv("./documento_historico_original.csv", encoding='utf-8', delimiter=';')
    tarifas = pd.read_csv("./tarifas.csv", encoding='utf-8', delimiter=';')

    dcp = 486.00
    dcfp = 540.00

    #azul
    C_P_V = []
    C_FP_V = []
    D_FP_V = []
    U_V = []
    #verde
    C_P_A = []
    C_FP_A = []
    D_P_A = []
    D_FP_A = []
    U_P_A = []
    U_FP_A = []

    for i in range(4):
        #verde
        cp = tarifas['C_P_V'].loc[i]
        cfp = tarifas['C_FP_V'].loc[i]
        tdp = tarifas['D_FP_V'].loc[i]
        tup = tarifas['U_V'].loc[i]
        #azul
        cpa = tarifas['C_P_A'].loc[i]
        cfpa = tarifas['C_FP_A'].loc[i]
        tdpa = tarifas['D_P_A'].loc[i]
        tdfpa = tarifas['D_FP_A'].loc[i]
        tupa = tarifas['U_P_A'].loc[i]
        tufpa = tarifas['U_FP_A'].loc[i]

        # verde

        cp = str(cp)
        cp = cp.replace(",", ".")
        cp = float(cp)

        cfp = str(cfp)
        cfp = cfp.replace(",", ".")
        cfp = float(cfp)

        tdp = str(tdp)
        tdp = tdp.replace(",", ".")
        tdp = float(tdp)

        tup = str(tup)
        tup = tup.replace(",", ".")
        tup = float(tup)

        #azul
        cpa = str(cpa)
        cpa = cpa.replace(",", ".")
        cpa = float(cpa)

        cfpa = str(cfpa)
        cfpa = cfpa.replace(",", ".")
        cfpa = float(cfpa)

        tufpa = str(tufpa)
        tufpa = tufpa.replace(",", ".")
        tufpa = float(tufpa)

        tupa = str(tupa)
        tupa = tupa.replace(",", ".")
        tupa = float(tupa)

        tdpa = str(tdpa)
        tdpa = tdpa.replace(",", ".")
        tdpa = float(tdpa)

        tdfpa = str(tdfpa)
        tdfpa = tdfpa.replace(",", ".")
        tdfpa = float(tdfpa)


        #verde
        C_P_V.append(cp)
        C_FP_V.append(cfp)
        D_FP_V.append(tdp)
        U_V.append(tup)
        #azul
        C_P_A.append(cpa)
        C_FP_A.append(cfpa)
        D_P_A.append(tdpa)
        D_FP_A.append(tdfpa)
        U_P_A.append(tupa)
        U_FP_A.append(tufpa)

    for i in range(12):
        dados[' Demanda Medida Ponta'].loc[i] = str(dados[' Demanda Medida Ponta'].loc[i])
        dados[' Demanda Medida Ponta'].loc[i] = dados[' Demanda Medida Ponta'].loc[i].replace(",", ".")
        dados[' Demanda Medida Ponta'].loc[i] = float(dados[' Demanda Medida Ponta'].loc[i])
        dados[' Demanda Medida fora Ponta'].loc[i] = str(dados[' Demanda Medida fora Ponta'].loc[i])
        dados[' Demanda Medida fora Ponta'].loc[i] = dados[' Demanda Medida fora Ponta'].loc[i].replace(",", ".")
        dados[' Demanda Medida fora Ponta'].loc[i] = float(dados[' Demanda Medida fora Ponta'].loc[i])
        dados[' Consumo Ponta'].loc[i] = str(dados[' Consumo Ponta'].loc[i])
        dados[' Consumo Ponta'].loc[i] = dados[' Consumo Ponta'].loc[i].replace(",", ".")
        dados[' Consumo Ponta'].loc[i] = float(dados[' Consumo Ponta'].loc[i])
        dados[' Consumo Fora Ponta'].loc[i] = str(dados[' Consumo Fora Ponta'].loc[i])
        dados[' Consumo Fora Ponta'].loc[i] = dados[' Consumo Fora Ponta'].loc[i].replace(",", ".")
        dados[' Consumo Fora Ponta'].loc[i] = float(dados[' Consumo Fora Ponta'].loc[i])

    #tarifa verde
    verde_pc = (C_P_V[3]*dados[' Consumo Ponta'])+(C_FP_V[3]*dados[' Consumo Fora Ponta'])
    verde_pd = D_FP_V[3] * dcfp
    dcfp_max = dcfp*1.05
    dcfp_novo = []
    #tem que ser a maior demanda ponta ou fora ponta
    demanda_medida1 = dados[' Demanda Medida Ponta']
    demanda_medida2 = dados[' Demanda Medida fora Ponta']
    demanda = []
    verde_pu = 0
    for i in range(12):
        aux = 0.0
        if demanda_medida1[i] > demanda_medida2[i]:
            demanda = demanda_medida1
        else:
            demanda = demanda_medida2

        if demanda[i] > dcfp_max:
            aux = demanda[i]-dcfp_max
        valor_unico = U_V[3]*(aux)
        verde_pu = verde_pu + valor_unico
    valor_verde = verde_pd+verde_pc+verde_pu
    st.write(valor_verde)

    #tarifa azul
    azul_pc = (C_P_A[0] * dados[' Consumo Ponta']) + (C_FP_A[0] * dados[' Consumo Fora Ponta'])
    azul_pd = (D_P_A[0] * dcp)+(D_FP_A[0] * dcfp)
    azul_pu = (U_P_A[0] * (dados[' Demanda Medida Ponta'] - dcp))+(U_FP_A[0] * (dados[' Demanda Medida fora Ponta'] - dcfp))
    valor_azul = azul_pc+azul_pd+azul_pu
    #st.write(valor_azul)






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