import requests
import json

# Códigos SGS do Banco Central para Tesouro Selic e Tesouro IPCA+
TITULOS = {
    "Tesouro Selic 2027": 4390,
    "Tesouro Selic 2029": 4391,
    "Tesouro Selic 2031": 4392,
    "Tesouro IPCA+ 2029": 4393,
    "Tesouro IPCA+ 2032": 4394,
    "Tesouro IPCA+ 2035": 4395,
    "Tesouro IPCA+ 2040": 4396,
    "Tesouro IPCA+ 2045": 4397,
    "Tesouro IPCA+ 2055": 4398
}

def obter_serie(codigo):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json"
    return requests.get(url).json()

resultado = {}

for nome, codigo in TITULOS.items():
    serie = obter_serie(codigo)
    resultado[nome] = serie[-1]  # último valor (mais recente)

with open("titulos.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)
