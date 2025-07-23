# %%
import requests
import pandas as pd
import datetime

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
        'Nome': produto['TrsrBd']['nm'],
        'Vencimento': produto['TrsrBd']['mtrtyDt'],
        'Valor Minimo Titulo': produto['TrsrBd']['minInvstmtAmt'],
        'Valor Unitário Titulo': produto['TrsrBd']['untrInvstmtVal'],
        'Juros Semestrais': produto['TrsrBd']['semiAnulIntrstInd'],
        'Taxa de Investimento': produto['TrsrBd']['anulInvstmtRate'],
        'Taxa de Resgate': produto['TrsrBd']['anulRedRate']


    })

# Criando um DataFrame
df = pd.DataFrame(titulos)

# Definindo Vencimento como coluna de data
df['Vencimento'] = pd.to_datetime(df['Vencimento'])

# %%

# Exibindo as primeiras linhas
print(df.head())


# %%
print("teste")