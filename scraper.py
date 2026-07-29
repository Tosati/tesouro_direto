import requests
import json

# Códigos SGS do Banco Central para títulos do Tesouro Direto
TITULOS = {
    "Tesouro Selic 2027": 4390,
    "Tesouro Selic 2029": 4391,
    "Tesouro IPCA+ 2035": 4393,
    "Tesouro IPCA+ 2045": 4394
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
