from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flasgger import Swagger
from models import Employee, Department, db
from datetime import datetime
from dotenv import load_dotenv

import os
import re

load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()
    Department.insert_initial_values()
    Employee.insert_initial_values()

ma = Marshmallow(app)
swagger = Swagger(app, template_file="swagger/swagger.yaml")


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "department")


employees_schema = EmployeeSchema(many=True)


class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


department_schema = DepartmentSchema(many=True)


@app.route("/funcionarios", methods=["GET"])
def list_employees():
    department_name = request.args.get("departamento", None, type=str)
    name = request.args.get("nome", None, type=str)
    email = request.args.get("email", None, type=str)
    department_name = department_name.upper() if department_name else None

    paginated_employees = Employee.get_paginated_employees(
        request.args.get("pagina", 1, type=int),
        request.args.get("total", 5, type=int),
        department_name,
        name,
        email,
    )

    if paginated_employees is None:
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

    return jsonify(paginated_employees)


@app.route("/funcionario/<id>", methods=["GET"])
def employee_detail(id):
    employee = Employee.query.get(id)
    return employee_detail_response(employee)


@app.route("/funcionario", methods=["POST"])
def create_employee():
    data = request.json

    if "name" not in data or not data["name"]:
        return jsonify({"error": "Nome não foi enviado ou está vazio"}), 400

    if "email" not in data or not data["email"]:
        return jsonify({"error": "Email não foi enviado ou está vazio"}), 400

    if Employee.get_employee_by_email(data["email"]) is not None:
        return jsonify({"error": "Email já cadastrado"}), 400

    if (
        data["department_id"] is not None
        and not isinstance(data["department_id"], int)
        or data["department_id"] == 0
    ):
        return jsonify({"error": "Departamento inválido"}), 400

    if Department.query.filter_by(id=data["department_id"]).first() is None:
        return jsonify({"error": "Departamento não encontrado"}), 404

    new_employee = Employee(
        name=data["name"],
        second_name=data["second_name"],
        email=data["email"],
        department_id=data["department_id"],
        date_time_creation=datetime.now(),
        date_time_updated=None,
    )

    db.session.add(new_employee)
    db.session.commit()

    return employee_detail_response(new_employee), 201


@app.route("/funcionario/<id>", methods=["PUT"])
def update_employee(id):
    employee = Employee.query.get(id)

    if employee is None:
        return jsonify({"error": "Funcionário não encontrado"}), 404

    name = request.json.get("name")
    email = request.json.get("email")
    department_id = request.json.get("department_id")

    employee_by_email = Employee.get_employee_by_email(email)

    employee_by_email = Employee.get_employee_by_email(email)

    if (
        employee_by_email
        and employee_by_email.get("id") is not None
        and employee.id != employee_by_email["id"]
    ):
        return jsonify({"error": "Email já cadastrado"}), 400

    if email is not None and not is_valid_email(email):
        return jsonify({"error": "Email inválido"}), 400

    if (
        department_id is not None
        and not isinstance(department_id, int)
        or department_id == 0
    ):
        return jsonify({"error": "Departamento inválido"}), 400

    if department_id:
        if Department.query.filter_by(id=department_id).first() is None:
            return jsonify({"error": "Departamento não encontrado"}), 404

    if name or email or department_id:
        if name:
            employee.name = name
        if email:
            employee.email = email
        if department_id:
            employee.department_id = department_id

        employee.date_time_updated = datetime.now()

        db.session.commit()
        return employee_detail_response(employee), 201
    else:
        return jsonify({"message": "Nenhum dado para atualização fornecido"}), 400


@app.route("/funcionario/<id>", methods=["DELETE"])
def delete_employee(id):
    employee = Employee.query.get(id)

    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Funcionário excluído com sucesso"}), 200
    else:
        return jsonify({"error": "Funcionário não foi encontrado"}), 404


@app.route("/departamentos", methods=["GET"])
def list_department():
    all_departments = Department.query.all()
    results = department_schema.dump(all_departments)
    return jsonify(results)


@app.route("/departamento/<id>", methods=["GET"])
def department_detail(id):
    department = Department.query.get(id)
    if department:
        return {
            "id": department.id,
            "name": department.name,
        }
    else:
        return jsonify({"error": "Departamento não encontrado"}), 404


@app.route("/departamento", methods=["POST"])
def create_department():
    data = request.json

    if "name" not in data:
        return (
            jsonify(
                {
                    "error": "O campo 'name' para o cadastro de Departamento é obrigatório"
                }
            ),
            400,
        )

    existing_department = Department.query.filter_by(name=data["name"].upper()).first()
    if existing_department:
        return jsonify({"error": "Departamento já existe"}), 409

    new_department = Department(name=data["name"].upper())

    db.session.add(new_department)
    db.session.commit()

    return (
        jsonify({"id": new_department.id, "name": new_department.name}),
        201,
    )


def employee_detail_response(employee):
    if employee is None:
        return jsonify({"error": "Funcionário não encontrado"}), 404
    return {
        "id": employee.id,
        "name": employee.name,
        "second_name": employee.second_name,
        "email": employee.email,
        "department": {
            "id": employee.department.id,
            "name": employee.department.name,
        },
        "date_time_creation": employee.date_time_creation.strftime("%Y-%m-%d %H:%M:%S"),
        "date_time_updated": (
            employee.date_time_updated.strftime("%Y-%m-%d %H:%M:%S")
            if employee.date_time_updated
            else ""
        ),
    }


def is_valid_email(email):
    regex = r"^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(regex, email) is not None


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080, debug=True)
