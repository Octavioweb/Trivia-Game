from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

# Create a SQLite in-memory database
DATABASE_URL = "sqlite:///temp.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer)

# Create the table
Base.metadata.create_all(engine)

# Function to add an integer value to the database
def add_value(value):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_item = Item(value=value)
    session.add(new_item)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Error: Value already exists in the database.")
    session.close()

# Function to delete a value from the database
def delete_value(value):
    Session = sessionmaker(bind=engine)
    session = Session()
    item_to_delete = session.query(Item).filter_by(value=value).first()
    if item_to_delete:
        session.delete(item_to_delete)
        session.commit()
        print("Value deleted successfully.")
    else:
        print("Value not found in the database.")
    session.close()

# Function to retrieve the top 5 elements from the database
def get_top_5():
    Session = sessionmaker(bind=engine)
    session = Session()
    top_items = session.query(Item).order_by(Item.id).limit(5).all()
    session.close()
    return top_items

# Testing the functions
if __name__ == "__main__":
    add_value(10)
    add_value(20)
    add_value(30)
    add_value(40)
    add_value(50)
    
    print("Top 5 elements:")
    top_elements = get_top_5()
    for item in top_elements:
        print(item.id, item.value)
    
    delete_value(30)
    
    print("Top 5 elements after deletion:")
    top_elements = get_top_5()
    for item in top_elements:
        print(item.id, item.value)
