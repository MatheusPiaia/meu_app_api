from pydantic import BaseModel
from typing import List
from model.equipamento import Equipamento


class EquipamentoSchema(BaseModel):
    """Define como um novo equipamento ao ser cadastrado
        deve ser representado
    """
    nome: str
    modelo: str
    setor: str
    impacto: str

class EquipamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do equipamento.
    """
    nome: str

class ListagemEquipamentoSchema(BaseModel):
    """ Define como a lista de equipamentos cadastrados deverá será retornada.
    """
    equipamentos:List[EquipamentoSchema]

def apresenta_equipamentos(equipamentos: List[Equipamento]):
    """ Retorna uma representação do equipamento seguindo o schema definido em
        EquipamentoSchema.
    """
    result = []
    for equipamento in equipamentos:
        result.append({
            "nome": equipamento.nome,
            "modelo": equipamento.modelo,
            "setor": equipamento.setor,
            "impacto": equipamento.impacto,            
        })
    return {"equipamentos": result}

class EquipamentoViewSchema(BaseModel):
    """Define como um  equipamento será retornado
    """
    nome: str
    modelo: str
    setor: str
    impacto: str

class EquipamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str
    

def apresenta_equipamento(equipamento: Equipamento):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "nome": equipamento.nome,
        "modelo": equipamento.modelo,
        "setor": equipamento.setor,
        "impacto": equipamento.impacto
    }
