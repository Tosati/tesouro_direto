import requests
import pandas as pd

URL = "https://www.tesourodireto.com.br/json/titulos.json"

data = requests.get(URL).json()

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

for titulo in data["response"]["titulos"]:
    nome = titulo["nome"]

    if nome in titulos_desejados:
        linhas.append({
            "nome": nome,
            "data_cotacao": titulo["dataBase"],
            "pu_compra": titulo["precoCompra"],
            "pu_venda": titulo["precoVenda"],
            "taxa_compra": titulo["taxaCompra"],
            "taxa_venda": titulo["taxaVenda"],
            "vencimento": titulo["vencimento"]
        })

df = pd.DataFrame(linhas)
df.to_csv("tesouro_direto.csv", index=False)
