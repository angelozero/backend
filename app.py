from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from models import User, Department, db
from datetime import datetime
from dotenv import load_dotenv

import os

load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI


db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()
    Department.insert_initial_values()
    User.insert_initial_values()

ma = Marshmallow(app)
swagger = Swagger(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "department")


users_schema = UserSchema(many=True)


class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


department_schema = DepartmentSchema(many=True)


@app.route("/usuarios", methods=["GET"])
def list_users():
    """
    Listando usuários
    ---
    parameters:
      - name: pagina
        in: query
        description: Número da página correspondente a pesquisa
        required: false
        default: 1
      - name: total
        in: query
        type: integer
        description: Total de registros que serão retornados por página
        required: false
        default: 5
      - name: departamento
        in: query
        type: string
        description: Nome do departamento
        required: false
    responses:
      200:
        description: Um lista páginada de usuários
        schema:
          type: array
          items:
            id:
              type: integer
              description: Id do usuário
            name:
              type: string
              description: Nome do usuário
            department:
              type: string
              description: Nome do departamento
    """
    department_name = request.args.get("departamento", None, type=str)
    department_name = department_name.upper() if department_name else None

    paginated_users = User.get_paginated_users(
        request.args.get("pagina", 1, type=int),
        request.args.get("total", 5, type=int),
        department_name,
    )

    if paginated_users is None:
        return (
            jsonify(
                {
                    "page": request.args.get("pagina", 1, type=int),
                    "total_pages": 0,
                    "total_records": 0,
                    "results": [],
                }
            ),
            200,
        )

    return jsonify(paginated_users)


@app.route("/usuario/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_detail_response(user)


@app.route("/usuario", methods=["POST"])
def create_user():
    data = request.json

    # Verifica se o campo de Departmento esta presente
    if "name" not in data or "department_id" not in data:
        return jsonify({"error": "Não foi enviado a informação de departmento"}), 400

    # Verifica se o ID do departmento é válido
    if Department.query.filter_by(id=data["department_id"]).first() is None:
        return jsonify({"error": "Departmento inválido"}), 400

    new_user = User(
        name=data["name"],
        second_name=data["second_name"],
        email=data["email"],
        department_id=data["department_id"],
        date_time_creation=datetime.now(),
        date_time_updated=None,
    )

    db.session.add(new_user)
    db.session.commit()

    return user_detail_response(new_user), 201


@app.route("/usuario/<id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404

    name = request.json["name"]
    email = request.json["email"]

    user.name = name
    user.email = email

    db.session.commit()
    return user_detail_response(user), 201


@app.route("/usuario/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    else:
        return jsonify({"error": "Usuário não foi encontrado"}), 404


@app.route("/departmentos", methods=["GET"])
def list_department():
    all_departments = Department.query.all()
    results = department_schema.dump(all_departments)
    return jsonify(results)


@app.route("/departmento/<id>", methods=["GET"])
def department_detail(id):
    department = Department.query.get(id)
    return {
        "id": department.id,
        "department": department.name,
    }


@app.route("/departmento", methods=["POST"])
def create_department():
    data = request.json

    # Verifica se todos os campos necessários estão presentes
    if "name" not in data:
        return (
            jsonify(
                {"error": "O campo nome para o cadastro de Departmento é obrigatório"}
            ),
            400,
        )

    # Verifica se já existe um departmento com o mesmo nome
    existing_department = Department.query.filter_by(name=data["name"].upper()).first()
    if existing_department:
        return jsonify({"error": "Departmento já existe"}), 409

    new_department = Department(name=data["name"].upper())

    db.session.add(new_department)
    db.session.commit()

    return (
        jsonify({"id": new_department.id, "name": new_department.name}),
        201,
    )


def user_detail_response(user):
    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return {
        "id": user.id,
        "name": user.name,
        "second_name": user.second_name,
        "email": user.email,
        "department": {
            "id": user.department.id,
            "name": user.department.name,
        },
        "date_time_creation": user.date_time_creation.strftime("%Y-%m-%d %H:%M:%S"),
        "date_time_updated": (
            user.date_time_updated.strftime("%Y-%m-%d %H:%M:%S")
            if user.date_time_updated
            else ""
        ),
    }


if __name__ == "__main__":
    app.run(debug=True)
