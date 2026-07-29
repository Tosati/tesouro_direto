import requests
import pandas as pd

URL = "https://statusinvest.com.br/tesouro direto/api/tesouro"

headers = {
    "User-Agent": "Mozilla/5.0"
}

data = requests.get(URL, headers=headers).json()

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

linhas = []

for titulo in data:
    nome = titulo["name"]

    if nome in titulos_desejados:
        linhas.append({
            "nome": nome,
            "data_cotacao": titulo["updatedAt"],
            "pu_compra": titulo["priceBuy"],
            "pu_venda": titulo["priceSell"],
            "taxa_compra": titulo["rateBuy"],
            "taxa_venda": titulo["rateSell"],
            "vencimento": titulo["maturity"]
        })

df = pd.DataFrame(linhas)
df.to_csv("tesouro_direto.csv", index=False)
