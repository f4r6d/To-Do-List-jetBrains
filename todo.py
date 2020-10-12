from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today()


while True:
    print('1) Today\'s tasks')
    print('2) Week\'s tasks')
    print('3) All tasks')
    print('4) Missed tasks')
    print('5) Add task')
    print('6) Delete task')
    print('0) Exit')
    option = int(input())

    if option == 1:
        print()
        print(f'Today {today.day} {today.strftime("%b")}:')
        today_rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if len(today_rows) == 0:
            print('Nothing to do!')
        else:
            for row in today_rows:
                print(f'{row.id}. {row.task}')
        print()

    elif option == 2:

        for i in range(7):

            selected_day = today + timedelta(days=i)
            print()
            print(f'{selected_day.strftime("%A")} {selected_day.day} {selected_day.strftime("%b")}:')
            week_rows = session.query(Table).filter(Table.deadline == selected_day.date()).all()
            if len(week_rows) == 0:
                print('Nothing to do!')
            else:
                for row in week_rows:
                    print(f'{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
            print()

    elif option == 3:
        print()
        print('All tasks:')
        all_rows = session.query(Table).order_by(Table.deadline).all()
        if len(all_rows) == 0:
            print('Nothing to do!')
        else:
            for row in all_rows:
                print(f'{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
        print()

    elif option == 4:
        print()
        print('Missed tasks:')
        all_rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
        if len(all_rows) == 0:
            print('Nothing is missed!')
        else:
            for row in all_rows:
                print(f'{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
        print()

    elif option == 5:
        print()
        new_task = input('Enter task\n')
        new_task_deadline = input('Enter deadline\n')
        new_row = Table(task=new_task,
                 deadline=datetime.strptime(new_task_deadline, '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print('The task has been added!')
        print()

    elif option == 6:
        print()
        print('Choose the number of the task you want to delete:')
        all_rows = session.query(Table).order_by(Table.deadline).all()
        if len(all_rows) == 0:
            print('Nothing to delete!')
        else:
            for row in all_rows:
                print(f'{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
            del_row_id = int(input()) - 1
            del_row = all_rows[del_row_id]
            session.delete(del_row)
            session.commit()
            print('The task has been deleted!')
        print()

    elif option == 0:
        break


