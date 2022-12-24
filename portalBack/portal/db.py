from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random

# connect with data base
engine = create_engine('sqlite:///portal.sqlite', echo=True)
# manage tables
base = declarative_base()

class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

def init_db():
    base.metadata.create_all(engine)

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