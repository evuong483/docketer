#------------------------------------------------------------------------------
# objects.py
# Author: Erin Vuong
#
# Holds object class definitions used for backend operations
#
# Classes:
#   TimeSlot
#   User
#   SchedulingLink
#------------------------------------------------------------------------------

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Time, Float, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import random, string
import json

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------

DAYS_PER_WEEK = 7.0
MINUTES_PER_HOUR = 60
MINUTES_PER_DAY = 24 * 60.0

DEFAULT_START = datetime.time(hour=9)
DEFAULT_END = datetime.time(hour=17)
WEEKDAYS = [0, 1, 2, 3, 4]

DEFAULT_BEST_HR = datetime.time(hour=10)
DEFAULT_BEST_DAY = 2

DEFAULT_SCALING_FACTOR = 1.2

#------------------------------------------------------------------------------
# TimeSlot
#------------------------------------------------------------------------------
class TimeSlot:

    # start_time and end_time are datetime.datetime objects
    # next_event_start, last_event_start, and best_hour are datetime.time objects
    # best_day is an integer range(7) (0-6 Monday-Sunday)
    # interruption_scaling_factor is a float
    def __init__(self,
                 start_time: datetime.datetime,
                 end_time: datetime.datetime,
                 buffer_time=10):
        assert start_time.date() == end_time.date()
        self._start_time = start_time
        self._end_time = end_time
        self._buffer_time = buffer_time
        yr, mo, day = start_time.year, start_time.month, start_time.day
        self._last_end = datetime.datetime(yr,mo,day,9)
        self._next_start = datetime.datetime(yr,mo,day,17)

    def start_time(self):
        return self._start_time

    def end_time(self):
        return self._end_time

    def get_buffer_time(self):
        return self._buffer_time
    
    def set_last_end(self, last_end):
        self._last_end = last_end
        
    def set_next_start(self, next_start):
        self._next_start = next_start
        
    def get_last_end(self):
        return self._last_end
    
    def get_next_start(self):
        return self._next_start

    def for_json(self):
        vals = { 'start': self._start_time.strftime('%I:%M %p'),
                 'end': self._end_time.strftime('%I:%M %p'),
                 'buffer_time': self._buffer_time,
                 'date': self._start_time.strftime('%Y-%m-%d'),
                 'pretty_date': self._start_time.strftime('%A, %B %d, %Y')}
        return vals

    def _to_minutes(self, time_obj):
        return time_obj.hour * MINUTES_PER_HOUR + time_obj.minute

    def _get_value(self,
                   best_hour,
                   best_day,
                   scaling_factor):
        # distance from optimal day normalized to 1 
        aux = abs(best_day - self._start_time.weekday())
        day_comp = min(aux, abs(aux-7)) / 3

        # distance from optimal hour normalized by 8 hours
        time_comp = \
            self._min_diff(best_hour, self._start_time.time()) \
                / (8 * MINUTES_PER_HOUR)

        # interruption created normalized to less than one and multiplied by
        # scaling factor
        interrupt_comp = min(
                self._min_diff(self._next_start, self._end_time.time()),
                self._min_diff(self._last_end, self._start_time.time())
            ) / (8 * MINUTES_PER_HOUR) * scaling_factor

        return day_comp + time_comp + interrupt_comp

    # takes two datetime.time objects
    def _min_diff(self, time_one, time_two):
        return abs(self._to_minutes(time_one) - self._to_minutes(time_two))

# Sort a list of time slot objects
def sort_slots(time_slots,
               best_hour=DEFAULT_BEST_HR,
               best_day=2,
               scaling_factor=1.2):
    time_slots.sort(key=lambda x: x._get_value(best_hour,
                                               best_day,
                                               scaling_factor))

def generate_url():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

