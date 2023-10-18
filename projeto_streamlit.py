import streamlit as st
from streamlit_option_menu import option_menu
import math
#import streamlit.components.v1 as html
import numpy as np
import cv2
from PIL import Image
#from PIL import ImageChops
import pandas as pd
#from st_aggrid import AgGrid
#import plotly.express as px
#import io
import os
import matplotlib.pyplot as plt
#from sklearn import datasets
#import yagmail
#import sendgrid
import locale
import imageio

if 'opt' not in st.session_state:
    st.session_state.opt = None
if 'number1' not in st.session_state:
    st.session_state.number1 = 0.0
if 'number2' not in st.session_state:
    st.session_state.number2 = 0.0
if 'sub1' not in st.session_state:
    st.session_state.sub1 = None
#if 'uploadedfile' not in st.session_state:
    #st.session_state.uploadedfile = None


pd.set_option("display.max_columns", 50)

st.set_page_config(layout="centered",page_title="Ferramenta Analitica de Consumo e Demanda", page_icon=":bar_chart:")

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



if choose == "Tutorial":
    st.header('Tutorial de Utilização da Ferramenta')
    st.write('A utilização da ferramenta consiste em dois passos, entradas dos dados atuais e depois a parte de relátorio')
    st.write('Para começar a utilizar a ferramenta precisamos escolher o modelo tarifário atualmente contratado:')
    video_file = open('modelo_tar.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    st.write('Logo após, digitar a(s) demanda(s) contratadas atualmente:')
    video_file = open('demanda_contratada.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    st.write('Depois, escolher o subgrupo atualmente inserido:')
    video_file = open('subgrupo.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    st.write('E por fim, realizar o upload do arquivo com os dados:')
    video_file = open('Modelo_tar.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    st.write('O arquivo tem o seguinte formato:')
    image = Image.open('modelo_img.jpg')
    st.image(image, caption='Modelo de entrada de dados')

    modelo_entrada_dados = pd.read_csv("./modelo_entrada_dados.csv")
    @st.cache
    def convert_df(modelo_entrada_dados):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return modelo_entrada_dados.to_csv().encode('utf-8')


    csv = convert_df(modelo_entrada_dados)
    st.write('E pode ser baixado clicando no botão logo abaixo:')
    st.download_button(
        label="Download do modelo de entrada de dados",
        data=csv,
        file_name='modelo_entrada_dados.csv',
        mime='text/csv',
    )
elif choose == "Upload de arquivo":

    st.subheader('Ferramenta Analítica de Consumo e Demanda')

    # Selecionar a tarifação atual
    st.session_state.opt = st.selectbox(
        'Qual sua tarifação atual?',
        ('Horo-Sazional Verde', 'Horo-Sazional Azul'),
    )
    st.write('Sua seleção foi:', st.session_state.opt)

    if st.session_state.opt == 'Horo-Sazional Azul':

        # Informar a demanda contratada atualmente
        st.session_state.number1 = st.number_input('Insira a sua demanda contrada atualmente Ponta')
        st.write('A demanda atual é ',st.session_state.number1)
        st.session_state.number2 = st.number_input('Insira a sua demanda contrada atualmente Fora Ponta')
        st.write('A demanda atual é ',st.session_state.number2)
    else:
        st.session_state.number1 = st.number_input('Insira a sua demanda contrada atualmente Ponta')
        st.write('A demanda atual é ',st.session_state.number1)

    # Selecionar a tarifação atual
    st.session_state.sub1 = st.selectbox(
            'Qual seu Subgrupo A4 (V=13,8kV)?',
            ('Sub-classes Demais ', 'Rural','Rural Irrigação','Serviço público'),
        )
    st.write('Sua seleção foi:', st.session_state.sub1)
    if st.session_state.sub1 == 'Sub-classes Demais ':
        st.session_state.indice = 0
    elif st.session_state.sub1 == 'Rural':
        st.session_state.indice = 1
    elif st.session_state.sub1 == 'Rural Irrigação':
        st.session_state.indice = 2
    elif st.session_state.sub1 == 'Serviço público':
        st.session_state.indice = 3

    with st.form("my_form"):

        def save_uploadedfile(uploadedfile):
            with open(os.path.join("./", uploadedfile.name), "wb") as f:
                f.write(uploadedfile.getbuffer())
            return ()

        st.session_state.uploaded_file = st.file_uploader("Faça o upload do arquivo excel baixado da energisa",type=['csv'])

        submitted = st.form_submit_button("Enviar")
        if submitted:
            st.success('Enviado com sucesso')

    st.write('\n')
    df = None
    if st.session_state.uploaded_file is not None:
        file_details = {"FileName": st.session_state.uploaded_file.name, "FileType": st.session_state.uploaded_file.type}
        df = pd.read_csv(st.session_state.uploaded_file, encoding='utf-8', delimiter=';')
        st.dataframe(df)
        save_uploadedfile(st.session_state.uploaded_file)

    st.session_state.df = df


elif choose == "Relatório":

    #dados = pd.read_csv("./documento_historico_original.csv",encoding='utf-8', delimiter=';')
    #st.write(dados)
    #st.subheader(':bar_chart:Gráfico de consumo')
    #st.bar_chart(dados[[" Consumo",' Consumo Ponta'," Consumo Fora Ponta"]])

    #Leitura de arquivos
    #df = pd.read_csv("./documento_historico_original.csv", encoding='utf-8', delimiter=';')
    #st.write(st.session_state.uploaded_file)
    dados = st.session_state.df

    tarifas = pd.read_csv("./tarifas.csv", encoding='utf-8', delimiter=';')
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    # CORREÇÃO DO FATOR DE POTÊNCIA

    ## PASSOS:

    # - IMPORTAR BIBLIOTECAS
    # - LER CSV
    # - ANALISAR COLUNAS
    # - OPERAR COLUNAS
    # - OBTER CORREÇÃO DO FATOR DE POTÊNCIA

    ### IMPORTANDO BIBLIOTECAS

    ### LENDO CSV E TRATANDO COLUNAS

    tabela = st.session_state.df

    colunas = [' Ano', ' Leitura Ponta', ' Leitura Fora Ponta', ' Dias',
               ' Consumo', ' Consumo Ponta', ' Consumo Fora Ponta', ' Consumo Reativo Ponta',
               ' Consumo Reativo Fora Ponta', ' Demanda Medida Ponta', ' Demanda Faturada Ponta',
               ' Demanda Excedente Ponta', ' Fator Potência Ponta', ' Fator Potência Fora Ponta',
               ]

    QUANTIDADE_DE_MESES = tabela.shape[0]

    ##print(f'A análise será feita dentro de {QUANTIDADE_DE_MESES} meses')

    for coluna in colunas:

        for i in range(QUANTIDADE_DE_MESES):
            tabela[coluna].loc[i] = str(tabela[coluna].loc[i])
            tabela[coluna].loc[i] = tabela[coluna].loc[i].replace(",", ".")
            tabela[coluna].loc[i] = float(tabela[coluna].loc[i])

        tabela[[coluna]].astype(np.dtype('float32'))

    # display(tabela.dtypes)

    for i in range(QUANTIDADE_DE_MESES):
        if tabela[' Demanda Contratada Ponta'].loc[i] == ' -':
            tabela[' Demanda Contratada Ponta'].loc[i] = 0

    # display(tabela[[' Demanda Contratada Ponta']])

    # display(tabela)

    ### CÁCULO

    FP_CORRIGIDO = 0.92
    i = 0

    coluna_potencia_aparente = []
    coluna_potencia_reativa = []
    coluna_potencia_aparente_corrigida = []
    coluna_potencia_reativa_corrigida = []
    coluna_potencia_banco_capacitores = []
    coluna_FP = []
    coluna_FP_corrigido = []
    for potencia_ativa in tabela[' Consumo']:

        # CÁLCULO DA POTÊNCIA APARENTE MEDIDA
        potencia_reativa = tabela[' Consumo Reativo Ponta'][i] + tabela[' Consumo Reativo Fora Ponta'][i]
        potencia_aparente = ((potencia_ativa)**2 + (potencia_reativa)**2)**(1 / 2)

        # CÁLCULO DO FATOR DE POTÊNCIA
        FP = potencia_ativa / potencia_aparente
        # CÁLCULO DO ANGULO EM RADIANOS
        angulo_radianos_fp = math.acos(FP)

        # FP = tabela[' Fator Potência Ponta'][i]
        # potencia_aparente = potencia_ativa / FP
        # potencia_reativa = potencia_aparente * math.sin(angulo_radianos_fp)

        # CÁLCULO DA POTÊNCIA APARENTE CORRIGIDA NA PONTA
        if 0.92 < FP > -0.92:
            potencia_aparente_corrigida = potencia_aparente
        else:
            potencia_aparente_corrigida = potencia_ativa / FP_CORRIGIDO

        # CÁLCULO DA POTÊNCIA REATIVA CORRIGIDA NA PONTA
        angulo_radianos_fp_corrigida = math.acos(FP_CORRIGIDO)
        if 0.92 < FP > -0.92:
            potencia_reativa_corrigida = potencia_reativa
        else:
            potencia_reativa_corrigida = potencia_aparente_corrigida * math.sin(angulo_radianos_fp_corrigida)

        # CÁLCULO DA POTÊNCIA REATIVA DO BANCO DE CAPACITORES
        Potencia_reativa_inicial = potencia_reativa
        Potencia_reativa_final = potencia_reativa_corrigida
        POTENCIA_REATIVA_BANCO_DE_CAPACITORES = Potencia_reativa_final - Potencia_reativa_inicial

        # ADICONANDO VALORES EM SUAS RESPECITIVAS LISTAS
        coluna_potencia_aparente.append(potencia_aparente)
        coluna_potencia_reativa.append(potencia_reativa)
        coluna_potencia_aparente_corrigida.append(potencia_aparente_corrigida)
        coluna_potencia_reativa_corrigida.append(potencia_reativa_corrigida)
        coluna_FP.append(FP)
        coluna_FP_corrigido.append(FP_CORRIGIDO)

        if 0.92 < FP > -0.92:
            coluna_potencia_banco_capacitores.append(0)
        else:
            coluna_potencia_banco_capacitores.append(POTENCIA_REATIVA_BANCO_DE_CAPACITORES)

        i = i + 1

    # print(f'potencia aparente medida ponta: {coluna_potencia_aparente} KVA')

    # print(f'potencia reativa medida ponta: {coluna_potencia_reativa} KVAr')

    # print(f'potencia aparente corrigida ponta: {coluna_potencia_aparente_corrigida} KVA')

    # print(f'potencia reativa após a correção ponta: {coluna_potencia_reativa_corrigida} KVA')

    # print(f'POTENCIA_REATIVA_BANCO_DE_CAPACITORES: {coluna_potencia_banco_capacitores} KVAr')

    ### CRIANDO DICIONÁRIOS E ADICIONANDO NO DATAFRAME

    ### CRIANDO DICIONÁRIOS E ADICIONANDO NO DATAFRAME

    tabela['BANCO DE CAPACITORES'] = coluna_potencia_banco_capacitores

    # display(tabela)

    banco_capacitores = 0

    for i in range(QUANTIDADE_DE_MESES):
        if tabela['BANCO DE CAPACITORES'][i] < banco_capacitores:
            banco_capacitores = tabela['BANCO DE CAPACITORES'][i]

    # print(banco_capacitores)

    tabela_resultado = pd.DataFrame({'MES': tabela['Mes']})
    tabela_resultado['ANO'] = tabela[' Ano'].astype(np.dtype('int32'))
    tabela_resultado['POTENCIA_ATIVA(W)'] = tabela[' Consumo']
    tabela_resultado['POTENCIA_APARENTE(VA)'] = coluna_potencia_aparente
    tabela_resultado['POTENCIA_REATIVA(VAr)'] = coluna_potencia_reativa
    tabela_resultado['FP'] = coluna_FP

    tabela_resultado_corrigido = pd.DataFrame({'MES': tabela['Mes']})
    tabela_resultado_corrigido['ANO'] = tabela[' Ano'].astype(np.dtype('int32'))
    tabela_resultado_corrigido['POTENCIA_APARENTE(VA)'] = coluna_potencia_aparente_corrigida
    tabela_resultado_corrigido['POTENCIA_REATIVA (VAr)'] = coluna_potencia_reativa_corrigida
    tabela_resultado_corrigido['BANCO_DE_CAPACITORES(VAr)'] = coluna_potencia_banco_capacitores

    tabela_resultado_corrigido['FP_CORRIGIDO'] = [FP_CORRIGIDO, FP_CORRIGIDO, FP_CORRIGIDO, FP_CORRIGIDO, FP_CORRIGIDO,
                                                  FP_CORRIGIDO, FP_CORRIGIDO, FP_CORRIGIDO, FP_CORRIGIDO, FP_CORRIGIDO,
                                                  FP_CORRIGIDO, FP_CORRIGIDO]

    #display(tabela_resultado)
    #display(tabela_resultado_corrigido)

    # print(tabela_resultado)


    cor_do_texto = "red"  # Substitua "blue" pela cor desejada
    #dcp = 486.00
    #dcfp = 540.00
    dcp = st.session_state.number1
    dcfp = st.session_state.number2


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
    pcp1 = (C_P_V[st.session_state.indice] * dados[' Consumo Ponta'])
    pc1 = (C_FP_V[st.session_state.indice]*dados[' Consumo Fora Ponta'])
    pd = D_FP_V[st.session_state.indice] * dcfp
    dcfp_max = dcfp*1.05
    dcfp_novo = []

    #tem que ser a maior demanda ponta ou fora ponta
    demanda_medida1 = dados[' Demanda Medida Ponta']
    demanda_medida2 = dados[' Demanda Medida fora Ponta']
    demanda = []
    pu = 0
    for i in range(12):
        aux = 0.0
        if demanda_medida1[i] > demanda_medida2[i]:
            demanda = demanda_medida1
        else:
            demanda = demanda_medida2

        if demanda[i] > dcfp_max:
            aux = demanda[i]-dcfp_max
        valor_unico = U_V[st.session_state.indice]*(aux)
        pu = pu + valor_unico
    valor_verde = pd+pc1+pcp1+pu
    valor_verde_anual = valor_verde.sum()

    #st.write(valor_verde)
    #st.write(valor_verde_anual)


    # Demanda Média
    demanda_ponta = 0
    acum1 = 0
    acum2 = 0
    for i in range(12):

        demanda_ponta = demanda_medida1[i] + acum1
        demanda_foraponta = demanda_medida2[i] + acum2
        acum1 = demanda_ponta
        acum2 = demanda_foraponta

    media_demanda_ponta = demanda_ponta / 12
    media_demanda_foraponta = demanda_foraponta / 12
    demanda_sugerida = (media_demanda_ponta+media_demanda_foraponta)/2
    #st.write(demanda_sugerida)
    f_dcp = locale.currency(dcp, grouping=True, symbol=None)
    f_dcfp = locale.currency(dcfp, grouping=True, symbol=None)
    st.markdown("<h1 style='text-align: center;'>Relatório Completo</h1>", unsafe_allow_html = True)
    st.write('Sua demanda atual é')
    if st.session_state.opt == 'Horo-Sazional Azul':
        st.write(f'Demanda Ponta: <span style="color:{cor_do_texto}">{f_dcp} kW</span>',unsafe_allow_html=True)
        st.write(f'Demanda Fora Ponta: <span style="color:{cor_do_texto}">{f_dcfp} kW</span>', unsafe_allow_html=True)
    else:
        st.write(f'Demanda Ponta: <span style="color:{cor_do_texto}">{f_dcp} kW</span>', unsafe_allow_html=True)

    #modelo_atual = 'Horo - Sazional Azul'
    modelo_atual = st.session_state.opt
    modelo_atual1 = st.session_state.sub1
    st.write(f'O seu modelo de tarifação atual é o <span style="color:{cor_do_texto}">{modelo_atual}</span>',unsafe_allow_html=True)
    st.write(f'O seu Subgrupo A4 é o <span style="color:{cor_do_texto}">{modelo_atual1}</span>',unsafe_allow_html=True)
    st.write('Abaixo o gráfico faz um comparativo dos gastos, mês a mês, com cada um dos modelos de tarifação:')

    #tarifa azul
    pcp2 = (C_P_A[st.session_state.indice] * dados[' Consumo Ponta'])
    pc2 = (C_FP_A[st.session_state.indice] * dados[' Consumo Fora Ponta'])
    pd = (D_P_A[st.session_state.indice] * dcp)
    pdp = (D_FP_A[st.session_state.indice] * dcfp)
    valor_azul = pcp2 + pc2 + pd + pdp
    valor_zul_anual = valor_azul.sum()
    #st.write(valor_azul)

    #Plotagem do gráfico 1
    grupos = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    cont = np.arange(len(grupos))
    largura = 0.35
    fig, ax = plt.subplots()
    ax.bar(cont - largura/2, valor_verde, largura, label='Verde', color='green')
    ax.bar(cont + largura/2, valor_azul, largura, label='Azul',color='blue')
    ax.set_ylabel('Valor')
    ax.set_title('Valor por mês Demanda Contratada')
    ax.set_xticks(cont,grupos)
    #bar_label_h = ax.bar(cont - largura/2, valor_verde, largura, label='Verde', color='green')
    #bar_label_m = ax.bar(cont + largura/2, valor_azul, largura, label='Azul',color='blue')
    #ax.bar_label(bar_label_h)
    #ax.bar_label(bar_label_m)
    ax.legend()
    plt.show()
    st.pyplot(plt)


    f_valor_verde_anual = locale.currency(valor_verde_anual, grouping=True, symbol=True)
    f_valor_azul_anual = locale.currency(valor_zul_anual, grouping=True, symbol=True)

    #aaa = "{:-.2f}".format(valor_verde_anual)
    #st.write(aaa)
    #st.write(bbb)
    st.write('Os valores gastos anualmente com cada modalidade seriam de:')
    st.write(f'Horo-Sazional Verde:<span style="color:{cor_do_texto}">{f_valor_verde_anual}</span>',unsafe_allow_html=True)
    st.write(f'Horo-Sazional Azul:<span style="color:{cor_do_texto}">{f_valor_azul_anual}</span>',unsafe_allow_html=True)
    diferenca = valor_zul_anual - valor_verde_anual
    f_diferenca = locale.currency(diferenca, grouping=True, symbol=True)
    if valor_verde_anual > valor_zul_anual:
        melhor = "Horo-Sazional Azul"
    else:
        melhor = "Horo-Sazional Verde"
    f_demanda_sugerida = locale.currency(demanda_sugerida, grouping=True, symbol=None)
    st.write(f'Tendo em vista uma diferença de gastos anual de <span style="color:{cor_do_texto}">{f_diferenca}</span> entre as duas modalidades, a sugestão é que seja optado pela modalidade tarifaria:<span style="color:{cor_do_texto}">{melhor}</span>',unsafe_allow_html=True)
    # st.write(f"Column name is **{columnName}**")
    st.write('Ainda neste sentido, com o modelo tárifario redefinido, aconcelha-se também a mudança do valor da demanda contratada')
    st.write(f'Nossa sugestão de demanda é <span style="color:{cor_do_texto}">{f_demanda_sugerida} kW</span>',unsafe_allow_html=True)

    pd2 = D_FP_V[st.session_state.indice] * demanda_sugerida
    valor_verde2 = pd2 + pc1 + pcp1 + pu
    valor_verde_anual2 = valor_verde2.sum()
    diferenca2 = valor_zul_anual - valor_verde_anual2

    # Plotagem do gráfico 2
    grupos = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    cont = np.arange(len(grupos))
    largura = 0.35
    fig, ax = plt.subplots()
    ax.bar(cont - largura / 2, valor_verde2, largura, label='Verde', color='green')
    #ax.bar(cont + largura / 2, valor_azul, largura, label='Azul', color='blue')
    ax.set_ylabel('Valor')
    ax.set_title('Valor por mês Demanda Sugerida')
    ax.set_xticks(cont, grupos)
    ax.legend()
    plt.show()
    st.pyplot(plt)
    f_diferenca2 = locale.currency(diferenca2, grouping=True, symbol=True)
    f_valor_verde_anual2 = locale.currency(valor_verde_anual2, grouping=True, symbol=True)
    st.write(f'O valor gasto anualmente na modalidade escolhida com a demanda sugerida é de <span style="color:{cor_do_texto}">{f_valor_verde_anual2}</span> ', unsafe_allow_html=True)
    st.write(f'que é uma diferença de <span style="color:{cor_do_texto}">{f_diferenca2}</span> em relação ao seu gasto anual atual', unsafe_allow_html=True)

    #tabela_resultado['ANO'] = tabela_resultado['ANO'].astype(int)
    st.write('Calculo para dimensionar o banco de capacitores')
    st.write('Abaixo encontra-se os valores medidos atualmente:')
    st.write(tabela_resultado)
    st.write('Abaixo encontra-se os valores corrigidos caso o fator de potência esteja abaixo de ***0,92*** ')
    st.write(tabela_resultado_corrigido)

    #plt.set_title('FATOR DE POTÊNCIA ATUAL X MES-ANO')
    #plt.plot(grupos, tabela_resultado_corrigido['FP_CORRIGIDO'])
    #plt.show()
    #st.pyplot(plt)
    #Plotagem grafico 3
    fig, ax = plt.subplots()
    ax.bar(cont - largura / 2, tabela_resultado_corrigido['FP_CORRIGIDO'], largura, label='Verde', color='green')
    # ax.bar(cont + largura / 2, valor_azul, largura, label='Azul', color='blue')
    ax.set_ylabel('Valor')
    ax.set_title('caralho')
    ax.set_xticks(cont,grupos)
    ax.legend()
    plt.show()
    st.pyplot(plt)
    st.line_chart(tabela_resultado_corrigido['FP_CORRIGIDO'])

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