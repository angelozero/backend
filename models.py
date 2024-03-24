from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime

import string
import random
import math

db = SQLAlchemy()


class Departament(db.Model):
    __tablename__ = "departament"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    # initial values into the departments table"
    @staticmethod
    def insert_initial_values():
        departaments = ["Desenvolvimento", "Qualidade", "Marketing", "Administrativo"]
        for departament in departaments:
            if not Departament.query.filter_by(name=departament).first():
                new_departament = Departament(name=departament)
                db.session.add(new_departament)
        db.session.commit()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    second_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    departament_id = db.Column(db.Integer, db.ForeignKey("departament.id"))
    departament = db.relationship("Departament", backref=db.backref("users", lazy=True))
    date_time_creation = db.Column(db.DateTime)
    date_time_updated = db.Column(db.DateTime)

    # initial values into the users table
    @staticmethod
    def insert_initial_values():
        users_name = [
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

        for name in users_name:
            new_user = User(
                name=name,
                second_name="".join(
                    random.choice(string.ascii_lowercase) for i in range(10)
                ).capitalize(),
                email=name.lower()
                + "_"
                + "".join(random.choice(string.digits) for i in range(3))
                + "@email.com",
                departament_id=random.randint(1, 4),
                date_time_creation=datetime.now(),
            )
            db.session.add(new_user)
        db.session.commit()

    # paginated search results
    @staticmethod
    def get_paginated_users(page, total_page):
        formatted_results = []
        users = User.query.paginate(page=page, per_page=total_page)

        for user in users.items:
            departament = (
                Departament.query.filter_by(id=user.id_departament).first()
                if user.id_departament
                else None
            )
            formatted_user = {
                "id": user.id,
                "name": user.name,
                "departament": {
                    "id": departament.id,
                    "name": departament.name,
                },
                "date_time_creation": user.date_time_creation.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "date_time_updated": (
                    user.date_time_updated.strftime("%Y-%m-%d %H:%M:%S")
                    if user.date_time_updated
                    else ""
                ),
            }
            formatted_results.append(formatted_user)

        return {
            "page": page,
            "total_pages": math.ceil(users.total / total_page),
            "total_records": users.total,
            "results": formatted_results,
        }
