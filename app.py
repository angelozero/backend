from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow

from models import User, Departament, db

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


@app.route("/usuarios/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
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


@app.route("/departamentos", methods=["GET"])
def list_departament():
    all_departaments = Departament.query.all()
    results = departament_schema.dump(all_departaments)
    return jsonify(results)


@app.route("/departamentos/<id>", methods=["GET"])
def departament_detail(id):
    departament = Departament.query.get(id)
    return {
        "id": departament.id,
        "departament": departament.name,
    }


if __name__ == "__main__":
    app.run(debug=True)
