# Documentação da API
- Simples API de cadastro de funcionário em Python, Flask e PostgreSQL

## Executando a aplicação via Docker Compose
- *Necessário ter o [Docker](https://www.docker.com/) instalado*
- Faça uma cópia do projeto em sua máquina
    ```bash
    git clone git@github.com:angelozero/backend.git
    ```
- Acesse a pasta do projeto e execute o seguinte comando 
    ```bash
    $ docker compose up -d
    ```
- Acessar a url para documentação Swagger das rotas
    ```bash
    http://localhost:8080/apidocs/
    ```

## Configurações iniciais - Docker
- ### Subindo a aplicação via Docker
    - A imagem Docker se encontra no [DockerHub](https://hub.docker.com/repository/docker/angelozero/py-backend/general) ou no arquivo [Dockerfile](https://github.com/angelozero/backend/blob/main/Dockerfile) do projeto.

    - Acessar a rota `http://localhost:8080/servico_da_api` direto no navegador ou utilize o [Postman](https://www.postman.com/downloads/) e importe o arquivo [postman_collection.json](https://github.com/angelozero/backend/blob/main/postman_collection.json) disponibilizado no projeto.

- ### Subindo o banco via Docker
    - Acesse [PostgresSQL - Docker](https://hub.docker.com/_/postgres)
--- 
## Configurações iniciais - Local  
- ### Executando a aplicação localmente
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
            pip3 install joblib
            pip3 install pytest
            pip3 install hypothesis
            pip3 install numpy
            pip3 install scikit-learn
            pip3 install pandas
            ```
---
- ###  Executando a API via terminal
    - Para executar a API, use o comando:
        ```bash
        flask run
        ```
    - Url para acesso as rotas disponíveis da api: http://localhost:8080/

---
## Configuração, criação e carga inicial de dados

- Criação das tabelas e carga Inicial:
    - A criação das tabelas e suas correlações ocorrem automaticamente no momento da execução da api
    - Para toda vez que a aplicação é iniciada a seguinte ordem é executada:
        - 1 - Exclusão automática de todas as tabelas
        - 2 - Criação automática de todas as tabelas
        - 3 - Carga inicial com 20 endereços gerados em tempo de execução
        - 4 - Carga inicial com 4 departamentos gerados em tempo de execução
        - 5 - Carga inicial com 20 funcionários gerados em tempo de execução, vinculados a um departamento e endereço aleatório
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
- Para mais informações e detalhamentos técnicos acesse o arquivo [README-SQL-INFO](https://github.com/angelozero/backend/blob/main/README-SQL-INFO.md)


## Integração API ViaCEP
- A api [ViaCEP](viacep.com.br/ws/13063000/json/) é uma api externa que suporta as seguintes funções:
    - Retorna dados de endereço de acordo com o cep informado
    - Serviço utilizado para validação do cep e auto preenchimento do campos
        - UF
        - Cidade
        - Estado
    - Serviço utilizado para validar fluxos:
        - POST: Criação de um funcionário vinculado a um endereço
        - PUT: Alteração de um funcionário vinculado a um endereço

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
    - A parametrização da url que invoca a API ViaCEP fica em [config.ini](https://github.com/angelozero/backend/blob/main/config.ini)
    ```shell
        [viacep]
        BASE_URL = https://viacep.com.br/ws
    ```
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

## Machine Learning 
- Para informações de como o modelo de predição é gerado acesse o projeto [AngeloZero - Machine Learning](https://github.com/angelozero/machine_learning)

- O trecho a seguir permite fazer previsões sobre a probabilidade de um funcionário deixar a empresa com base em diversas características, usando um modelo de machine learning previamente treinado.

```python
import joblib
import numpy as np
import pandas as pd 
```

```python
# Carregar o modelo
model = joblib.load('best_model_employee_attrition.pkl')
feature_names = joblib.load('best_model_employee_feature_names.pkl')
```

```python
@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Criando um DataFrame a partir dos dados recebidos
    input_data = pd.DataFrame(
        {
            "satisfaction_level": [float(data["satisfaction_level"])],
            "last_evaluation": [float(data["last_evaluation"])],
            "number_project": [int(data["number_project"])],
            "average_montly_hours": [int(data["average_montly_hours"])],
            "time_spend_company": [int(data["time_spend_company"])],
            "work_accident": [int(data["work_accident"])],
            "promotion_last_5years": [int(data["promotion_last_5years"])],
            "dept": [data["dept"]],
            "salary": [data["salary"]],
        }
    )

    # Codificação One-Hot para 'dept'
    dept_dummies = pd.get_dummies(input_data['dept'], prefix='dept')
    input_data = pd.concat([input_data, dept_dummies], axis=1)
    input_data.drop('dept', axis=1, inplace=True)

    # Codificação Ordinal para 'salary'
    salary_mapping = {'low': 0, 'medium': 1, 'high': 2}
    input_data['salary'] = input_data['salary'].map(salary_mapping)

    # Asegurando que a entrada possui a mesma estrutura que o modelo
    input_data = input_data.reindex(columns=feature_names, fill_value=0)

    # Realizando a predição
    prediction = model.predict(input_data)

    # Armazenando o resultado em uma variável
    result = int(prediction[0])

    # Retornando a variável
    return jsonify({"prediction": result})
```

### Teste com PytTest

```python
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Carregando o modelo
model, model_columns = joblib.load('best_model_with_columns.pkl')

# Função de teste
def test_model_performance():
    # Gerando dados de teste fictícios (ou carregando um dataset de teste real)
    X_test_sample = pd.DataFrame({
        'last_evaluation': [0.7, 0.5, 0.3],
        'number_project': [3, 2, 5],
        'average_montly_hours': [150, 200, 100],
        'time_spend_company': [3, 2, 5],
        'Work_accident': [0, 1, 0],
        'promotion_last_5years': [0, 1, 0],
        'dept_IT': [1, 0, 0],
        'dept_sales': [0, 1, 0],
        'salary_low': [1, 0, 0],
        'salary_medium': [0, 1, 0],
        'salary_high': [0, 0, 1]
    })

    # Valores reais de satisfação (1 para satisfeito, 0 para insatisfeito)
    y_test_sample = np.array([1, 0, 0])  

    # Certifique-se de que as colunas estão na mesma ordem do modelo
    X_test_sample = X_test_sample.reindex(columns=model_columns, fill_value=0)

    # Predições do modelo
    y_pred = model.predict(X_test_sample)

    # Métricas de desempenho
    accuracy = accuracy_score(y_test_sample, y_pred)
    precision = precision_score(y_test_sample, y_pred)
    recall = recall_score(y_test_sample, y_pred)

    # Limites aceitáveis
    assert accuracy > 0.60, f"Acurácia do modelo abaixo do esperado: {accuracy:.2f}"
    assert precision <= 0.0, f"Precisão do modelo abaixo do esperado: {precision:.2f}"
    assert recall <= 0.0, f"Recall do modelo abaixo do esperado: {recall:.2f}"
```

## Fluxograma
- Mapa do fluxograma no backend
![fluxograma-via-cep](./images/fluxograma-backend.drawio.png)
        

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
| Joblib | https://pypi.org/project/joblib/ |
| Pytest | https://pypi.org/project/pytest/ |
| Hypothesis | https://pypi.org/project/hypothesis/ |
| Numpy | https://pypi.org/project/numpy/ |
| Scikit Lean | https://pypi.org/project/scikit-learn/ |
| Pandas | https://pandas.pydata.org/docs/getting_started/install.html |
