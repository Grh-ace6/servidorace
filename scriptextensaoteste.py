import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from requests import Session

# Inicia a sessão
session = Session()

# Definindo as URLs
ROOT_URL = "https://sigaa.sig.ufal.br"
POST_PESQUISA_URL = urljoin(ROOT_URL, "/sigaa/public/extensao/consulta_extensao.jsf")


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/jxl,image/webp,image/png,image/svg+xml,/;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=6C1B12E43E37220A3DAEC3C6AFF563B3.srv1inst1', 
    'Origin': 'https://sigaa.sig.ufal.br',
    'Priority': 'u=0, i',
    'Referer': 'https://sigaa.sig.ufal.br/sigaa/public/extensao/consulta_extensao.jsf',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0'
}
data = {
    "formBuscaAtividade": "formBuscaAtividade",
    "formBuscaAtividade:selectBuscaTitulo": "on",
    "formBuscaAtividade:buscaTitulo": "computa",
    "formBuscaAtividade:selectBuscaTipoAtividade": "on",
    "formBuscaAtividade:buscaTipoAcao": "2",
    "formBuscaAtividade:buscaUnidade": "0",
    "": "formBuscaAtividade:nomeServidor",
    "": "formBuscaAtividade:suggestionNomeServ_selection",
    "formBuscaAtividade:buscaAno": "2024",
    "formBuscaAtividade:btBuscar": "Buscar",
    "javax.faces.ViewState": "j_id3"
}



# Fazer uma requisição GET inicial para capturar cookies e iniciar a sessão
response = session.post(POST_PESQUISA_URL, headers=headers, data=data)

# Exibir os cookies que foram enviados
print("Cookies enviados na requisição:", headers.get('Cookie'))
# Processar o HTML da resposta
html = response.text
print(html)








































"""
html = session.get(POST_PESQUISA_URL, headers=headers, data=data).text
print(html)

# Supondo que html já tenha sido obtido a partir do request
""""""soup = BeautifulSoup(html, "html.parser")
table = soup.select_one("table.listagem")
extensoes = []


for row in table.select("tr"):
    # Seleciona todas as <td> na linha
    td = row.select("td")
    
    # Extrai o primeiro <td>, que contém o link e o script
    primeiro_td = td[0]
    
    # Extrai o texto do link (título e ano)
    ano_titulo = primeiro_td.select_one("a").text.strip()
    
    # Extrai os outros valores (tipo e departamento)
    tipo = td[1].text.strip()
    departamento = td[2].text.strip()
    
    # Cria um dicionário com as informações extraídas
    extensao = {
        "ano_titulo": ano_titulo,
        "tipo": tipo,
        "departamento": departamento,
    }
    
    # Adiciona ao resultado final
    print(extensao)

"""