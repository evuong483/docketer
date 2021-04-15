#-----------------------------------------------------------------------------
# object_tests.py
# 
# Tests for all objects and methods
#-----------------------------------------------------------------------------
import sys
sys.path.insert(0, '..')

from objects import *
from datetime import datetime, time, date

import unittest

class TestUser(unittest.TestCase):

    def test_simple_user(self):
        user_id = 'evuong'
        name = 'Erin Vuong'
        refresh_key = 'awoeisld3$#9o'
        optimal_hour = time(hour=10, minute=30)
        optimal_day = 1
        email = 'evuong@princeton.edu'
        default_scaling_factor = 1.2
        user = User(user_id, name, refresh_key, optimal_hour, optimal_day, email)

        self.assertEqual(user.get_user_id(), user_id)
        self.assertEqual(user.get_name(), name)
        self.assertEqual(user.get_refresh_key(), refresh_key)
        self.assertEqual(user.get_optimal_hour(), optimal_hour)
        self.assertEqual(user.get_optimal_day(), optimal_day)
        self.assertEqual(user.get_email(), email)
        self.assertEqual(len(user.get_links()), 0) 
        self.assertEqual(user.get_scaling_factor(), default_scaling_factor)
        
        # test for_json
        vals = { 'name': 'Erin Vuong',
                 'optimal_hour': '10:30',
                 'optimal_day': '1',
                 'email': 'evuong@princeton.edu',
                 'scaling_factor': 1.2,
                 'links': [] }
        self.assertEqual(user.for_json(), vals)


class TestSchedulingLink(unittest.TestCase):
    
    def test_simple_scheduling_link(self):
        user_id = 'evuong'

        # all defaults
        link = SchedulingLink(user_id)
        self.assertEqual(link.get_user_id(), user_id)
        self.assertEqual(len(link.get_target()), 16)
        self.assertEqual(link.get_workday_start(), time(9))
        self.assertEqual(link.get_workday_end(), time(17))
        self.assertEqual(link.get_weeks_out(), 4)
        self.assertEqual(link.get_start_scheduling(), 1)
        self.assertEqual(link.get_meeting_length(), 60)
        self.assertEqual(link.get_weekdays(), [0,1,2,3,4])
        self.assertEqual(link.get_user(), None)
        self.assertEqual(link.get_buffer_time(), 10)
        self.assertEqual(link.get_half_hours(), False)
        

    def test_add_scheduling_link(self):
        user_id = 'evuong'
        name = 'Erin Vuong'
        refresh_key = 'awoeisld3$#9o'
        optimal_hour = time(hour=10, minute=30)
        optimal_day = 1
        email = 'evuong@princeton.edu'
        user = User(user_id, name, refresh_key, optimal_hour, optimal_day, email)

        links = user.get_links()
        self.assertEqual(len(links), 0)

        # generate a new scheduling link
        link = user.add_scheduling_link()
        self.assertEqual(type(link), SchedulingLink)
        self.assertEqual(link.get_user_id(), user_id)
        self.assertEqual(len(link.get_target()), 16)
        self.assertEqual(link.get_workday_start(), time(9))
        self.assertEqual(link.get_workday_end(), time(17))
        self.assertEqual(link.get_weeks_out(), 4)
        self.assertEqual(link.get_start_scheduling(), 1)
        self.assertEqual(link.get_meeting_length(), 60)
        self.assertEqual(link.get_weekdays(), [0,1,2,3,4])
        self.assertEqual(link.get_buffer_time(), 10)
        self.assertEqual(link.get_half_hours(), False)

        # check links
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], link)

        # check link user
        link_user = link.get_user()
        self.assertEqual(link_user, user)
        
        # check for_json
        target = link.get_target()
        vals = { 'target': target,
                 'half_hours': False,
                 'workday_start': '09:00',
                 'workday_end': '17:00',
                 'buffer_time': 10,
                 'start_scheduling': 1,
                 'weekdays': ['0','1','2','3','4'],
                 'weeks_out': 4,
                 'meeting_length': 60 }
        self.assertEqual(link.for_json(), vals)
        
        # check for_json for the (updated) user
        vals_user = { 'name': 'Erin Vuong',
                 'optimal_hour': '10:30',
                 'optimal_day': '1',
                 'email': 'evuong@princeton.edu',
                 'scaling_factor': 1.2,
                 'links': [vals] }
        self.assertEqual(user.for_json(), vals_user)


