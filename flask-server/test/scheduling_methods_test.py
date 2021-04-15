#-----------------------------------------------------------------------------
# scheduling_methods_tests.py
# 
# Tests for generate_time_slot method in scheduling_methods
#-----------------------------------------------------------------------------

import sys
sys.path.insert(0, '..')

#from objects import *
#from common import *
from datetime import datetime, time, date, timedelta
from scheduling_methods import *

import unittest

class TestSchedulingMethods(unittest.TestCase):

    def assert_dates_equal(self, date_one, date_two):
        self.assertEqual(date_one.year, date_two.year)
        self.assertEqual(date_one.month, date_two.month)
        self.assertEqual(date_one.day, date_two.day)
        self.assertEqual(date_one.hour, date_two.hour)
        self.assertEqual(date_one.minute, date_two.minute)
    
    def test_parse_free_busy(self):
        freebusy = { 'busy': [
                            {'start': '2021-02-17T13:30:00-05:00', 
                             'end': '2021-02-17T14:30:00-05:00'}, 
                            {'start': '2021-02-17T17:00:00-05:00',
                             'end': '2021-02-17T18:00:00-05:00'}, 
                            {'start': '2021-02-18T13:30:00-05:00', 
                             'end': '2021-02-18T14:30:00-05:00'}, 
                            {'start': '2021-02-19T13:30:00-05:00',
                             'end': '2021-02-19T14:30:00-05:00'},
                            {'start': '2021-02-20T13:30:00-05:00',
                             'end': '2021-02-20T14:30:00-05:00'}
                        ]
                    }

        busy_times = parse_free_busy(freebusy)
        self.assertEqual(len(busy_times), 5)
        for time_slot in busy_times:
            self.assertEqual(type(time_slot), TimeSlot)

    def test_merge_slots_with_buffers(self):
        time1_start = datetime(2021,2,17,13,30,0)
        time1_end = datetime(  2021,2,17,14,30,0)
        time2_start = datetime(2021,2,17,15,0,0)
        time2_end = datetime(  2021,2,17,16,0,0)
        time3_start = datetime(2021,2,17,17,0,0)
        time3_end = datetime(  2021,2,17,18,0,0)
        time4_start = datetime(2021,2,18,9,0,0)
        time4_end = datetime(  2021,2,18,10,0,0)
        time5_start = datetime(2021,2,18,10,0,0)
        time5_end = datetime(  2021,2,18,11,0,0)
        time6_start = datetime(2021,2,19,11,0,0)
        time6_end = datetime(  2021,2,19,12,0,0)
        time7_start = datetime(2021,2,19,10,30,0)
        time7_end = datetime(  2021,2,19,13,0,0)
        
        start_times = [time4_start,time1_start,time7_start,time2_start,
                       time3_start,time6_start,time5_start]
        end_times = [time4_end,time1_end,time7_end,time2_end,
                     time3_end,time6_end,time5_end]
        slots = []
        for i in range(7):
            slots.append(TimeSlot(start_times[i],end_times[i],0))
        merged1 = merge_slots_with_buffer(slots, 0)
        merged2 = merge_slots_with_buffer(slots, 15)
        merged3 = merge_slots_with_buffer(slots, 40)
        self.assertEqual(len(merged1), 5)
        self.assertEqual(len(merged2), 4)
        self.assertEqual(len(merged3), 3)
        self.assert_dates_equal(merged1[-1].start_time(),
                               datetime(2021,2,19,10,30,0))
        self.assert_dates_equal(merged1[-1].end_time(),
                               datetime(2021,2,19,13,0,0))
        
    def test_generate_time_slots_emptybusy(self):
        workday_start = time(9,0,0)
        workday_end = time(17,0,0)
        weekdays = {0,2,4}
        all_week = {0,1,2,3,4,5,6}
        
        gen = generate_time_slots(0, workday_start, workday_end, all_week, 
                                   [], 60, num_days=2, min_days_before_scheduling=1)
        self.assertEqual(len(gen), 8)
        
        gen = generate_time_slots(0, workday_start, workday_end, all_week, 
                                   [], 60, num_days=2, min_days_before_scheduling=1)
        self.assertEqual(len(gen), 8)
        
        gen = generate_time_slots(0, workday_start, workday_end, all_week, 
                                   [], 60.1, num_days=2, min_days_before_scheduling=1)
        self.assertEqual(len(gen), 7)
        
        gen = generate_time_slots(0, workday_start, workday_end, all_week, 
                                   [], 60, num_days=2, min_days_before_scheduling=1, 
                                   half_hours=True)
        self.assertEqual(len(gen), 15)
        
        gen = generate_time_slots(0, workday_start, workday_end, weekdays, 
                                   [], 50, num_days=29, min_days_before_scheduling=1)
        self.assertEqual(len(gen), 8*3*4)
        
        gen = generate_time_slots(0, workday_start, workday_end, weekdays, 
                                   [], 50, num_days=29, min_days_before_scheduling=1, half_hours=True)
        self.assertEqual(len(gen), 15*3*4)
        
    def test_generate_time_slots(self):
        workday_start = time(9,0,0)
        workday_end = time(17,0,0)
        weekdays = {0,2,4}
        all_week = {0,1,2,3,4,5,6}
        
        today = datetime(date.today().year, datetime.today().month, datetime.today().day)
        
        time1_start = today + timedelta(days=1,hours=13,minutes=30)
        time1_end = today+ timedelta(days=1,hours=14,minutes=30)
        time2_start = today + timedelta(days=1,hours=15)
        time2_end = today + timedelta(days=1,hours=16)
        time3_start = today + timedelta(days=1,hours=17)
        time3_end = today + timedelta(days=1,hours=18)
        time4_start = today + timedelta(days=2,hours=9)
        time4_end = today + timedelta(days=2,hours=10)
        time5_start = today + timedelta(days=2,hours=10)
        time5_end = today + timedelta(days=2,hours=11)
        time6_start = today + timedelta(days=3,hours=11)
        time6_end = today + timedelta(days=3,hours=12)
        time7_start = today + timedelta(days=3,hours=10,minutes=30)
        time7_end = today + timedelta(days=3,hours=13)
        
        start_times = [time4_start,time1_start,time7_start,time2_start,
                       time3_start,time6_start,time5_start]
        end_times = [time4_end,time1_end,time7_end,time2_end,
                     time3_end,time6_end,time5_end]
        busy_list = []
        for i in range(7):
            busy_list.append(TimeSlot(start_times[i],end_times[i],0))
            
        gen = generate_time_slots(40, workday_start, workday_end, all_week, 
                                  busy_list, 61, num_days=2, 
                                  min_days_before_scheduling=1)
        
        self.assertEqual(len(gen), 3)
        self.assert_dates_equal(gen[0].start_time(), 
                                today + timedelta(days=1, hours=9))
        self.assert_dates_equal(gen[1].start_time(),
                                today + timedelta(days=1, hours=10))
        self.assert_dates_equal(gen[2].start_time(),
                                today + timedelta(days=1, hours=11))
        
        self.assert_dates_equal(gen[0].get_last_end(), 
                                today + timedelta(days=1, hours=9))
        self.assert_dates_equal(gen[0].get_next_start(),
                                today + timedelta(days=1, hours=12, minutes=50))
                
        gen = generate_time_slots(40, workday_start, workday_end, all_week, 
                                  busy_list, 50, num_days=2, 
                                  min_days_before_scheduling=1)
        self.assertEqual(len(gen), 4)
        
        gen = generate_time_slots(15, workday_start, workday_end, all_week, 
                                  busy_list, 20, num_days=3, 
                                  min_days_before_scheduling=2,
                                  half_hours=True)
        self.assertEqual(len(gen), 11)

    def test_slot_generation_with_limited_workday(self):
        workday_start = time(9,0,0)
        workday_end = time(10,0,0)
        
        today = datetime(date.today().year, datetime.today().month, datetime.today().day)

        weekdays = {((today.weekday() + 1) % 7)}
        
        time1_start = today + timedelta(days=1)
        time1_start = time1_start.replace(hour=9)
        time1_end = today + timedelta(days=1)
        time1_end = time1_end.replace(hour=10)
        
        busy_list = [TimeSlot(time1_start, time1_end, 0)]
            
        gen = generate_time_slots(10, workday_start, workday_end, weekdays, 
                                  busy_list, 60, num_days=7*4, 
                                  min_days_before_scheduling=1, half_hours=True)
        
        self.assertEqual(len(gen), 3)

if __name__ == '__main__':
    unittest.main()
