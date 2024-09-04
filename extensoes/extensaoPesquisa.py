import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def generate_extensao():
    ROOT_URL = "https://sigaa.sig.ufal.br"
    URL = urljoin(ROOT_URL, "/sigaa/public/extensao/consulta_extensao.jsf")

    html = req.get(URL).text
    soup = BeautifulSoup(html, "html.parser")
    form = soup.select_one("#formBuscaAtividade")
    action = urljoin(ROOT_URL, form.get("action"))
    enc_type = form.get("enctype")

    response = req.post(
        action,
        data= "formBuscaAtividade=formBuscaAtividade&formBuscaAtividade%3AselectBuscaTitulo=on&formBuscaAtividade%3AbuscaTitulo=Computa%E7%E3o&formBuscaAtividade%3AbuscaTipoAcao=0&formBuscaAtividade%3AbuscaUnidade=0&formBuscaAtividade%3AnomeServidor=&formBuscaAtividade%3AsuggestionNomeServ_selection=&formBuscaAtividade%3AbuscaAno=2024&formBuscaAtividade%3AbtBuscar=Buscar&javax.faces.ViewState=j_id1",
        headers={
            "Content-Type": enc_type,
        },
    )

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    form_result = soup.select_one("#form")
    table_result = form_result.select_one("table.listagem")

    extensoes = []

    for row in table_result.select_one('tbody'):
        if row.name == 'tr':
            cells = row.find_all('td')
            
            # Acessa e armazena os textos em variáveis
            titulo = cells[0].find('a').get_text(strip=True)  
            tipo_projeto = cells[1].get_text(strip=True)      
            localizacao = cells[2].get_text(strip=True)

            # Acessa a tag a e pega o id da url dos detalhes
            onclick = cells[0].find('a').get('onclick')
            id_detalhes = re.search(r"idAtividadeExtensaoSelecionada':'(\d+)'", onclick)
            id_refatorado = id_detalhes.group(1)

            extensao = {
                "titulo": titulo,
                "tipo_projeto": tipo_projeto,
                "UP": localizacao,
                "id": id_refatorado
            }
            extensoes.append(extensao)

    return extensoes