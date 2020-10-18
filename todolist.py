from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

try:
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
except:
    pass
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session_ = sessionmaker(bind=engine)
session = Session_()


def print_task(lst, date=0, mss='Nothing to do!'):
    if len(lst) < 1:
        print(mss)
        return None
    for lst_ in range(len(lst)):
        print('{}. {}'.format(lst_ + 1, lst[lst_]), end='')
        if date:
            print('. {}'.format(lst[lst_].deadline.strftime('%d %b')), end='')
        print()


while True:
    print('1) Today\'s tasks\n2) Week\'s tasks\n3) All tasks', end='')
    opt = input('\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n')
    if opt == '1':
        today = datetime.today()
        print('\nToday {}:'.format(today.strftime('%d %b')))
        print_task(session.query(Table).filter(Table.deadline == today.date()).all())
        print()
    elif opt == '2':
        today = datetime.today()
        for _ in range(7):
            day = today + timedelta(_)
            print('\n{}:'.format(day.strftime('%A %d %b')))
            print_task(session.query(Table).filter(Table.deadline == day.date()).all())
        print()
    elif opt == '3':
        print('\nAll tasks:')
        print_task(session.query(Table).order_by(Table.deadline).all(), 1)
        print()
    elif opt == '4':
        print('\nMissed tasks:')
        day = datetime.today() - timedelta(1)
        rows = session.query(Table).filter(Table.deadline < day).order_by(Table.deadline).all()
        print_task(rows, 1, 'Nothing is missed!')
        print()
    elif opt == '5':
        tsk, dline = input('\nEnter task\n'), input('Enter deadline\n')
        session.add(Table(task=tsk, deadline=datetime.strptime(dline, '%Y-%m-%d')))
        session.commit()
        print('The task has been added!\n')
    elif opt == '6':
        print('\nChoose the number of the task you want to delete:')
        rows = session.query(Table).order_by(Table.deadline).all()
        print_task(rows, 1)
        row = int(input())
        session.delete(rows[row - 1])
        session.commit()
        print('The task has been deleted!\n')
    else:
        print('\nBye!')
        break
