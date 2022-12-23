from flask import url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db

import sqlite3

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

def init_app(app):
    db = SQLAlchemy(app)
    
    with app.app_context():
        db.create_all()