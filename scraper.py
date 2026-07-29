import requests
import json
import time

# Códigos SGS do Banco Central (taxas diárias)
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

    for tentativa in range(5):
        try:
            r = requests.get(url, timeout=10)

            try:
                data = r.json()
            except:
                time.sleep(2)
                continue

            if not isinstance(data, list):
                time.sleep(2)
                continue

            if len(data) == 0:
                time.sleep(2)
                continue

            return data

        except:
            time.sleep(2)

    return []

resultado = {}

for nome, codigo in TITULOS.items():
    serie = obter_serie(codigo)

    if len(serie) == 0:
        resultado[nome] = {
            "codigo_sgs": codigo,
            "erro": "Falha ao obter dados do Banco Central",
            "ultimos_15_dias": []
        }
        continue

    # Último valor
    ultimo = serie[-1]
    data_ultimo = ultimo["data"]
    valor_ultimo = float(ultimo["valor"])

    # Valor anterior
    if len(serie) > 1:
        anterior = serie[-2]
        valor_anterior = float(anterior["valor"])
        variacao = valor_ultimo - valor_anterior
    else:
        valor_anterior = None
        variacao = None

    resultado[nome] = {
        "codigo_sgs": codigo,
        "data": data_ultimo,
        "valor": valor_ultimo,
        "valor_anterior": valor_anterior,
        "variacao": variacao,
        "ultimos_15_dias": serie[-15:]  # agora sim: últimos 15 dias reais
    }

with open("titulos.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)
