import requests as req
from bs4 import BeautifulSoup

# Lógica para web scrapping da pagina de detalhes  
def generate_extensaoDetalhes(id):
    
    response_detalhes = req.get(f'http://sigaa.sig.ufal.br/sigaa/link/public/extensao/visualizacaoAcaoExtensao/{id}')
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
                    value = td.get_text(strip=True).replace("\n", "").replace("\t", "").strip()
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
    membros_table = soup.find_all('table', id='tbEquipe')
    membros_list = []

    for membros in membros_table:
        # Extrair a URL da imagem
        imagem_tag = membros.find('td', class_='foto').find('img')
        imagem_url = imagem_tag['src'] if imagem_tag else None
        
        # Extrair o nome
        nome_tag = membros.find('span', class_='nome')
        nome = nome_tag.get_text(strip=True).split('Categoria')[0].strip() if nome_tag else None
        
        # Extrair a categoria e função
        descricao = membros.find('td', class_='descricao').get_text(separator="|", strip=True).split("|")
        categoria = descricao[1].split(' ')[1]
        if len(descricao) > 3:
            funcao = descricao[3].split(' ')[0] 
        else:
            funcao = descricao[2].split(':')[1]

        # Armazenar as informações em um dicionário
        membros_dict = {
            'nome': nome,
            'categoria': categoria,
            'funcao': funcao,
            'imagem_url': imagem_url
        }
        membros_list.append(membros_dict)

    extensao_detalhes = {
        "data": data,
        "resumo": resumo,
        "publico_alvo": publico_alvo,
        "membros": membros_list,   
    }
    
    return extensao_detalhes