class TestUrlGenerate(unittest.TestCase):

    def test_generate_url(self):
        tag = generate_url()
        self.assertEqual(len(tag), 16)

        tag2 = generate_url()
        self.assertEqual(len(tag2), 16)
        self.assertFalse(tag == tag2)

class TestTimeSlots(unittest.TestCase):

    def assert_dates_equal(self, date_one, date_two):
        self.assertEqual(date_one.year, date_two.year)
        self.assertEqual(date_one.month, date_two.month)
        self.assertEqual(date_one.day, date_two.day)
        self.assertEqual(date_one.hour, date_two.hour)
        self.assertEqual(date_one.minute, date_two.minute)

    def make_time_slot(self,
                       start_h,
                       start_m,
                       end_h,
                       end_m,
                       year=2021,
                       month=2,
                       day=16):
        start = datetime(year, month, day, hour=start_h, minute=start_m)
        end = datetime(year, month, day, hour=end_h, minute=end_m)
        return start, end, TimeSlot(start, end)

    def test_init(self):
        # no other events - using defaults
        start, end, time_slot = self.make_time_slot(13, 30, 14, 30)
        self.assert_dates_equal(start, time_slot.start_time())
        self.assert_dates_equal(end, time_slot.end_time())
        self.assertEqual(time_slot.get_buffer_time(), 10)
    
    def test_rank_two_simple_time_only(self):
        start1, end1, time_slot = self.make_time_slot(10, 0, 11, 0)
        start2, end2, time_slot_2 = self.make_time_slot(13, 30, 14, 30)
        slots = [time_slot, time_slot_2]

        # preferred hour 10
        sort_slots(slots)

        # first slot more preferred
        self.assert_dates_equal(start1, slots[0].start_time())
        self.assert_dates_equal(end1, slots[0].end_time()) 

    def test_rank_two_simple_day_only(self):
        start1, end1, time_slot = self.make_time_slot(10, 0, 11, 0, day=16)
        start2, end2, time_slot_2 = self.make_time_slot(10, 0, 11, 00, day=19)
        slots = [time_slot, time_slot_2]
        
        # preferred day 2 = Wednesday, 16 is Tues and 19 is Fri
        sort_slots(slots)

        # first slot more preferred
        self.assert_dates_equal(start1, slots[0].start_time())
        self.assert_dates_equal(end1, slots[0].end_time()) 

    def test_rank_two_simple_interruption_only(self):
        # prefer minimal interruptions
        start1, end1, time_slot = self.make_time_slot(10, 0, 11, 0)
        start2, end2, time_slot_2 = self.make_time_slot(10, 0, 11, 00)
        slots = [time_slot, time_slot_2]

        # next only
        next_start = time(14)
        time_slot.set_next_start(datetime(2021,2,16,14))
        time_slot_2.set_next_start(datetime(2021,2,16,14))
        self.assert_dates_equal(time_slot.get_next_start(), datetime(2021,2,16,14))
        self.assert_dates_equal(time_slot.get_last_end(), datetime(2021,2,16,9))
        sort_slots(slots)

        # first slot more preferred
        self.assert_dates_equal(start1, slots[0].start_time())
        self.assert_dates_equal(end1, slots[0].end_time()) 

        # last only
        time_slot.set_last_end(datetime(2021,2,16,9,30))
        time_slot_2.set_next_start(datetime(2021,2,16,9,30))
        time_slot.set_next_start(datetime(2021,2,16,17))
        time_slot_2.set_next_start(datetime(2021,2,16,17))
        self.assert_dates_equal(time_slot.get_last_end(), datetime(2021,2,16,9,30))
        sort_slots(slots)

        # first slot more preferred
        self.assert_dates_equal(start1, slots[0].start_time())
        self.assert_dates_equal(end1, slots[0].end_time()) 

        # next and last
        time_slot.set_next_start(datetime(2021,2,16,14))
        time_slot_2.set_next_start(datetime(2021,2,16,14))

        # start and last
        sort_slots(slots)

        # first slot more preferred
        self.assert_dates_equal(start1, slots[0].start_time())
        self.assert_dates_equal(end1, slots[0].end_time()) 
        
    def test_for_json(self):
        start, end, time_slot = self.make_time_slot(13, 30, 14, 30)
        vals = { 'start': '01:30 PM',
                 'end': '02:30 PM',
                 'buffer_time': 10,
                 'date': '2021-02-16',
                 'pretty_date': 'Tuesday, February 16, 2021'}
        self.assertEqual(time_slot.for_json(), vals)
  

if __name__ == '__main__':
    unittest.main()
