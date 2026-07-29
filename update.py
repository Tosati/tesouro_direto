import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = "https://www.tesourodireto.com.br/titulos/"

html = requests.get(URL).text
soup = BeautifulSoup(html, "html.parser")

linhas = []

titulos_desejados = [
    "Tesouro Selic 2027",
    "Tesouro Selic 2029",
    "Tesouro Selic 2031",
    "Tesouro IPCA+ 2029",
    "Tesouro IPCA+ 2032",
    "Tesouro IPCA+ 2035",
    "Tesouro IPCA+ 2040",
    "Tesouro IPCA+ 2045",
    "Tesouro IPCA+ 2055"
]

tabela = soup.find("table")

for row in tabela.find_all("tr")[1:]:
    cols = [c.get_text(strip=True) for c in row.find_all("td")]
    nome = cols[0]

    if nome in titulos_desejados:
        linhas.append({
            "nome": nome,
            "data_cotacao": datetime.now().strftime("%Y-%m-%d"),
            "pu_compra": cols[1],
            "pu_venda": cols[2],
            "taxa_compra": cols[3],
            "taxa_venda": cols[4],
            "vencimento": cols[5]
        })

df = pd.DataFrame(linhas)
df.to_csv("tesouro_direto.csv", index=False)
