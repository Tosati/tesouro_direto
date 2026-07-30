import requests
import json
import time
import os

# ============================
# CONFIGURAÇÃO DA API SGS
# ============================

SERIE_SELIC = 11       # Selic diária
SERIE_IPCA = 433       # IPCA diária

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

# ============================
# FUNÇÃO PARA BAIXAR SÉRIE SGS
# ============================

def obter_serie(codigo):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json"

    for tentativa in range(5):
        try:
            r = requests.get(url, timeout=10)
            data = r.json()

            if isinstance(data, list) and len(data) > 0:
                return data

        except:
            time.sleep(2)

    return []

# ============================
# CÁLCULO DE PU DIÁRIO
# ============================

def calcular_pu_selic(serie_selic):
    pu = 1000.0
    dias = min(15, len(serie_selic))

    for dia in serie_selic[-dias:]:
        taxa = float(dia["valor"]) / 100
        pu *= (1 + taxa)

    return pu

def calcular_pu_ipca(serie_ipca, serie_real):
    pu = 1000.0
    dias = min(len(serie_ipca), len(serie_real), 15)

    for i in range(-dias, 0):
        ipca = float(serie_ipca[i]["valor"]) / 100
        real = float(serie_real[i]["valor"]) / 100
        pu *= (1 + ipca) * (1 + real)

    return pu

# ============================
# PROCESSAMENTO DOS TÍTULOS
# ============================

resultado = {}

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
            "ultimos_15_dias": []
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
        "pu_diario": round(pu, 4),
        "ultimos_15_dias": serie_titulo[-15:]
    }

# ============================
# CRIAÇÃO DA ESTRUTURA /api
# ============================

os.makedirs("api/titulo", exist_ok=True)

# JSON principal
with open("api/titulos.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)

# JSON minificado
with open("api/titulos.min.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, separators=(",", ":"))

# JSON por título
for nome, dados in resultado.items():
    codigo = dados["codigo_sgs"]
    caminho = f"api/titulo/{codigo}.json"

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
