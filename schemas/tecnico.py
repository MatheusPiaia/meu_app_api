from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from model.tecnico import Tecnico

class TecnicoSchema(BaseModel):
    """Define como um novo tecnico ao ser cadastrado
        deve ser representado
    """
    model_config = ConfigDict(coerce_numbers_to_str=True)
    nome: str
    matricula: str
    turno: str

class TecnicoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no nome e matricula do tecnico.
    """
    model_config = ConfigDict(coerce_numbers_to_str=True)
    nome: Optional[str] = None
    matricula: Optional[str] = None

class ListagemTecnicoSchema(BaseModel):
    """ Define como a lista de tecnicos cadastrados deverá será retornada.
    """
    tecnicos:List[TecnicoSchema]

def apresenta_tecnicos(tecnicos: List[Tecnico]):
    """ Retorna uma representação do cadastro do tecnico seguindo o schema definido em
        TecnicoSchema.
    """
    result = []
    for tecnico in tecnicos:
        result.append({
            "nome": tecnico.nome,
            "matricula": tecnico.matricula,
            "turno": tecnico.turno,                       
        })
    return {"tecnicos": result}

class TecnicoViewSchema(BaseModel):
    """Define como deve ser a estrutura do dado para ser retornado 
        para o Schema de manutencao"""
    nome:str
    matricula:str

class TecnicoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str
    matricula: str

def apresenta_tecnico(tecnico: Tecnico):
    """ Retorna uma representação dos dados do tecnico seguindo o schema definido em
        TecnicoSchema.
    """
    return {
        "nome": tecnico.nome,
        "matricula": tecnico.matricula,
        "turno": tecnico.turno,
    }