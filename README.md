# API APlicação gerenciamento manutenção empilhadeiras

# Índice

* [Instalação](#-instalação)

# 🎲 Instalação
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal e executar:
pip install -r requirements.txt

Este comando instala as dependências/bibliotecas, descritas no arquivo requirements.txt.

Para executar a API basta executar:

flask run --host 0.0.0.0 --port 5000
Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.

flask run --host 0.0.0.0 --port 5000 --reload

Abra o http://localhost:5000/#/ no navegador para verificar o status da API em execução.

# Descrição
Aplicação desenvolvida como MVP para a Sprint: Desenvolvimento Full Stack Básico no curso de Engenharia de Software.
Esta aplicação tem o objetivo de criar um ambiente visual para facilitar a comunicação entre os fornecedores (manutenção) e os clientes (produção), fornecendo informações de quais equipamentos estão "Em manutenção", na "Fila para Manutenção", "Aguardando peças" para ser possível executar o reparo e "Finalizado".


# Funcionalidades
- [x] Cadastro de Equipamentos
- [x] Cadastro de Técnicos
- [x] Cadastro de Manutenções separadas por Status

Após a Execução da API é possível acessar a documentação via Swagger e verificar/testar todas as funcionalidades da aplicação.
Abaixo segue todas as rotas da API




# 🛠 Tecnologias utilizadas
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [OpenAPI3](https://swagger.io/solutions/getting-started-with-oas/)

# Autor
---

<a href="https://github.com/MatheusPiaia">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/185968337?s=400&u=b4f54f3c5ea4b83b959d508547adf7077fd2caf8&v=4" width="100px;" alt=""/>
 <br />
 <sub><b>Matheus Piaia</b></sub></a> <a href="https://github.com/MatheusPiaia" title="GitHub">🚀</a>
 [![Linkedin Badge](https://img.shields.io/badge/-Matheus-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/matheus-piaia-231647144)](https://www.linkedin.com/in/matheus-piaia-231647144) 
