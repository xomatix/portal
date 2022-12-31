from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from flask import Blueprint, current_app
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (url_safe  as Serializer, BadSignature, SignatureExpired)
import random

# connect with data base
engine = create_engine('sqlite:///portal.sqlite', echo=True)

base = declarative_base()

bp = Blueprint('db', __name__)

class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password_hash = Column(String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self):
        s = Serializer.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None 
        except BadSignature:
            return None
        session = get_db()
        user = session.query(User).filter_by(id=data['id']).first()
        return user

def init_db():
    base.metadata.create_all(engine)

#init_db()

def get_db():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

#adding random data
def add_data(session):
    for i in range(10,20):
            name = ''.join(chr(random.randint(97,122)) for _ in range(3))
            email = ''.join(chr(random.randint(97,122)) for _ in range(3)) + '@example.com'

            usr = User(name=name, email=email)
            session.add(usr)

    session.commit()
#add_data(get_db())

def search_db(session):
    d = session.query(User).filter(User.name.contains('%a%'))

    for q in d:
        print(q.id, q.name, q.email)

#search_db(get_db())