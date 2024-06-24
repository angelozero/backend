# Documentação da API
- Simples API de cadastro de funcionário em Python, Flask e PostgreSQL

## Executando a aplicação via Docker Compose
- Faça uma cópia do projeto em sua máquina
    ```bash
    git clone git@github.com:angelozero/backend.git
    ```
- Executar o comando 
    ```bash
    $ docker compose up -d
    ```
- Acessar a url para documentação Swagger das rotas
    ```bash
    http://localhost:8080/apidocs/
    ```

## Executando a aplicação localmente
- ### Configurações iniciais
    - Faça uma cópia do projeto em sua máquina
        ```bash
        git clone git@github.com:angelozero/backend.git
        ```
    - Acesse a pasta 
        ```bash
        $ cd backend
        ```
    - Crie um arquivo do tipo `.env` na pasta raiz do projeto.
    - Adicione a seguinte chave
        ```bash
        DB_URL=postgresql://postgres:postgres@localhost:5432/postgres
        ```
---
- ### Subindo o banco via Docker
    - Dentro da pasta `backend` executar o seguinte compando
        ```bash
        docker compose up -d employee_db
        ```
---
- ### Subindo o banco localmente
    - Acessar o site do [Postgres](https://www.postgresql.org/download/) e baixar o banco respectivo ao seu sistema operacional

    - Criar um banco com o nome `postgres`
---
- ### Incializando o ambiente
    - Para inicializar o ambiente virtual, execute o comando ( *é necessário ter o [Python](https://www.python.org/downloads/) instalado* ):
        ```bash
        $ python3 -m venv .venv
        ```
        - ou
        ```bash
        $ . .venv/bin/activate
        ```
---
- ### Instalação das Dependências

    - Instale as dependências usando os seguintes comandos:
    - Acesse a pasta `backend`
        - Através do arquivo `requirements.txt`
            ```bash
            pip3 install -r requirements.txt
            ```
        - Ou dentro do ambiente `. venv`
            ```bash
            pip3 install Flask
            pip3 install flask_marshmallow
            pip3 install SQLAlchemy
            pip3 install Flask-SQLAlchemy
            pip3 install python-dotenv
            pip3 install psycopg2-binary
            pip3 install flasgger
            pip3 install marshmallow-sqlalchemy
            pip3 install faker    
            pip3 install requests
            ```
---
- ###  Executando da API

    - Para executar a API, use o comando:
        ```bash
        flask run
        ```
    - Url para acesso as rotas disponíveis da api: http://localhost:8080/


## Configuração, criação e carga inicial de dados

- Criação das tabelas e carga Inicial:
    - A criação das tabelas e suas correlações ocorrem automaticamente no momento da execução da api
    - Para toda vez que a aplicação é iniciada a seguinte ordem é executada:
        - 1 - Exclusão automática de todas as tabelas
        - 2 - Criação automática de todas as tabelas
        - 3 - Carga inicial com 4 departamentos gerados em tempo de execução
        - 4 - Carga inicial com 20 funcionários gerados em tempo de execução, vinculados a um departamento aleatório
            ```python
            # arquivo app.py
            
            # ... some code here 
            
            with app.app_context():
            db.drop_all()
            db.create_all()
            Department.insert_initial_values()
            Employee.insert_initial_values()

            # ... some code here
            ```
- Para mais informações e detalhamentos técnicos acesse o arquivo [README-SQL-INFO](https://github.com/angelozero/backend/blob/main/README-SQL-INFO.md)


## API ViaCEP
- Para a criação e/ou atualização de um endereço do funcionário é necessário enviar apenas um cep válido.
    - As seguintes informações serão preenchidas automáticamente de acordo com o retorno da [API ViaCEP](viacep.com.br/ws/13063000/json/)
        - UF
        - Cidade 
        - Estado 

    - As seguintes informações não são de envio obrigatório
        - Rua
        - Numero
        - Bairro
        - Complemento
    - O serviço pode ser consultado na classe [via_cep_service.py](https://github.com/angelozero/backend/blob/main/via_cep_service.py)
    ```python
        import requests
        import configparser


        class ViaCEPService:
            def __init__(self, config_file="config.ini"):
                self.base_url = self.load_base_url(config_file)

            def load_base_url(self, config_file):
                config = configparser.ConfigParser()
                config.read(config_file)
                return config["viacep"]["BASE_URL"]

            def get_address_info(self, cep):
                try:
                    response = requests.get(f"{self.base_url}/{cep}/json/")

                    if response.status_code != 200:
                        return
                    
                    data = response.json()
                    return data

                except requests.exceptions.RequestException as req_err:
                    return {"error": f"API CEP - Request error: {req_err}"}

                except Exception as err:
                    return {"error": f"API CEP - An error occurred: {err}"}
    ```
    - Fluxograma
        ![alt text](./images/fluxograma-via-cep.png)
        

## Swagger
- Acessem em http://localhost:8080/apidocs/
    ![swagger](./images/swagger.png)


## Postman
- Importar para dentro do postman o arquivo `postman_collection.json`
![postman](./images/postman.png)

## Documentação das dependências utilizadas

| Plugin | Documentação |
| ------ | ------------ |
| Flask | https://flask.palletsprojects.com/en/3.0.x/quickstart/ |
| Flask Marshmallow | https://flask-marshmallow.readthedocs.io/en/latest/ |
| Flask CORS | https://flask-cors.readthedocs.io/en/latest/ |
| SQL Alchemy | https://docs.sqlalchemy.org/en/20/orm/quickstart.html |
| Flask SQLAlchemy | https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/ |
| Python Dotenv | https://medium.com/@habbema/dotenv-9915bd642533 |
| Psycopg2 Binary | https://www.psycopg.org/docs/install.html#quick-install |
| Flasgger | https://github.com/flasgger/flasgger/blob/master/README.md |
| Marshmallow Sqlalchemy | https://marshmallow-sqlalchemy.readthedocs.io/en/latest/ |
| Faker | https://pypi.org/project/Faker/ |
| Requests | https://pypi.org/project/requests/ |
