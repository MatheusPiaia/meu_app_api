from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Equipamento(Base):
    __tablename__ = 'equipamentos'

    nome = Column("pk_nome", String, primary_key=True)
    modelo = Column(String(140))
    setor = Column(String(3))
    impacto = Column(Enum("Alto", "Medio", "Baixo", name="impacto_enum"), nullable=False) #qual o impacto desse equipamento na produção Alto,Medio ou baixo
    data_insercao = Column(DateTime, default=datetime.now())

    manutencao = relationship("Manutencao", back_populates="equipamentos")

    #check do impacto para garantir integridade do bd
    __table_args__ = (
        CheckConstraint("impacto IN ('Alto', 'Medio', 'Baixo')", name="check_impacto"),
    )

    def __init__(self, nome:str, modelo:str, setor:str, impacto:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cadastra um equipamento

        Arguments:
            nome: nome do equipamento.
            modelo: modelo do equipamento.
            setor: setor em que o equipamento opera.            
            data_insercao: data de quando o produto foi inserido à base
        """
        self.nome = nome
        self.modelo = modelo
        self.setor = setor
        self.impacto = impacto

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

   