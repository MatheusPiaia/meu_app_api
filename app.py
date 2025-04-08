from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify, request, render_template
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Equipamento, Tecnico, Manutencao
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo as tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
equipamento_tag = Tag(name="Equipamento", description="Adição, visualização e remoção de equipamentos a base")
tecnico_tag = Tag(name="Tecnico", description="Adição, visualização e remoção de técnicos a base")
manutencao_tag = Tag(name="Manutencao", desccription="Adição, visualização e remoção de equipamentos em manutencao a base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/equipamento', tags=[equipamento_tag],
          responses={"200":EquipamentoSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_equipamento(form: EquipamentoSchema):
    """Cadastra um novo Equipamento à base de dados
    
    Retorna uma representação de todos os equipamentos cadastrados"""
    equipamento = Equipamento(
        nome=form.nome,
        modelo=form.modelo,
        setor=form.setor,
        impacto=form.impacto)
    logger.debug(f"Adicionando equipamento de nome:'{equipamento.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando equipamento
        session.add(equipamento)
        # efetivando o cadastro de um novo equipamento a tabela
        session.commit()
        logger.debug(f"Adicionado equipamento de nome:'{equipamento.nome}'")
        return apresenta_equipamento(equipamento), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Equipamento de mesmo nome já salvo na base"
        logger.warning(f"Erro ao adicionar equipamento '{equipamento.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar cadastro do novo equipamento"
        logger.warning(f"Erro ao cadastrar novo equipamento '{equipamento.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/equipamentos', tags=[equipamento_tag],
         responses={"200":ListagemEquipamentoSchema})
def get_equipamentos():
    """Faz a busca por todos os Equipamentos cadastrados
    
    Retorna uma representação em forma de lista de todos os equipamentos
    cadastrados"""

    logger.debug(f"Coletando equipamentos no banco")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    equipamentos = session.query(Equipamento).all()

    if not equipamentos:
        # se não há equipamentos cadastrados
        return {"equipamentos":[]}, 200
    else:
        logger.debug(f"{len(equipamentos)} equipamentos encontrados")
        # retorna a representação de equipamento
        print(equipamentos)
        return apresenta_equipamentos(equipamentos), 200


@app.delete('/equipamento', tags=[equipamento_tag],
            responses={"200":EquipamentoDelSchema, "404":ErrorSchema})
def del_equipamento(query:EquipamentoBuscaSchema):
    """Deleta o cadastro de um equipamento a partir do nome informado
    
    Retorna uma mensagem de confirmação da remoção
    """
    equipamento_nome = unquote(unquote(query.nome))    
    logger.debug(f"Deletando dados sobre o equipamento {equipamento_nome}")
    #criando conexão com o banco
    session=Session()
    
    try:
        # Verifica se existe manutenção associada
        manutencao = session.query(Manutencao).filter(Manutencao.nome_equipamento == equipamento_nome).first()
        if manutencao:
            error_msg = "Não foi possível deletar o equipamento, pois há manutenção vinculada."
            logger.warning(f"Erro ao deletar equipamento '{equipamento_nome}': {error_msg}")
            return {"mesage": error_msg}, 400

        # Se não há manutenção, tenta deletar
        count = session.query(Equipamento).filter(Equipamento.nome == equipamento_nome).delete()
        session.commit()

        if count:
            logger.debug(f"Deletado equipamento {equipamento_nome}")
            return {"mesage": "Equipamento removido", "nome": equipamento_nome}, 200
        else:
            error_msg = "Equipamento não encontrado na base"
            logger.warning(f"Erro ao deletar equipamento '{equipamento_nome}': {error_msg}")
            return {"mesage": error_msg}, 404

    except IntegrityError as e:
        session.rollback()
        logger.error(f"Erro de integridade ao deletar '{equipamento_nome}': {str(e)}")
        return {"mesage": "Erro de integridade. Possível vínculo com outros registros."}, 400

    except Exception as e:
        session.rollback()
        logger.error(f"Erro inesperado ao deletar '{equipamento_nome}': {str(e)}")
        return {"mesage": "Erro interno do servidor."}, 500


@app.post('/tecnico', tags=[tecnico_tag],
          responses={"200":TecnicoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tecnico(form: TecnicoSchema):
    """Cadastra um novo Técnico à base de dados
    
    Retorna uma representação de todos os técnicos cadastrados"""
    tecnico = Tecnico(
        nome=form.nome,
        matricula=form.matricula,
        turno=form.turno)
    logger.debug(f"Adicionando técnico de nome:'{tecnico.nome}' e matrícula '{tecnico.matricula}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando tecnico
        session.add(tecnico)
        # efetivando o cadastro do tecnico a tabela
        session.commit()
        logger.debug(f"Adicionado tecnico de nome:'{tecnico.nome}' e matricula '{tecnico.matricula}'")
        return apresenta_tecnico(tecnico), 200
    
    except IntegrityError as e:
        # como a duplicidade de matricula é a provável razão do IntegrityError
        error_msg = "Técnico de mesma matricula já salvo na base"
        logger.warning(f"Erro ao adicionar técnico de matriula '{tecnico.matricula}', {error_msg}")
        return {"mesage": error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar cadastro do novo técnico"
        logger.warning(f"Erro ao cadastrar novo técnico de matricula '{tecnico.matricula}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/tecnicos', tags=[tecnico_tag],
         responses={"200":ListagemTecnicoSchema})
def get_tecnicos():
    """Faz a busca por todos os Tecnicos cadastrados
    
    Retorna uma representação em forma de lista de todos os tecnicos
    cadastrados"""

    logger.debug(f"Coletando tecnicos no banco")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tecnicos = session.query(Tecnico).all()

    if not tecnicos:
        # se não há tecnicos cadastrados
        return {"tecnicos":[]}, 200
    else:
        logger.debug(f"{len(tecnicos)} tecnicos encontrados")
        # retorna a representação de tecnico
        print(tecnicos)
        return apresenta_tecnicos(tecnicos), 200


@app.delete('/tecnico', tags=[tecnico_tag],
            responses={"200":TecnicoDelSchema, "404":ErrorSchema})
def del_tecnico(query:TecnicoBuscaSchema):
    """Deleta o cadastro de um técnico a partir da matrícula informada
    
    Retorna uma mensagem de confirmação da remoção
    """
    tecnico_matricula = unquote(unquote(query.matricula))    
    logger.debug(f"Deletando dados sobre o técnico {tecnico_matricula}")
    #criando conexão com o banco
    session=Session()

    try:
        # Verifica se existe manutenção associada
        manutencao = session.query(Manutencao).filter(Manutencao.matricula_tecnico == tecnico_matricula).first()
        if manutencao:
            error_msg = "Não foi possível deletar o técnico, pois há manutenção vinculada."
            logger.warning(f"Erro ao deletar técnico '{tecnico_matricula}': {error_msg}")
            return {"mesage": error_msg}, 400

        # Se não há manutenção, tenta deletar
        count = session.query(Tecnico).filter(Tecnico.matricula == tecnico_matricula).delete()
        session.commit()

        if count:
        # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado técnico {tecnico_matricula}")
            return {"mesage": "Técnico removido", "nome": tecnico_matricula}, 200
        else:
        #se o técnico não foi encontrado
            error_msg = "Técnico não encontrado na base"
            logger.warning(f"Erro ao deletar técnico '{tecnico_matricula}', {error_msg}")
            return {"mesage": error_msg}, 404

    except IntegrityError as e:
        session.rollback()
        logger.error(f"Erro de integridade ao deletar '{tecnico_matricula}': {str(e)}")
        return {"mesage": "Erro de integridade. Possível vínculo com outros registros."}, 400

    except Exception as e:
        session.rollback()
        logger.error(f"Erro inesperado ao deletar '{tecnico_matricula}': {str(e)}")
        return {"mesage": "Erro interno do servidor."}, 500
   

@app.get('/manutencoes/status', tags=[manutencao_tag],
         responses={"200":ListagemManutencaoSchema, "404":ErrorSchema})
def get_manutencoes(query: ManutencaoStatusSchema):
    """Faz a busca por todos as Manutencoes cadastrados com o status informado
    
    Retorna uma representação em forma de lista de todas as manutencoes do status
    buscado cadastradas"""
    manutencao_status = unquote(unquote(query.status))
    try:
        logger.debug(f"Buscando manutenções com status: {manutencao_status}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        manutencoes = session.query(Manutencao).filter(Manutencao.status == manutencao_status).all()

        if not manutencoes:
            #logger.debug(f"Nenhuma manutenção encontrada com status: {manutencao_status}")
            return {"manutenções":[]}, 200  # Retorna lista vazia no formato esperado
        else:
            #logger.debug(f"Encontradas {len(manutencoes)} manutenções com status: {manutencao_status}")
            # retorna a representação das manutencoes em lista
            #print(manutencoes)
            return apresenta_manutencoes(manutencoes), 200
    except Exception as e:
        logger.error(f"Erro ao buscar manutenções: {str(e)}")
        return {"error": "Erro interno no servidor", "details": str(e)}, 500

    
@app.get('/manutencoes', tags=[manutencao_tag],
         responses={"200":ListagemManutencaoSchema, "404":ErrorSchema})
def get_manutencoes_all():
    """Faz a busca por todos as Manutencoes cadastradas
    
    Retorna uma representação em forma de lista de todas as manutencoes cadastradas"""
    try:
        logger.debug(f"Buscando manutenções")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        manutencoes = session.query(Manutencao).all()

        if not manutencoes:
            #logger.debug(f"Nenhuma manutenção encontrada com status: {manutencao_status}")
            return {"manutenções":[]}, 200  # Retorna lista vazia no formato esperado
        else:
            #logger.debug(f"Encontradas {len(manutencoes)} manutenções com status: {manutencao_status}")
            # retorna a representação das manutencoes em lista
            #print(manutencoes)
            return apresenta_manutencoes(manutencoes), 200
    except Exception as e:
        logger.error(f"Erro ao buscar manutenções: {str(e)}")
        return {"error": "Erro interno no servidor", "details": str(e)}, 500


@app.post('/manutencao', tags=[manutencao_tag],
          responses={"200": ManutencaoViewSchema, "404":ErrorSchema})
def add_manutencao(form: ManutencaoSchema):
    """Cadastro de uma nova manutencao à base de dados
    
    Retorna uma representação da Manutencao cadastrada"""
    manutencao = Manutencao(
        nome_equipamento= form.nome_equipamento,
        matricula_tecnico= form.matricula_tecnico,
        status= form.status,
        tipo_manutencao= form.tipo_manutencao,
        comentario= form.comentario,
        previsao_conclusao= form.previsao_conclusao
    )
    logger.debug(f"Adicionando manutencao")
    try:
        #criando conexão com a base
        session = Session()
        #adicionando manutencao
        session.add(manutencao)
        #efetivando o cadastro do tecnico a tabela
        session.commit()
        logger.debug(f"Adicionada manutencao")
        return apresenta_manutencao(manutencao)
    
    except IntegrityError as e:
        # como a duplicidade de matricula é a provável razão do IntegrityError
        error_msg = "Máquina já está em manutenção"
        logger.warning(f"Erro ao adicionar manutencao da máquina '{manutencao.nome_equipamento}', {error_msg}")
        return {"mesage": error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar manutencao"
        logger.warning(f"Erro ao cadastrar manutencao da máquina '{manutencao.nome_equipamento}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.patch('/manutencao/<int:id>', tags=[manutencao_tag],
          responses={"200": ManutencaoViewSchema, "404":ErrorSchema} )
def patch_manutencao(path: ManutencaoPath, form:ManutencaoStatusSchema):
    """Atualiza parcialmente uma manutenção existente com dados de um formulário.

    Apenas os campos enviados no formulário serão alterados.
    """
    id = path.id
    logger.debug(f"Buscando manutenção com ID {id} para atualização parcial")

    try:
        session = Session()
        manutencao = session.query(Manutencao).filter(Manutencao.id == id).first()

        if not manutencao:
            error_msg = "Manutenção não encontrada"
            logger.warning(f"Erro ao atualizar manutenção ID {id}: {error_msg}")
            return {"message": error_msg}, 404

        # Como apenas alguns dados serão enviados não será usado um Schema
        # e sim os dados do formulário enviado na requisição
        
        data = request.form

        # Atualiza apenas os campos informados no form
        if "nome_equipamento" in data:
            manutencao.nome_equipamento = data["nome_equipamento"]
        if "matricula_tecnico" in data:
            manutencao.matricula_tecnico = data["matricula_tecnico"]
        if "status" in data:
            manutencao.status = data["status"]
        if "tipo_manutencao" in data:
            manutencao.tipo_manutencao = data["tipo_manutencao"]
        if "comentario" in data:
            manutencao.comentario = data["comentario"]
        if "previsao_conclusao" in data:
            manutencao.previsao_conclusao = data["previsao_conclusao"]
                    
        session.commit()

        logger.debug(f"Manutenção ID {id} atualizada parcialmente com sucesso")
        return apresenta_manutencao(manutencao), 200

    except Exception as e:
        session.rollback()
        error_msg = f"Erro ao atualizar parcialmente a manutenção: {str(e)}"
        logger.error(f"Erro inesperado ao atualizar manutenção ID {id}: {error_msg}")
        return {"message": error_msg}, 500

    finally:
        session.close()


@app.delete('/manutencao', tags=[manutencao_tag],
            responses={"200":ManutencaoDelSchema, "404":ErrorSchema})
def del_manutencao(query:ManutencaoIdSchema):
    """Deleta o cadastro de uma manutencao a partir do id informado
    
    Retorna uma mensagem de confirmação da remoção
    """
    id_manutencao = query.id
    print(id_manutencao)
    logger.debug(f"Deletando dados sobre o técnico {id_manutencao}")
    #criando conexão com o banco
    session=Session()
    #fazendo a remoção
    count = session.query(Manutencao).filter(Manutencao.id == id_manutencao).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado manutenção {id_manutencao}")
        return {"mesage": "Manutenção removida", "ID": id_manutencao}, 200
    else:
        #se o equipamento não foi encontrado
        error_msg = "Manutenção não encontrada na base"
        logger.warning(f"Erro ao deletar manutenção '{id_manutencao}', {error_msg}")
        return {"mesage": error_msg}, 404

