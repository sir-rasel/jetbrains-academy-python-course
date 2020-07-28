from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def all_rows():
    rows = session.query(Table).all()
    task = list()
    for i in rows:
        task.append(i)

    for idx in range(len(task)):
        print(str((idx + 1)) + ".", task[idx])

    if(len(rows) == 0):
        print('Nothing to do!')

def add_row(new_input):
    new_row = Table(task=new_input, deadline=datetime.today())
    session.add(new_row)
    session.commit()


while(True):
    print("1) Today's tasks\n2) Add task\n0) Exit")
    first_input = int(input())

    if first_input == 1:
        all_rows()
    elif first_input == 2:
        add_row(input("Enter new Todo:"))
    else:
        print("Bye!")
        exit()
