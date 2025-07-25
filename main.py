import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

@st.cache_data(ttl="1day")

def coleta_tesouro():
    # URL com os dados dos títulos
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json"

    # Fazendo a requisição
    response = requests.get(url)
    data = response.json()

    # Lista onde para armazenar os dados dos títulos
    titulos = []

    # Iterar pelos produtos
    for produto in data['response']["TrsrBdTradgList"]:
        titulos.append({
            'Título': produto['TrsrBd']['nm'],
            'Vencimento': produto['TrsrBd']['mtrtyDt'],
            'Valor Minimo Titulo': produto['TrsrBd']['minInvstmtAmt'],
            'Valor Unitário Titulo': produto['TrsrBd']['untrInvstmtVal'],
            'Juros Semestrais': produto['TrsrBd']['semiAnulIntrstInd'],
            'Taxa de Investimento': produto['TrsrBd']['anulInvstmtRate'],
            'Taxa de Resgate': produto['TrsrBd']['anulRedRate']


        })

    # ultima_att = [x['opngDtTm'] for x in data['response']["TrsrBondMkt"]]
    
    # Criando um DataFrame
    df = pd.DataFrame(titulos)

    # Definindo Vencimento como coluna de data
    df['Vencimento'] = pd.to_datetime(df['Vencimento']).dt.date
    today = datetime.today().date()
    df['anos'] = (df['Vencimento']- today).apply(lambda x: int(x.days/365))
    df['dias_ate_vencimento'] = (df['Vencimento']- today)
   
    return df

def opcao_titulo(df: pd.DataFrame, tempo: int):
    df = df

    if tempo < 3:
        df_filtrado = df[df['anos'] < 3]

    elif tempo > 2 and tempo < 6:
        df_filtrado = df[(df['anos'] > 2) & (df['anos'] < 6)]
    
    else:
        df_filtrado = df[df['anos'] > 5]
        
    
    return df_filtrado


st.set_page_config(page_title="Planejador", page_icon="💰")

st.markdown(
    """
# Qual o melhor título do tesouro pra você?

Aqui você pode escolher qual título se encaixa pra você nesse momento.

"""
)
# Organizando em colunas

with st.container(border=True):
    objetivo_opt = ['Curto (até 2 anos)', 'Médio (3 - 5 anos)', 'Longo (5+ anos)']
    objetivo = st.selectbox("Qual seu objetivo?", objetivo_opt)

col1, col2= st.columns(2)

valor_investir = col1.number_input("Valor para investir?", min_value=0., format='%.2f')
tempo = col2.number_input("Tempo do investimento?", min_value=0)    


# Botão para pesquisa e início do programa
if st.button("Pesquisar"):
    df = coleta_tesouro()

    #st.write(df)

    if (objetivo == 'Curto (até 2 anos)'):
        st.write(opcao_titulo(df, 2))
        st.success("Pesquisa realizada com sucesso!")
        
    elif (objetivo == 'Médio (3 - 5 anos)'):
        st.write(opcao_titulo(df, 5))
        st.success("Pesquisa realizada com sucesso!")

    elif (objetivo == 'Longo (5+ anos)'):
        st.write(opcao_titulo(df, 6))
        st.success(f"Pesquisa realizada com sucesso!")

    st.button("Reset", type='primary')


