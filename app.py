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
def list_user():
    paginated_users = User.get_paginated_users(
        request.args.get("pagina", 1, type=int), request.args.get("total", 5, type=int)
    )

    return paginated_users


@app.route("/departamentos", methods=["GET"])
def list_departament():
    all_departaments = Departament.query.all()
    results = departament_schema.dump(all_departaments)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
