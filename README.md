# Documentação da API

## Configuração do Ambiente

- Crie um arquivo `.env` na pasta raiz do projeto.
- Adicione a chave `SQLALCHEMY_DATABASE_URI` no arquivo `.env`.
- Acesse o site [ElephantSQL](https://www.elephantsql.com/) e faça login.
    - *Obs.: O ElephantSQL chegará ao fim de sua vida útil em 27 de janeiro de 2025. Considere usar outro provedor.*
- Crie uma nova instância com o nome "company".
- Acesse a instância criada e recupere o valor dentro de "URL".
- Exemplo de URL: `postgres://ewdmssig:5-GGe88HTw2i6DEngLVvcVY8dzpPcxVu@castor.db.elephantsql.com/ewdmssig`.
- No arquivo `.env`, substitua o valor da URL de `postgres` para `postgresql`.
  - Exemplo: `SQLALCHEMY_DATABASE_URI=postgresql://ewdmssig:5-GGe88HTw2i6DEngLVvcVY8dzpPcxVu@castor.db.elephantsql.com/ewdmssig`.

## Inicialização do Ambiente

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

## Execução da API - Swagger

- Para executar a API, use o comando:
    ```shell
    flask run
    ```
- Url para acesso ao Swagger

    - http://127.0.0.1:5000/apidocs/


### Documentação das dependências utilizadas
---
- [Flask](https://flask.palletsprojects.com/en/3.0.x/quickstart/)
- [Flask Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- [SQL Alchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/)
- [Python Dotenv](https://medium.com/@habbema/dotenv-9915bd642533)
- [Psycopg2 Binary](https://www.psycopg.org/docs/install.html#quick-install)
- [Flasgger](https://github.com/flasgger/flasgger/blob/master/README.md)
- [Marshmallow Sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
