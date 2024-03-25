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

## Configuração, criação e carga inicial de dados
- Configuração:
    - Toda configuração para acesso ao banco de dados se encontra no arquivo .env ( criado no passo anteriormente e com a palavra `postgres` alterada para `postgresql` )
        ```shell
        // arquivo .env
        SQLALCHEMY_DATABASE_URI=postgresql://zdrxdzqw:ME10bkAcv78-0fQsibLtcyg5bEfxm5nl@raja.db.elephantsql.com/zdrxdzqw
        ```
- Criação:
    - A criação das tabelas ocorre no momento da execução da api
    - Para toda vez que a aplicação é iniciada a seguinte ordem é executada:
        - Exclusão de todas as tabelas
        - Criação de todas as tabelas
        - Carga inicial com 4 departamentos
        - Carga inicial com 20 funcionários
        ```python
        // arquivo app.py
        
        // ... some code here 
        
        with app.app_context():
        db.drop_all()
        db.create_all()
        Department.insert_initial_values()
        Employee.insert_initial_values()

        // ... some code here
        ```
    - O relacionamento entre Funcionários e Departamento ocorre aqui
        ```python
        // arquivo models.py
        class Employee(db.Model):
            __tablename__ = "employee"
            department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
            department = db.relationship("Department", backref=db.backref("employees", lazy=True))
        ```

- Carga Inicial de Dados
    - Carga inicial para Departamentos
        ```python
        // arquivo models.py
        @staticmethod
        def insert_initial_values():
            departments = ["DESENVOLVIMENTO", "QUALIDADE", "MARKETING", "ADMINISTRATIVO"]
            for department in departments:
                if not Department.query.filter_by(name=department).first():
                    new_department = Department(name=department)
                    db.session.add(new_department)
            db.session.commit()
        ```
    - Carga inicial para Funcionários
        ```python
        @staticmethod
        def insert_initial_values():
            employees_name = [
                "Alice",
                "Bob",
                "Charlie",
                "David",
                "Eva",
                "Frank",
                "Grace",
                "Hannah",
                "Ian",
                "Julia",
                "Kevin",
                "Linda",
                "Mike",
                "Nora",
                "Oscar",
                "Pam",
                "Quinn",
                "Rachel",
                "Steve",
                "Tina",
            ]

            for name in employees_name:
                new_employee = Employee(
                    name=name,
                    second_name="".join(
                        random.choice(string.ascii_lowercase) for i in range(10)
                    ).capitalize(),
                    email=name.lower()
                    + "_"
                    + "".join(random.choice(string.digits) for i in range(3))
                    + "@email.com",
                    department_id=random.randint(1, 4),
                    date_time_creation=datetime.now(),
                )
                db.session.add(new_employee)
            db.session.commit()
        ```


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
