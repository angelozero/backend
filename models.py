from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import string
import random
import math

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    # Running an initial load with random departments
    @staticmethod
    def insert_initial_values():
        departments = ["DESENVOLVIMENTO", "QUALIDADE", "MARKETING", "ADMINISTRATIVO"]
        for department in departments:
            if not Department.query.filter_by(name=department).first():
                new_department = Department(name=department)
                db.session.add(new_department)
        db.session.commit()


class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    second_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    department = db.relationship("Department", backref=db.backref("employees", lazy=True))
    date_time_creation = db.Column(db.DateTime)
    date_time_updated = db.Column(db.DateTime)

    # Running an initial load with random employee data
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

    # Executing a query paged by: page number, total records and department name
    @staticmethod
    def get_paginated_employees(page, total_page, department):
        formatted_results = []

        if department:
            employees_query = Employee.query.join(Department).filter(
                Department.name == department
            )
        else:
            employees_query = Employee.query

       
        total_records = employees_query.count()
        total_pages = math.ceil(total_records / total_page)

        if page < 1 or page > total_pages:
            return None 

        if total_records > 0:
            employees = employees_query.paginate(page=page, per_page=total_page)

            for employee in employees.items:
                department = Department.query.filter_by(id=employee.department_id).first()
                formatted_employee = {
                    "id": employee.id,
                    "name": employee.name,
                    "department": {
                        "id": department.id,
                        "name": department.name,
                    },
                    "date_time_creation": employee.date_time_creation.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "date_time_updated": (
                        employee.date_time_updated.strftime("%Y-%m-%d %H:%M:%S")
                        if employee.date_time_updated
                        else ""
                    ),
                }
                formatted_results.append(formatted_employee)

        return {
            "page": page,
            "total_pages": total_pages,
            "total_records": total_records,
            "results": formatted_results,
        }
