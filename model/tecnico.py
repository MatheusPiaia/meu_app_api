from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Tecnico(Base):
    __tablename__ = 'tecnicos'

    nome = Column(String(140))
    matricula = Column("pk_matricula", String(140), primary_key=True)
    turno = Column(String(140))

    manutencao = relationship("Manutencao", back_populates="tecnicos")

    def __init__(self, nome:str, matricula:str, turno:str):
        """
        Cadastra um técnico

        Arguments:
            nome: nome do técnico.
            turno: turno de trabalho do técnico            
        """
        self.nome = nome
        self.matricula = matricula
        self.turno = turno
     
