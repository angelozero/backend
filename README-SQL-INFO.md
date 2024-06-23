# Detalhamento técnico sobre API e Banco 

- ## Criação e configuração do banco:
    - ### Usando via Docker
        - O PostgreSQL está configurado em [docker-compose-yml](https://github.com/angelozero/backend/blob/main/docker-compose.yml)
        - Para criar o banco execute o seguinte comando: 
            ```bash
            docker compose up -d employee_db
            ```
    
    - ### Usando Localmente
        - Para testes usando a aplicação e o banco local, criar o arquivo na raiz do projeto `.env`
            - Adicionar a seguinte chave: 
            ```bash
            DB_URL=postgresql://postgres:postgres@localhost:5432/postgres
            ```
        - Acessar o site do [Postgres](https://www.postgresql.org/download/) e baixar o banco respectivo ao seu sistema operacional

        - Criar um banco com o nome `postgres`

- ## Criação e correlacionamento das tabelas:
    - A criação das tabelas ocorre no momento da execução da api
    - Para toda vez que a aplicação é iniciada a seguinte ordem é executada:
        - 1 - Exclusão de todas as tabelas
        - 2 - Criação de todas as tabelas
        - 3 - Carga inicial com 20 endereços
        - 4 - Carga inicial com 4 departamentos
        - 5 - Carga inicial com 20 funcionários
            ```python
            # arquivo app.py
            
            # ... some code here 
            
            with app.app_context():
            db.drop_all()
            db.create_all()
            Address.insert_initial_values()
            Department.insert_initial_values()
            Employee.insert_initial_values()

            # ... some code here
            ```
    - O relacionamento entre Funcionários, Departamento e Endereço ocorre aqui
        ```python
        # arquivo models.py
        class Employee(db.Model):
            __tablename__ = "employee"
            department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
            department = db.relationship("Department", backref=db.backref("employees", lazy=True))
            address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
            address = db.relationship("Address", backref=db.backref("addresses", lazy=True))
        ```

- ## Carga inicial de dados
    - Carga inicial para Endereços
        ```python
        class Address(db.Model):
        __tablename__ = "address"
        id = db.Column(db.Integer, primary_key=True)
        zipcode = db.Column(db.String(100))
        street = db.Column(db.String(100))
        number = db.Column(db.String(100))
        complement = db.Column(db.String(100))
        neighborhood = db.Column(db.String(100))
        city = db.Column(db.String(100))
        uf = db.Column(db.String(100))
        @staticmethod
        def insert_initial_values():
            faker = Faker('pt_BR')
            addresses = []

            for _ in range(20):
                address = Address(
                    zipcode=faker.postcode(),
                    street=faker.street_name(),
                    neighborhood=faker.bairro(),
                    complement = faker.license_plate(),
                    city=faker.city(),
                    uf=faker.state_abbr(),
                    number=faker.random_int(min=1, max=10000)
                )
                addresses.append(address)

            db.session.bulk_save_objects(addresses)
            db.session.commit()
        ```
    - Carga inicial para Departamentos
        ```python
        # arquivo models.py
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
                    address_id=random.randint(1, 20),
                    date_time_creation=datetime.now(),
                    
                )
                db.session.add(new_employee)
            db.session.commit()
        ```