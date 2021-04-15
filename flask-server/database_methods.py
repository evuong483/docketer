#------------------------------------------------------------------------------
# database_methods.py
# Author: Erin Vuong
# Methods for connecting to the postgres database
#------------------------------------------------------------------------------

from os import environ
from objects import User, SchedulingLink, Base
from objects import DEFAULT_START, DEFAULT_END, WEEKDAYS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

PWD = 'test'
DB_NAME = 'cal_db'

DATABASE_URL = environ.get('DATABASE_URL')
if not DATABASE_URL or DATABASE_URL is '127.0.0.1':
    DATABASE_URL = 'postgresql+psycopg2://postgres:{}@localhost:5432/{}'.\
                                format(PWD,'{}')

class Dorm():
    def __init__(self, db_name=DB_NAME):
        self.engine = create_engine(DATABASE_URL.format(db_name))

        # create all tables needed if not already created
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(expire_on_commit=False)
        self.Session.configure(bind=self.engine)

    def create_user(self, user):
        session = self.Session()
        session.add(user)
        session.commit()

    def get_user(self, user_id):
        try:
            session = self.Session()
            user = session.query(User).filter(User.user_id==user_id).one()
            session.commit()
            return user
        except NoResultFound:
            return None

    def update_refresh_key(self, user_id, new_key):
        try:
            session = self.Session()
            user = session.query(User).filter(User.user_id==user_id).one()
            user.set_refresh_key(new_key)
            session.commit()
        except NoResultFound:
            return None

    def update_optimal_hour(self, user_id, new_hour):
        try:
            session = self.Session()
            user = session.query(User).filter(User.user_id==user_id).one()
            user.set_optimal_hour(new_hour)
            session.commit()
        except NoResultFound:
            return None

    def update_optimal_day(self, user_id, new_day):
        try:
            session = self.Session()
            user = session.query(User).filter(User.user_id==user_id).one()
            user.set_optimal_day(new_day)
            session.commit()
        except NoResultFound:
            return None

    def delete_user(self, user_id):
        session = self.Session()
        session.query(SchedulingLink)\
            .filter(SchedulingLink.user_id==user_id).delete()
        session.query(User).filter(User.user_id==user_id).delete()
        session.commit()

    def add_scheduling_link(self,
                            user_id,
                            half_hours=False,
                            buffer_time=10,
                            workday_start=DEFAULT_START,
                            workday_end=DEFAULT_END,
                            start_scheduling=1,
                            weeks_out=4,
                            weekdays=WEEKDAYS,
                            meeting_length=60):
        try:
            session = self.Session()
            user = session.query(User).filter(User.user_id==user_id).one()
            link = user.add_scheduling_link(half_hours,
                                            buffer_time,
                                            workday_start,
                                            workday_end,
                                            start_scheduling,
                                            weeks_out,
                                            weekdays,
                                            meeting_length)
            session.add(link)
            session.commit()
            return link
        except NoResultFound:
            return None
        
    def fetch_scheduling_link(self, target):
        try:
            session = self.Session()
            user = session.query(User)\
                        .filter(SchedulingLink.user_id==User.user_id)\
                        .filter(SchedulingLink.target==target).one()
            link = session.query(SchedulingLink)\
                        .filter(SchedulingLink.target==target).one()
            session.commit()
            return user, link
        except NoResultFound:
            return None, None

    def delete_scheduling_link(self, target):
        session = self.Session()
        session.query(SchedulingLink)\
                    .filter(SchedulingLink.target==target).delete()
        session.commit()