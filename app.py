from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from models import User, Departament, db
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://famufcyv:FfNdYCVSXUxGr9g-i0IXhKGHPPsCCf-T@raja.db.elephantsql.com/famufcyv"
)


db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()
    Departament.insert_initial_values()
    User.insert_initial_values()

ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "departament")


users_schema = UserSchema(many=True)


class DepartamentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


departament_schema = DepartamentSchema(many=True)


@app.route("/usuarios", methods=["GET"])
def list_users():
    paginated_users = User.get_paginated_users(
        request.args.get("pagina", 1, type=int), request.args.get("total", 5, type=int)
    )
    return paginated_users


@app.route("/usuario/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_detail_response(user)


@app.route("/usuario", methods=["POST"])
def create_user():
    data = request.json

    # Verifica se o campo de Departamento esta presente
    if "name" not in data or "departament_id" not in data:
        return jsonify({"error": "Não foi enviado a informação de departamento"}), 400

    # Verifica se o ID do departamento é válido
    if Departament.query.filter_by(id=data["departament_id"]).first() is None:
        return jsonify({"error": "Departamento inválido"}), 400

    new_user = User(
        name=data["name"],
        second_name=data["second_name"],
        email=data["email"],
        departament_id=data["departament_id"],
        date_time_creation=datetime.now(),
        date_time_updated=None,
    )

    db.session.add(new_user)
    db.session.commit()

    return user_detail_response(new_user), 201


@app.route("/usuario/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    else:
        return jsonify({"error": "Usuário não foi encontrado"}), 404


@app.route("/departamentos", methods=["GET"])
def list_departament():
    all_departaments = Departament.query.all()
    results = departament_schema.dump(all_departaments)
    return jsonify(results)


@app.route("/departamento/<id>", methods=["GET"])
def departament_detail(id):
    departament = Departament.query.get(id)
    return {
        "id": departament.id,
        "departament": departament.name,
    }


@app.route("/departamento", methods=["POST"])
def create_departament():
    data = request.json

    # Verifica se todos os campos necessários estão presentes
    if "name" not in data:
        return (
            jsonify(
                {"error": "O campo nome para o cadastro de Departamento é obrigatório"}
            ),
            400,
        )

    # Verifica se já existe um departamento com o mesmo nome
    existing_departament = Departament.query.filter_by(
        name=data["name"].upper()
    ).first()
    if existing_departament:
        return jsonify({"error": "Departamento já existe"}), 409  # 409 - Conflict

    new_departament = Departament(name=data["name"].upper())

    db.session.add(new_departament)
    db.session.commit()

    return (
        jsonify({"id": new_departament.id, "name": new_departament.name}),
        201,
    )  # 201 - Created


def user_detail_response(user):
    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return {
        "id": user.id,
        "name": user.name,
        "second_name": user.second_name,
        "email": user.email,
        "departament": {
            "id": user.departament.id,
            "name": user.departament.name,
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
