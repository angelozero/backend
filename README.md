# Documentação da API

## Executando a aplicação via Docker Compose
- Executar o comando 
    ```bash
     docker compose up -d
    ```
- Acessar em 
    ```bash
    http://localhost:8080/apidocs/
    ```

## Configurando a aplicação localmente

- Crie um arquivo `.env` na pasta raiz do projeto.
- Adicione a seguinte chave
    - `DB_URL=postgresql://postgres:postgres@localhost:5432/postgres`

## Inicialização do Ambiente

- Subir um banco local via PostgreSQL chamado `postgres` ou execute o comando via Docker Compose
```shell
docker compose up -d employee_db
```

- Para inicializar o ambiente virtual, execute o comando:
```shell
python3 -m venv .venv
```

- Para iniciar o ambiente virtual, execute o comando:
```shell
. .venv/bin/activate
```

## Instalação das Dependências

- Instale as dependências usando os seguintes comandos:
- *Obs.: pip3 para o caso de estar usando Mac Os*
    - através do arquivo `requirements.txt`
    ```shell
    pip3 install -r requirements.txt
    ```
    - ou dentro do ambiente *venv*
    ```shell
    pip3 install Flask
    pip3 install flask_marshmallow
    pip3 install SQLAlchemy
    pip3 install Flask-SQLAlchemy
    pip3 install python-dotenv
    pip3 install psycopg2-binary
    pip3 install flasgger
    pip3 install marshmallow-sqlalchemy
    ```

## Execução da API

- Para executar a API, use o comando:
    ```shell
    flask run
    ```
- Url para acesso a api

    - http://localhost:8080/

## Configuração, criação e carga inicial de dados

- ### Usando via Docker
    - O PostgreSQL está configurado em [docker-compose-yml](https://github.com/angelozero/backend/blob/data-base-migration/docker-compose.yml)
    - Para criar o banco execute o seguinte comando: `docker compose up -d employee_db`

- ### Usando Localmente
    - Para testes usando a aplicação e o banco local, criar o arquivo na raiz do projeto: `.env`
        - Adicionar a seguinte chave: `DB_URL=postgresql://postgres:postgres@localhost:5432/postgres`

- Criação das tabelas e Carga Inicial:
    - A criação das tabelas e suas correlações ocorre automaticamente no momento da execução da api
    - Para toda vez que a aplicação é iniciada a seguinte ordem é executada:
        - Exclusão automática de todas as tabelas
        - Criação automática de todas as tabelas
        - Carga inicial com 4 departamentos gerados em tempo de execução
        - Carga inicial com 20 funcionários gerados em tempo de execução, vinculados a um departamento aleatório
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
- Para mais informações e detalhamentos técnicos
    - Acesse o arquivo [README-SQL-INFO](https://github.com/angelozero/backend/blob/main/README-SQL-INFO.md)

## Swagger
- Acessem em http://localhost:8080/apidocs/
    ![swagger](./images/swagger.png)

## Postman
- Importar para dentro do postman o arquivo `postman_collection.json`
![postman](./images/postman.png)

## Docker
- Baixar a imagem [angelozero/backend-py](https://hub.docker.com/repository/docker/angelozero/backend-py/general)
- Executar o comando 
    - `docker run -p 8080:8080 -e SQLALCHEMY_DATABASE_URI=ELEPHANT_SQL_URL angelozero/backend-py`
- Acesse o arquivo [README-DOCKER](https://github.com/angelozero/backend/blob/main/README-DOCKER.md) para mais informações de como baixar e executar a api via docker.

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
