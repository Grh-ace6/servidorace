from pydantic import BaseModel

#formBuscaAtividade:suggestionNomeServ_selection
#'javax.faces.ViewState': 'j_id1',

class ExtensaoInfo(BaseModel):
    formBuscaAtividade: str
    formBuscaAtividade_selectBuscaTitulo: str
    formBuscaAtividade_buscaTitulo: str
    formBuscaAtividade_buscaTipoAcao: str
    formBuscaAtividade_buscaUnidade: str
    formBuscaAtividade_nomeServidor: str
    formBuscaAtividade_suggestionNomeServSelection: str
    formBuscaAtividade_buscaAno: str
    formBuscaAtividade_btBuscar: str
    javax_faces_ViewState: str