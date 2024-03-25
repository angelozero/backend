# Detalhamento técnico sobre API e Banco
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