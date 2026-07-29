import requests
import json
import time

# Séries auxiliares do Banco Central
SERIE_SELIC = 11       # Selic diária
SERIE_IPCA = 433       # IPCA diário

# Códigos SGS dos títulos
TITULOS = {
    "Tesouro Selic 2027": {"codigo_sgs": 4390, "tipo": "selic"},
    "Tesouro Selic 2029": {"codigo_sgs": 4391, "tipo": "selic"},
    "Tesouro Selic 2031": {"codigo_sgs": 4392, "tipo": "selic"},
    "Tesouro IPCA+ 2029": {"codigo_sgs": 4393, "tipo": "ipca"},
    "Tesouro IPCA+ 2032": {"codigo_sgs": 4394, "tipo": "ipca"},
    "Tesouro IPCA+ 2035": {"codigo_sgs": 4395, "tipo": "ipca"},
    "Tesouro IPCA+ 2040": {"codigo_sgs": 4396, "tipo": "ipca"},
    "Tesouro IPCA+ 2045": {"codigo_sgs": 4397, "tipo": "ipca"},
    "Tesouro IPCA+ 2055": {"codigo_sgs": 4398, "tipo": "ipca"}
}

def obter_serie(codigo):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json"

    for tentativa in range(5):
        try:
            r = requests.get(url, timeout=10)

            # Tenta converter para JSON
            try:
                data = r.json()
            except:
                time.sleep(2)
                continue

            # Se não for lista, ignora
            if not isinstance(data, list):
                time.sleep(2)
                continue

            # Se vier vazio, tenta de novo
            if len(data) == 0:
                time.sleep(2)
                continue

            return data

        except:
            time.sleep(2)

    return []


def calcular_pu_selic(serie_selic):
    if len(serie_selic) < 2:
        return None

    pu = 1000.0
    dias = min(30, len(serie_selic))

    for dia in serie_selic[-dias:]:
        taxa = float(dia["valor"]) / 100
        pu *= (1 + taxa)

    return pu


def calcular_pu_ipca(serie_ipca, serie_real):
    if len(serie_ipca) < 2 or len(serie_real) < 2:
        return None

    pu = 1000.0
    dias = min(len(serie_ipca), len(serie_real), 30)

    for i in range(-dias, 0):
        ipca = float(serie_ipca[i]["valor"]) / 100
        real = float(serie_real[i]["valor"]) / 100
        pu *= (1 + ipca) * (1 + real)

    return pu


resultado = {}

# Séries auxiliares
serie_selic = obter_serie(SERIE_SELIC)
serie_ipca = obter_serie(SERIE_IPCA)

for nome, info in TITULOS.items():
    codigo = info["codigo_sgs"]
    tipo = info["tipo"]

    serie_titulo = obter_serie(codigo)

    if len(serie_titulo) == 0:
        resultado[nome] = {
            "codigo_sgs": codigo,
            "erro": "Falha ao obter dados do Banco Central",
            "serie_completa": []
        }
        continue

    ultimo = serie_titulo[-1]
    data_ultimo = ultimo["data"]
    valor_ultimo = float(ultimo["valor"])

    if len(serie_titulo) > 1:
        anterior = serie_titulo[-2]
        valor_anterior = float(anterior["valor"])
        variacao = valor_ultimo - valor_anterior
    else:
        valor_anterior = None
        variacao = None

    # Calcular PU real
    if tipo == "selic":
        pu = calcular_pu_selic(serie_selic)
    else:
        pu = calcular_pu_ipca(serie_ipca, serie_titulo)

    resultado[nome] = {
        "codigo_sgs": codigo,
        "data": data_ultimo,
        "valor": valor_ultimo,
        "valor_anterior": valor_anterior,
        "variacao": variacao,
        "pu_calculado": round(pu, 2) if pu else None,
        "serie_completa": serie_titulo
    }

with open("titulos.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)
