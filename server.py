from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.portariainfo import PortariaInfo
from portarias import generate_portarias
from extensoes.extensaoPesquisa import generate_extensao
from extensoes.extensaoDetalhes import generate_extensaoDetalhes


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/portarias")
def read_portarias(portariaInfo:PortariaInfo):
    return generate_portarias(portariaInfo)

@app.get("/extensao")
def read_extensao():
   return generate_extensao()

@app.get("/extensao/{id}")
def read_extensao_id(id: int):
    return generate_extensaoDetalhes(id=id)