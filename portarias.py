import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

from models.portariainfo import PortariaInfo


def generate_portarias(portariaInfo:PortariaInfo):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    data = {
        "pageNum": portariaInfo.pageNum,
        "pagina": portariaInfo.pagina,
        "publico": portariaInfo.publico,
        "acao": portariaInfo.acao,
        "inicio": portariaInfo.inicio,
        "solicitacao.numero": portariaInfo.solicitacao_numero,
        "solicitacao.ano": portariaInfo.solicitacao_ano,
        "solicitacao.boletim.numero": portariaInfo.solicitacao_boletim_numero,
        "solicitacao.boletim.ano": portariaInfo.solicitacao_boletim_ano,
        "solicitacao.tipo.id": portariaInfo.solicitacao_tipo_id,
        "solicitacao.assunto": portariaInfo.solicitacao_assunto,
        "solicitacao.informativo": portariaInfo.solicitacao_informativo,
        "data": portariaInfo.data
    }

    ROOT_URL = "https://sipac.sig.ufal.br"
    POST_PESQUISA_URL = urljoin(ROOT_URL, "/public/consultarInformativos.do")

    html = req.post(POST_PESQUISA_URL, headers=headers, data=data).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("tbody.listagem")
    valor_maximo = soup.select_one("input#pageMax").get('value')

    portarias = []

    

    for row in table.select("tr"):
        td = row.select("td")
        assert len(td) == 5
        cadastro, tipo, assunto, boletim, detalhar = td

        cadastro = cadastro.text.strip()
        tipo = tipo.text.strip()
        assunto = assunto.text.strip()

        boletim_url = urljoin(ROOT_URL, boletim.select_one("a").get("href"))
        boletim_nome = boletim.text.strip()

        detalhes = dict()
        for data in detalhar.select('input[type="hidden"]'):
            name, value = data.get("name"), data.get("value")
            detalhes[name] = value

        detalhes_id =  detalhes.get('solicitacao.id')
        detalhes_url = "https://sipac.sig.ufal.br/sipac/VerInformativo?id=" + detalhes_id

        portaria = {
            "cadastro": cadastro,
            "tipo": tipo,
            "assunto": assunto,
            "boletim": {
                "url": boletim_url,
                "nome": boletim_nome,
            },
            "valor_maximo": valor_maximo,
            "detalhes": detalhes,
            "url_detalhes": detalhes_url,
        }
        portarias.append(portaria)
        
    return portarias

