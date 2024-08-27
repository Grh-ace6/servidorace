from pydantic import BaseModel


class PortariaInfo(BaseModel):
    pageNum: str
    pagina: str
    publico: str
    acao: str
    inicio: str
    solicitacao_numero: str
    solicitacao_ano: str
    solicitacao_boletim_numero: str
    solicitacao_boletim_ano: str
    solicitacao_tipo_id: str
    solicitacao_assunto: str
    solicitacao_informativo: str
    data: str