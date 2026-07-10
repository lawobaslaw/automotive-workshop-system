from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehicle(db.Model):

    id=db.Column(db.Integer,primary_key=True)

    registration=db.Column(db.String(20))

    make=db.Column(db.String(50))

    model=db.Column(db.String(50))

    year=db.Column(db.Integer)

class Job(db.Model):

    id=db.Column(db.Integer,primary_key=True)

    vehicle=db.Column(db.String(50))

    technician=db.Column(db.String(50))

    status=db.Column(db.String(30))

    cost=db.Column(db.Float)