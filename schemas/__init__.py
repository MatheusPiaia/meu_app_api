from schemas.equipamento import EquipamentoSchema, EquipamentoBuscaSchema, ListagemEquipamentoSchema, \
                                EquipamentoDelSchema, EquipamentoViewSchema,\
                                 apresenta_equipamentos, apresenta_equipamento
from schemas.tecnico import TecnicoSchema, TecnicoDelSchema, TecnicoBuscaSchema, TecnicoViewSchema, \
                            ListagemTecnicoSchema, apresenta_tecnicos, apresenta_tecnico
from schemas.manutencao import ManutencaoSchema, ManutencaoBuscaSchema, ListagemManutencaoSchema, \
                                ManutencaoDelSchema, ManutencaoViewSchema, \
                                ManutencaoIdSchema, apresenta_manutencoes, apresenta_manutencao, \
                                ManutencaoStatusSchema, ManutencaoPath
from schemas.error import ErrorSchema