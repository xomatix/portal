from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask import Blueprint
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

class Category(base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String(256))
    posts = relationship('Post', backref='categories')

class Post(base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(4096))
    category_id = Column(Integer, ForeignKey('categories.id'))
    images = relationship('Image', backref='posts')

class Image(base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    url = Column(String(128))
    post_id = Column(Integer, ForeignKey('posts.id'))


def init_db():
    base.metadata.create_all(engine)

def get_db():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def delete_db():
    Post.__table__.drop(engine)
    session = get_db()
    session.delete(Post)
    session.commit()

#init_db()
#delete_db()

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