import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import re
from requests import Session


from models.extensaoinfo import ExtensaoInfo


def generate_extensao(extensaoInfo:ExtensaoInfo):
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
        data= {
            'formBuscaAtividade': extensaoInfo.formBuscaAtividade,
            'formBuscaAtividade:selectBuscaTitulo': extensaoInfo.formBuscaAtividade_selectBuscaTitulo,
            'formBuscaAtividade:buscaTitulo': extensaoInfo.formBuscaAtividade_buscaTitulo,
            'formBuscaAtividade:buscaTipoAcao': extensaoInfo.formBuscaAtividade_buscaTipoAcao,
            'formBuscaAtividade:buscaUnidade': extensaoInfo.formBuscaAtividade_buscaUnidade,
            'formBuscaAtividade:nomeServidor': extensaoInfo.formBuscaAtividade_nomeServidor,
            'formBuscaAtividade:suggestionNomeServ_selection': extensaoInfo.formBuscaAtividade_suggestionNomeServSelection,
            'formBuscaAtividade:buscaAno': extensaoInfo.formBuscaAtividade_buscaAno, 
            'formBuscaAtividade:btBuscar': extensaoInfo.formBuscaAtividade_btBuscar,
            'javax.faces.ViewState': extensaoInfo.javax_faces_ViewState,
        },
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

            # Acessa a tag a e pega o id da url dos detalhes
            onclick = cells[0].find('a').get('onclick')
            id_detalhes = re.search(r"idAtividadeExtensaoSelecionada':'(\d+)'", onclick)

        

            # Lógica para web scrapping da pagina de detalhes  
            response_detalhes = session.get(f'http://sigaa.sig.ufal.br/sigaa/link/public/extensao/visualizacaoAcaoExtensao/{id_detalhes.group(1)}')
            html_detalhes = response_detalhes.text
            soup = BeautifulSoup(html_detalhes, "html.parser")
            table = soup.select_one("table.visualizacao")

            #dados da primeira seção pagina de detalhes
            data = {}

            if table:  
                for row in table.find_all('tr'):  
                    th_elements = row.find_all('th')
                    td_elements = row.find_all('td')
                    
                    if th_elements and td_elements:  # Verifica se ambos os <th> e <td> existem
                        for th, td in zip(th_elements, td_elements):
                            key = th.get_text(strip=True)
                            value = td.get_text(strip=True)
                            data[key] = value
            
            #dados do resumo e público alvo
            resumo_h4 = soup.find('h4', string=" Resumo ")
            resumo = ""
            if resumo_h4:
                resumo_p = resumo_h4.find_next('p')
                resumo = resumo_p.get_text(strip=True)

            publico_alvo_h4 = soup.find('h4', string="Público Alvo ")
            publico_alvo = ""
            if publico_alvo_h4:
                publico_alvo = publico_alvo_h4.find_next('p')
                publico_alvo = publico_alvo.get_text(strip=True)

            #dados dos nomes, fotos e status dos membros
            membros = soup.find_all('div', class_='foto')

            extensao = {
                "titulo": titulo,
                "tipo_projeto": tipo_projeto,
                "UP": localizacao,
                "detalhes":
                    {
                        "data": data,
                        "resumo": resumo,
                        "publico_alvo": publico_alvo,
                        "membros": membros
                    },
            }

            print(extensao)