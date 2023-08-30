from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users.db', echo=False)
Session = sessionmaker(bind = engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    
    

    def __repr__(self):
        return f'<User(name = {self.name}, fullname = {self.fullname}, nickname = {self.nickname})>'

if __name__ == '__main__':
    Base.metadata.create_all(engine)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Escribe un programa que pida al usuario un numero entero y muestre un triangulo como el siguiente

# 1
# 3 1
# 5 3 1
# 7 5 3 1
# 9 7 5 3 1

def funcion():
    numero = int(input("Dame un numero entero: "))
    for n in range(1,numero+1,2):
        for m in range(n,0,-2):
            print(m, end = ' ')
        print()
        