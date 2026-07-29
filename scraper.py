import requests
import json
import time
import math

# Códigos SGS do Banco Central
TITULOS = {
    "Tesouro Selic 2027": {
        "codigo_sgs": 4390,
        "tipo": "selic"
    },
    "Tesouro Selic 2029": {
        "codigo_sgs": 4391,
        "tipo": "selic"
    },
    "Tesouro Selic 2031": {
        "codigo_sgs": 4392,
        "tipo": "selic"
    },
    "Tesouro IPCA+ 2029": {
        "codigo_sgs": 4393,
        "tipo": "ipca"
    },
    "Tesouro IPCA+ 2032": {
        "codigo_sgs": 4394,
        "tipo": "ipca"
    },
    "Tesouro IPCA+ 2035": {
        "codigo_sgs": 4395,
        "tipo": "ipca"
    },
    "Tesouro IPCA+ 2040": {
        "codigo_sgs": 4396,
        "tipo": "ipca"
    },
    "Tesouro IPCA+ 2045": {
        "codigo_sgs": 4397,
        "tipo": "ipca"
    },
    "Tesouro IPCA+ 2055": {
        "codigo_sgs": 4398,
        "tipo": "ipca"
    }
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

            if not data:
                time.sleep(2)
                continue

            return data

        except:
            time.sleep(2)

    return []

def calcular_pu_selic(serie):
    if len(serie) < 2:
        return None

    # Selic diária (%)
    taxa_hoje = float(serie[-1]["valor"]) / 100
    taxa_ontem = float(serie[-2]["valor"]) / 100

    # PU arbitrário inicial (1000)
    pu_ontem = 1000 * (1 + taxa_ontem)
    pu_hoje = pu_ontem * (1 + taxa_hoje)

    return pu_hoje

def calcular_pu_ipca(serie):
    if len(serie) < 2:
        return None

    # IPCA diário (%)
    ipca_hoje = float(serie[-1]["valor"]) / 100
    ipca_ontem = float(serie[-2]["valor"]) / 100

    # PU arbitrário inicial (1000)
    pu_ontem = 1000 * (1 + ipca_ontem)
    pu_hoje = pu_ontem * (1 + ipca_hoje)

    return pu_hoje

resultado = {}

for nome, info in TITULOS.items():
    codigo = info["codigo_sgs"]
    tipo = info["tipo"]

    serie = obter_serie(codigo)

    if len(serie) == 0:
        resultado[nome] = {
            "codigo_sgs": codigo,
            "erro": "Falha ao obter dados do Banco Central",
            "serie_completa": []
        }
        continue

    ultimo = serie[-1]
    data_ultimo = ultimo["data"]
    valor_ultimo = float(ultimo["valor"])

    if len(serie) > 1:
        anterior = serie[-2]
        valor_anterior = float(anterior["valor"])
        variacao = valor_ultimo - valor_anterior
    else:
        valor_anterior = None
        variacao = None

    # Calcular PU
    if tipo == "selic":
        pu = calcular_pu_selic(serie)
    else:
        pu = calcular_pu_ipca(serie)

    resultado[nome] = {
        "codigo_sgs": codigo,
        "data": data_ultimo,
        "valor": valor_ultimo,
        "valor_anterior": valor_anterior,
        "variacao": variacao,
        "pu_calculado": pu,
        "serie_completa": serie
    }

with open("titulos.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)
