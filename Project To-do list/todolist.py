from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DATE
from sqlalchemy.orm.session import sessionmaker
from datetime import datetime, timedelta

DATA_BASE_TYPE = 'sqlite'
DATA_BASE_PATH = '.\\todo.db'
CHECK_SAME_THREAD = False
TableBase = declarative_base()


class TableTask(TableBase):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='New Task')
    deadline = Column(DATE, default=datetime.today())

    def __repr__(self):
        return self.task

    def __str__(self):
        return self.__repr__()


class DataBaseUtil:
    """ DataBase Util """
    Session = ""

    def __init__(self, *args, **kwargs):
        if "session_engine" in kwargs.keys():
            DataBaseUtil.Session = kwargs['session_engine']
        if DataBaseUtil.Session == "":
            print("Error")
            raise Exception("Session Error")

    @staticmethod
    def insert(**kwargs):
        session = DataBaseUtil.Session()
        try:
            if 'id' in kwargs.keys():
                new_row = TableTask(id=kwargs['id'], task=kwargs['task'], deadline=kwargs['deadline'])
            else:
                new_row = TableTask(task=kwargs['task'], deadline=kwargs['deadline'])
            session.add(new_row)
            session.commit()
        except Exception():
            print("Args Error")
        finally:
            session.close()

    @staticmethod
    def query(**kwargs):
        session = DataBaseUtil.Session()
        if 'filter' not in kwargs.keys():
            kwargs['filter'] = True
        if 'order_by' not in kwargs.keys():
            kwargs['order_by'] = (False,)
        rows = session.query(TableTask).filter(kwargs['filter']).order_by(*kwargs['order_by']).all()
        session.close()
        return rows


class TodoList:
    def __init__(self):
        self.util = DataBaseUtil()

    def get_task(self, during: int = 0):
        today = datetime.today()
        query_date = today
        if during == -1:
            index = 1
            order_by = (TableTask.deadline,)
            tasks = self.util.query(order_by=order_by)
            for task in tasks:
                print("{}. {}. {} {}".format(index, task.task, task.deadline.day, task.deadline.strftime('%b')))
                index += 1

            if len(tasks) == 0:
                print("Nothing to do!")
            print()
        else:
            while query_date <= today + timedelta(days=during):
                date_filter = TableTask.deadline == query_date.date()
                order_by = (TableTask.deadline,)
                tasks = self.util.query(filter=date_filter, order_by=order_by)
                if during == 0:
                    print("Today {} {}".format(query_date.date().day, query_date.date().strftime('%b')))
                else:
                    print("{} {} {}".format(query_date.date().strftime("%A"), query_date.date().day, query_date.date().strftime('%b')))

                if len(tasks) == 0:
                    print("Nothing to do!\n")
                else:
                    index = 1
                    for task in tasks:
                        print(f"{index}. {task.task}")
                        index += 1
                    print()
                query_date += timedelta(days=1)

    def add_task(self, kwargs: dict):
        self.util.insert(**kwargs)

    def run(self):
        while True:
            print("""1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete Task\n0) Exit""")
            func_select = input()
            if func_select == '1':
                self.get_task(0)
            if func_select == '2':
                self.get_task(6)  # add 6 days a week
            if func_select == '3':
                print("All tasks:")
                self.get_task(-1)
            elif func_select == '4':
                print()
            elif func_select == '5':
                task = input("Enter task\n")
                deadline = input("Enter deadline\n")
                try:
                    self.add_task({'task': task, 'deadline': datetime.strptime(deadline, '%Y-%m-%d')})
                except ValueError:
                    print(f"time data '{deadline}' does not match format '%Y-%m-%d'")
                print("The task has been added!\n")
            elif func_select == '6':
                num = int(input("Chose the number of the task you want to delete:"))
                self.get_task(-1)


            elif func_select == '0':
                print("Bye!")
                exit()


def init():
    conn_engine = create_engine(f'{DATA_BASE_TYPE}:///{DATA_BASE_PATH}?check_same_thread={CHECK_SAME_THREAD}')
    TableBase.metadata.create_all(conn_engine)
    util = DataBaseUtil(session_engine=sessionmaker(bind=conn_engine))


def main():
    init()
    my_list = TodoList()
    my_list.run()


if __name__ == '__main__':
    main()
