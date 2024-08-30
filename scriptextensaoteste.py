from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# session é necessário porque o cookie só existe no html na primeira requisição.
# Uma vez setado, os próximos pedidos a URL não o apresentam
ROOT_URL = "https://sigaa.sig.ufal.br"
URL = urljoin(ROOT_URL, "/sigaa/public/extensao/consulta_extensao.jsf")
session = Session()

html = session.get(URL).text
soup = BeautifulSoup(html, "html.parser")
form = soup.select_one("#formBuscaAtividade")
action = urljoin(ROOT_URL, form.get("action"))
enc_type = form.get("enctype")

response = session.post(
    action,
    data="formBuscaAtividade=formBuscaAtividade&formBuscaAtividade%3AselectBuscaTitulo=on&formBuscaAtividade%3AbuscaTitulo=Computa&formBuscaAtividade%3AselectBuscaTipoAtividade=on&formBuscaAtividade%3AbuscaTipoAcao=2&formBuscaAtividade%3AbuscaUnidade=0&formBuscaAtividade%3AnomeServidor=&formBuscaAtividade%3AsuggestionNomeServ_selection=&formBuscaAtividade%3AbuscaAno=2024&formBuscaAtividade%3AbtBuscar=Buscar&javax.faces.ViewState=j_id1",
    headers={
        "Content-Type": enc_type,
    },
)
html = response.text
soup = BeautifulSoup(html, "html.parser")
form_result = soup.select_one("#form")
table_result = form_result.select_one("table.listagem")


for row in table_result.select_one('tbody'):
    
   if row.name == 'tr':
    
        cells = row.find_all('td')
        
        # Acessa e armazena os textos em variáveis
        titulo = cells[0].find('a').get_text(strip=True)  
        tipo_projeto = cells[1].get_text(strip=True)      
        localizacao = cells[2].get_text(strip=True)       
        
        extensao = {
            "titulo": titulo,
            "tipo_projeto": tipo_projeto,
            "UP": localizacao,
            "detalhes":
                {
                    
                },
        }

        print(extensao)
