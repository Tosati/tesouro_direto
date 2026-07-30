import requests
import json
import os

URL = "https://api.dadosdemercado.com.br/v1/treasury"
TOKEN = "SEU_TOKEN_AQUI"  # coloque seu token aqui

def obter_tesouro_direto():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    r = requests.get(URL, headers=headers, timeout=20)
    data = r.json()

    resultado = {}

    for titulo in data:
        nome = titulo["name"]

        resultado[nome] = {
            "taxa": titulo["rate"],
            "preco": titulo["price"],
            "vencimento": titulo["maturity"],
            "preco_compra": titulo["buy_price"],
            "preco_venda": titulo["sell_price"]
        }

    return resultado


dados = obter_tesouro_direto()

os.makedirs("api/titulo", exist_ok=True)

# JSON principal
with open("api/titulos.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

# JSON minificado
with open("api/titulos.min.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, separators=(",", ":"))

# JSON por título
for nome, info in dados.items():
    codigo = nome.replace(" ", "_").replace("+", "plus")
    caminho = f"api/titulo/{codigo}.json"

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
