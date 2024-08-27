from fastapi import FastAPI
from models.portariainfo import PortariaInfo
from portarias import generate_portarias
from models.extensaoinfo import ExtensaoInfo


app = FastAPI()


@app.get("/portarias")
def read_portarias(portariaInfo:PortariaInfo):
    return generate_portarias(portariaInfo)

@app.get("/extensao")
def read_extensao(extensaoInfo:ExtensaoInfo):
    return 