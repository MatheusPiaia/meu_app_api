from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from model.manutencao import Manutencao

class ManutencaoSchema(BaseModel):
    """Define como uma manutencao em equipamento ao ser cadastrada
        deve ser representada
    """
    model_config = ConfigDict(coerce_numbers_to_str=True)
    #id: int
    nome_equipamento: str
    matricula_tecnico: str
    status: str
    tipo_manutencao: str
    comentario: str
    previsao_conclusao: datetime

class ManutencaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no nome e status do equipamento.
    """
    nome_equipamento: Optional[str] = None
    status: Optional[str]= None

class ManutencaoIdSchema(BaseModel):
    '''Define como deve ser a estrutura de visualização feita separando
        cada status
    '''
    id: int

class ManutencaoStatusSchema(BaseModel):
    '''Define como deve ser a estrutura de visualização feita separando
        cada status
    '''
    status: str
    
class ListagemManutencaoSchema(BaseModel):
    """ Define como a lista de equipamentos em manutencao deverá será retornada.
    """
    manutencoes:List[ManutencaoSchema]

def apresenta_manutencoes(manutencoes: List[Manutencao]):
    """ Retorna uma representação do equipamento em manutencao seguindo o schema definido em
        ManutencaoSchema.
    """
    result = []
    for manutencao in manutencoes:        
        formatted_date = manutencao.previsao_conclusao.strftime("%d/%m/%Y %H:%M")
        result.append({
            "id":manutencao.id,
            "nome_equipamento": manutencao.nome_equipamento,
            "matricula_tecnico": manutencao.matricula_tecnico,
            "status": manutencao.status,
            "tipo_manutencao":manutencao.tipo_manutencao,
            "comentario":manutencao.comentario,
            "previsao_conclusao":formatted_date                        
        })
    return {"manutencoes": result}

class ManutencaoViewSchema(BaseModel):
    """Define como uma manutencao em equipamento será retornada
    """
    nome_equipamento: str
    matricula_tecnico: str
    status: str
    tipo_manutencao: str
    comentario: str
    previsao_conclusao: datetime    

class ManutencaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome_equipamento: str

def apresenta_manutencao(manutencao: Manutencao):
    """ Retorna uma representação do equipamento em manutencao seguindo o schema definido em
        ManutencaoSchema.
    """
    return {
        "nome_equipamento": manutencao.nome_equipamento,
        "matricula_tecnico": manutencao.matricula_tecnico,
        "status": manutencao.status,
        "tipo_manutencao": manutencao.tipo_manutencao,
        "comentario":manutencao.comentario,
        "previsao_conclusao":manutencao.previsao_conclusao
    }

class ManutencaoPath(BaseModel):
    id: int    
