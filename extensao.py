import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

from models.extensaoinfo import ExtensaoInfo


def generate_extensao(extensaoInfo:ExtensaoInfo):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'JSESSIONID=15DF67025B9FC8FE33F46B9A5FBA986D.srv1inst1',
        'Origin': 'https://sigaa.sig.ufal.br',
        'Referer': 'https://sigaa.sig.ufal.br/sigaa/public/extensao/consulta_extensao.jsf',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
        'sec-ch-ua': '"Opera GX";v="109", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'formBuscaAtividade': extensaoInfo.formBuscaAtividade,
        'formBuscaAtividade:selectBuscaTitulo': extensaoInfo.formBuscaAtividade_selectBuscaTitulo,
        'formBuscaAtividade:buscaTitulo': extensaoInfo.formBuscaAtividade_buscaTitulo,
        'formBuscaAtividade:buscaTipoAcao': extensaoInfo.formBuscaAtividade_buscaTipoAcao,
        'formBuscaAtividade:buscaUnidade': extensaoInfo.formBuscaAtividade_buscaUnidade,
        'formBuscaAtividade:nomeServidor': extensaoInfo.formBuscaAtividade_nomeServidor,
        'formBuscaAtividade:suggestionNomeServ_selection': extensaoInfo.formBuscaAtividade_suggestionNomeServSelection,
        'formBuscaAtividade:buscaAno': extensaoInfo.formBuscaAtividade_buscaAno, #deve sempre pegar o ano atual
        'formBuscaAtividade:btBuscar': extensaoInfo.formBuscaAtividade_btBuscar,
        'javax.faces.ViewState': extensaoInfo.javax_faces_ViewState,
    }

    ROOT_URL = "https://sigaa.sig.ufal.br/sigaa"
    POST_PESQUISA_URL = urljoin(ROOT_URL, "/public/extensao/consulta_extensao.jsf;")#cookies jsessionid=15DF67025B9FC8FE33F46B9A5FBA986D.srv1inst1

    html = req.post(POST_PESQUISA_URL, headers=headers, data=data).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("tbody")
    extensoes = []

    #tem que refatorar essa parte daqui
    for row in table.select("tr"):
        print("oi")
        # Seleciona todas as <td> na linha
        td = row.select("td")
        
        # O primeiro <td> pode conter um script, então precisamos ignorá-lo
        ano_titulo = td[0].select_one("a").text.strip()  # Extrai o texto do link (título e ano)
        
        tipo = td[1].text.strip()  # Tipo da extensão
        departamento = td[2].text.strip()  # Departamento/localização
        
        # Cria um dicionário com as informações extraídas
        extensao = {
            "ano_titulo": ano_titulo,
            "tipo": tipo,
            "departamento": departamento,
        }
        
        # Adiciona ao resultado final
        extensoes.append(extensao)

        # Retorna ou processa a lista de extensões conforme necessário
        return extensoes    
    
    print(extensoes)