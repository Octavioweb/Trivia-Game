from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

#Funcionamiento de manejo de bases de datos SQL usando el ORM de SQLALCHEMY y SQLite
Base = declarative_base()
engine=create_engine("sqlite:///leaderBoard.db", echo = True)
Session = sessionmaker(bind = engine)
session = Session()

class SingleScore(Base):
    __tablename__ = 'singlescore'
    id = Column(Integer, primary_key=True)
    questions = Column(String)
    name = Column(String)
    score = Column(Integer)
    date = Column(String) # se debe previamente formar un string usando os

    def __repr__(self):
        return f'   ESTO ES UN REPR   < singleScore(questions = {self.questions}, score = {self.score}, name = {self.name})>'
    
Base.metadata.create_all(engine)

#Funcion de agregar valor a dbo
class LeaderBoard():
    def __init__(self):
        print("Created SQL DataBase!")

    def put(self, questions, name, score, date):

        temp_item = SingleScore(questions = questions, name = name, score = score, date = date)
        session.add(temp_item)
        session.commit()

    def deleteAll(self):
        session.commit()
        itemsToDelete = session.query(SingleScore).all()

        for item in itemsToDelete:
            session.delete(item)
        session.commit()

    def selectTop5(self):
        #Function that returns top 5 players from both databases as a list. Rank by score
        questions10 = session.query(SingleScore).filter_by(questions = 10).order_by(SingleScore.score).limit(5).all()
        questions15 = session.query(SingleScore).filter_by(questions = 15).order_by(SingleScore.score).limit(5).all()
        print(questions10, questions15)
        return (questions10, questions15)
    
tablero = LeaderBoard()
t = time.localtime()

dateString =  time.strftime("%Y-%m-%d %H:%M:%S", t)
                       
tablero.put(questions = 15, name = 'Octavio', score = 10, date = dateString)
tablero.put(questions = 10, name = 'Arlberto', score = 11, date = dateString)
tablero.put(questions = 15, name = 'Albert', score = 12, date = dateString)
tablero.put(questions = 10, name = 'Octa', score = 13, date = dateString)
tablero.put(questions = 15, name = 'Carlos', score = 16, date = dateString)
tablero.put(questions = 10, name = 'Octi', score = 7, date = dateString)
tablero.put(questions = 15, name = 'Carl', score = 4, date = dateString)

tablero.selectTop5()
tablero.deleteAll()