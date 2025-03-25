from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Manutencao(Base):
    __tablename__ = 'manutencao'

    id = Column("pk_id",Integer, primary_key=True, autoincrement=True)
    nome_equipamento = Column(String(140), ForeignKey("equipamentos.pk_nome")) #ForeignKey nome da tabela equipamentos
    matricula_tecnico = Column(String(140), ForeignKey("tecnicos.pk_matricula")) #ForeignKey nome da tabela equipamentos
    status = Column(String(140))
    tipo_manutencao= Column(String(140))
    comentario = Column(String(140),default="")
    previsao_conclusao = Column(DateTime)

    equipamentos = relationship("Equipamento", back_populates="manutencao")
    tecnicos = relationship("Tecnico", back_populates="manutencao")

    def __init__(self, nome_equipamento:str, matricula_tecnico:str, status:str, tipo_manutencao:str, comentario:str, previsao_conclusao:datetime):

        self.nome_equipamento = nome_equipamento
        self.matricula_tecnico = matricula_tecnico
        self.status = status #Informar se equipamento está em Manutenção, Fila de espera, Pronto ou Aguardando peças
        self.tipo_manutencao = tipo_manutencao
        self.comentario = comentario #Permitir informar se equipamento está aguardando alguma peça para finalizar
        self.previsao_conclusao = previsao_conclusao #DateTime para permitir posteriormente filtrar por data/horario

