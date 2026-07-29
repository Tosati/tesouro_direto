import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.tesourodireto.com.br/titulos"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

# O JSON dos títulos está dentro de um <script> com "window.titulos"
script = soup.find("script", text=lambda t: t and "window.titulos" in t).text

# Extrair JSON
json_text = script.split("window.titulos =")[1].split(";")[0].strip()
data = json.loads(json_text)

# Salvar JSON limpo
with open("titulos.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