#------------------------------------------------------------------------------
# User
#------------------------------------------------------------------------------

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    name = Column(String)
    refresh_key = Column(String, nullable=False)
    optimal_hour = Column(Time, default=DEFAULT_BEST_HR)
    optimal_day = Column(Integer, default=DEFAULT_BEST_DAY)
    email = Column(String)
    scaling_factor = Column(Float, default=1.2)

    links = relationship('SchedulingLink', back_populates='user',
                cascade='all, delete, delete-orphan')

    def __init__(self,
                 user_id,
                 name,
                 refresh,
                 hour=DEFAULT_BEST_HR,
                 day=DEFAULT_BEST_DAY,
                 email=''):
        super(User, self).__init__(user_id=user_id,
                                   name=name,
                                   refresh_key=refresh,
                                   optimal_hour=hour,
                                   optimal_day=day,
                                   email=email,
                                   scaling_factor=DEFAULT_SCALING_FACTOR)

    def get_user_id(self):
        return self.user_id

    def set_refresh_key(self, new_key):
        self.refresh_key = new_key

    def set_optimal_hour(self, new_hour):
        self.optimal_hour = new_hour

    def set_optimal_day(self, new_day):
        self.optimal_day = new_day

    def get_name(self):
        return self.name

    def get_scaling_factor(self):
        return self.scaling_factor

    def get_refresh_key(self):
        return self.refresh_key

    def get_optimal_hour(self):
        return self.optimal_hour

    def get_optimal_day(self):
        return self.optimal_day

    def get_links(self):
        return self.links

    def get_email(self):
        return self.email

    def for_json(self):
        vals = { 'name': self.name,
                 'optimal_hour': self.optimal_hour.strftime('%H:%M'),
                 'optimal_day': str(self.optimal_day),
                 'email': self.email,
                 'scaling_factor': self.scaling_factor,
                 'links': [link.for_json() for link in self.links] }
        return vals

    def add_scheduling_link(self,
                            half_hours=False,
                            buffer_time=10,
                            workday_start=DEFAULT_START,
                            workday_end=DEFAULT_END,
                            start_scheduling=1,
                            weeks_out=4,
                            weekdays=WEEKDAYS,
                            meeting_length=60):
        link = SchedulingLink(self.user_id,
                              half_hours,
                              buffer_time,
                              workday_start,
                              workday_end,
                              start_scheduling,
                              weeks_out,
                              weekdays,
                              meeting_length)
        self.links.append(link)
        return link

#------------------------------------------------------------------------------
# SchedulingLink
#------------------------------------------------------------------------------

class SchedulingLink(Base):
    __tablename__ = 'urls'

    user_id = Column(String, ForeignKey('users.user_id'))
    target = Column(String, primary_key=True)
    half_hours = Column(Boolean)
    buffer_time = Column(Integer, default=10)
    user = relationship('User', back_populates='links')
    workday_start = Column(Time, default=DEFAULT_START)
    workday_end = Column(Time, default=DEFAULT_END)
    start_scheduling = Column(Integer, default=1)
    weeks_out = Column(Integer, default=4)
    # list of integers joined with ,
    weekdays = Column(String)
    meeting_length = Column(Integer, default=60)

    def __init__(self,
                 user_id,
                 half_hours=False,
                 buffer_time=10,
                 start=DEFAULT_START,
                 end=DEFAULT_END,
                 start_scheduling=1,
                 weeks_out=4,
                 weekdays=WEEKDAYS,
                 meeting_len=60):
        weekday_str = ','.join([str(day) for day in weekdays])
        super(SchedulingLink, self).__init__(user_id=user_id,
                                             half_hours=half_hours,
                                             buffer_time=buffer_time,
                                             workday_start=start,
                                             workday_end=end,
                                             start_scheduling=start_scheduling,
                                             weeks_out=weeks_out,
                                             weekdays=weekday_str,
                                             meeting_length=meeting_len,
                                             target=generate_url())

    def get_target(self):
        return self.target

    def get_half_hours(self):
        return self.half_hours

    def get_buffer_time(self):
        return self.buffer_time

    def get_user_id(self):
        return self.user_id

    def get_user(self):
        return self.user

    def get_workday_start(self):
        return self.workday_start

    def get_workday_end(self):
        return self.workday_end

    def get_start_scheduling(self):
        return self.start_scheduling

    def get_weeks_out(self):
        return self.weeks_out

    def get_weekdays(self):
        return [int(day) for day in self.weekdays.split(',')]

    def get_meeting_length(self):
        return self.meeting_length

    def __str__(self):
        return json.dumps(self.for_json())

    def for_json(self):
        vals = { 'target': self.target,
                 'half_hours': self.half_hours,
                 'workday_start': self.workday_start.strftime('%H:%M'),
                 'workday_end': self.workday_end.strftime('%H:%M'),
                 'buffer_time': self.buffer_time,
                 'start_scheduling': self.start_scheduling,
                 'weekdays': self.weekdays.split(','),
                 'weeks_out': self.weeks_out,
                 'meeting_length': self.meeting_length }
        return vals
