import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm"

def obter_tesouro_direto():
    r = requests.get(URL, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    tabela = soup.find("table")
    linhas = tabela.find_all("tr")[1:]  # ignora cabeçalho

    resultado = {}

    for linha in linhas:
        colunas = [c.get_text(strip=True) for c in linha.find_all("td")]

        if len(colunas) < 6:
            continue

        nome = colunas[0]
        taxa = colunas[1]
        preco = colunas[2]
        vencimento = colunas[3]
        preco_compra = colunas[4]
        preco_venda = colunas[5]

        resultado[nome] = {
            "taxa": taxa,
            "preco": preco,
            "vencimento": vencimento,
            "preco_compra": preco_compra,
            "preco_venda": preco_venda
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
