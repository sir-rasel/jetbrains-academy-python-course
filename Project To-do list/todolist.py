from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

# initialising the parent class for a table
Base = declarative_base()

class Task(Base):
    """ This is ORM table class for sqlite database """

    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        """ Table rows with id and respective task """
        return f"{self.id}. {self.task}"


class To_Do_List:
    """ This is To-do-list class with task handling operation """

    prompt = "1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n"

    def __init__(self, db_name):
        """ initialising the database and gui """

        # table and database initialising
        self.engine = create_engine(f"sqlite:///{db_name}.db?check_same_thread=False")
        Base.metadata.create_all(self.engine)

        # Session and interaction with database initialising
        self.session = sessionmaker(bind=self.engine)()

        # to-do-list gui initialising
        self.choices = {'1': self.show_today_tasks, '2': self.show_week_tasks, '3': self.show_all_tasks,
                        '4': self.show_missed_tasks, '5': self.add_task, '6': self.delete_task, '0': self.shutdown}
        self.running = True
        self.main()

    def shutdown(self):
        """ shuts down the program, by terminating the while loop and close the ORM session"""

        self.running = False
        self.session.close()
        print('Bye!')

    def show_today_tasks(self):
        """ Give the todays task list if empty show 'Nothing to do' """

        date_today = datetime.today()
        month = date_today.strftime('%b')
        day = date_today.day

        tasks = self.session.query(Task).filter(Task.deadline == date_today.date()).all()
        print(f"Today {day} {month}:")
        for task in tasks:
            print(task)
        if not tasks:
            print("Nothing to do!")

    def add_task(self):
        """ Adds a task to the database, with the deadline specified """

        task = input('Enter task:\n')
        deadline = datetime.strptime(input('Enter deadline:\n'), r'%Y-%m-%d')
        self.session.add(Task(task=task, deadline=deadline))
        self.session.commit()
        print("The task has been added!")

    def show_week_tasks(self):
        """ Shows the tasks for this week with day if has not task show 'Nothing to do!' """

        for date in (datetime.today() + timedelta(n) for n in range(7)):
            day = date.day
            day_name = date.strftime("%A")
            month = date.strftime('%b')
            tasks = self.session.query(Task).filter(Task.deadline == date.date()).all()
            print(f"{day_name} {day} {month}:")
            if tasks:
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task.task}")
            else:
                print("Nothing to do!")
            print()

    def show_all_tasks(self,flag=True):
        """ Shows every task with deadline existing in database """

        if flag:
            print("All tasks:")
        tasks = self.session.query(Task).order_by(Task.deadline).all()
        for task in tasks:
            month = task.deadline.strftime('%b')
            day = task.deadline.day
            print(f"{task.id}. {task.task}. {day} {month}")
        if not tasks:
            print("Nothing to do!")

    def show_missed_tasks(self):
        """ This shows those tasks that missed its deadline """

        print("Missed tasks:")
        tasks = self.session.query(Task).filter(Task.deadline < datetime.today().date()).order_by(Task.deadline).all()
        for task in tasks:
            month = task.deadline.strftime('%b')
            day = task.deadline.day
            print(f"{task.id}. {task.task}. {day} {month}")
        if not tasks:
            print("Nothing to do!")

    def delete_task(self):
        """Funtion for deleting the tasks from database """

        print("Chose the number of the task you want to delete:")
        self.show_all_tasks(False)
        number_of_deletion = int(input())

        tasks = self.session.query(Task).order_by(Task.deadline).all()
        if len(tasks) == 0:
            print("Nothing to delete")
        else:
            self.session.delete(tasks[number_of_deletion-1])
            self.session.commit()
            print("The task has been deleted!")

    def main(self):
        """ Driver function for all operation continuously running until manually stop """

        while self.running:
            choice = input(self.prompt)
            print()
            self.choices.get(choice, lambda: None)()
            print() if choice not in {'0', '2'} else None

if __name__ == "__main__":
    To_Do_List('todo')
