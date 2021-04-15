#------------------------------------------------------------------------------
# scheduling_methods.py
# Author: Erin Vuong
# methods for parsing/creating scheduling
#------------------------------------------------------------------------------
import os

from objects import TimeSlot, sort_slots
from dateutil.parser import parse as dtparse
from datetime import date, datetime, timedelta

# free_busy is a dict in the form of the README dict
def parse_free_busy(free_busy):
    if 'busy' not in free_busy:
        return None

    busy_times = []

    for busy_slot_dict in free_busy['busy']:
        start_time = dtparse(busy_slot_dict['start'], ignoretz=True)
        end_time = dtparse(busy_slot_dict['end'], ignoretz=True)
        busy_times.append(TimeSlot(start_time, end_time, buffer_time=0))

    return busy_times

FOUR_WEEKS = 7 * 4

# TimeSlot(start_time: datetime.datetime,
#                 end_time: datetime.datetime,
#                 buffer_time=10) 

def generate_time_slots(buffer_time,
                        workday_start,
                        workday_end,
                        weekdays,
                        busy_list,
                        meeting_length,
                        num_days=FOUR_WEEKS,
                        min_days_before_scheduling=1,
                        half_hours=False):
    ans = []
    if num_days <= 0 : return ans     
    
    busy_list_merged = merge_slots_with_buffer(busy_list, buffer_time)
    
    # If min_days_before_scheduling == 0, 
    # then work_start depends on the current time
    if min_days_before_scheduling == 0 \
        and date.today().weekday() in weekdays:
        today = datetime.today()
        work_start_datetime = today + timedelta(minutes = 30)
        work_end_datetime = datetime(today.year,
                                     today.month,
                                     today.day,
                                     workday_end.hour,
                                     workday_end.minute,
                                     workday_end.second)
        ans += generate_time_slots_singleday(work_start_datetime,
                                             work_end_datetime,
                                             busy_list_merged,
                                             meeting_length,
                                             half_hours)
    
    init_day = max(min_days_before_scheduling,1)
    
    for i in range(init_day,num_days):
        today = date.today() + timedelta(days = i)
        if today.weekday() not in weekdays: continue
        work_start_datetime = datetime(today.year,
                                       today.month,
                                       today.day,
                                       workday_start.hour,
                                       workday_start.minute,
                                       workday_start.second)
        work_end_datetime = datetime(today.year,
                                     today.month,
                                     today.day,
                                     workday_end.hour,
                                     workday_end.minute,
                                     workday_end.second)
        ans += generate_time_slots_singleday(work_start_datetime,
                                             work_end_datetime,
                                             busy_list_merged,
                                             meeting_length,
                                             half_hours)
    return ans
        
    # for each valid day(today to day n=num_days, or today + num_days days after)

        # starting from max(workday_start, next hour or half hour)
            # generate all time slots (every hour or 1/2 hour, include buffer)

    # repeat to end of busy_list and list
        # while start time of index in list > end time of first slot on busy_list
            # pop front of busy list
        # while end time of index in list > start time of first in busy_list

def merge_slots_with_buffer(timeslot_list,
                            buffer_time):
    # timeslot_list : list of TimeSlot objects
    # buffer_time : int (minutes)
    # return : list of TimeSlot objects
    # extend each TimeSlot in timeslot_list by buffer_time (in both directions),
    # and merge different TimeSlots if they overlap
    if not timeslot_list: return []
    
    # sort by start_time
    timeslot_list = sorted(timeslot_list, key=lambda x: x.start_time())
    
    ans = []
    
    delta = timedelta(minutes = buffer_time)  # timedelta object for buffer_time
    for timeslot in timeslot_list:
        new_slot = TimeSlot(timeslot.start_time()-delta,
                            timeslot.end_time()+delta,
                            0)   # extend timeslot by buffer_time
        if not ans: ans.append(new_slot) 
        
        # skip if new_slot is a subset of ans[-1]
        if ans[-1].end_time().timestamp() \
            >= new_slot.end_time().timestamp(): continue
        
        elif ans[-1].end_time().timestamp() \
            >= new_slot.start_time().timestamp():
            # if ans[-1] overlaps with new_slot, then update ans[-1]
            # buffer counted twice: 
            # if the previous meeting ended at 10:00:00 and next is at 10:20:00,
            # and the buffer = 10, then can't schedule anything in between.
            prev = ans.pop()
            mod_slot = TimeSlot(prev.start_time(),
                                new_slot.end_time(),
                                0)  # modified TimeSlot object
            ans.append(mod_slot)
        else: # non_overlapping case
            ans.append(new_slot)
    
    return ans


def generate_time_slots_singleday(work_start_datetime,
                                  work_end_datetime,
                                  busy_list_merged,
                                  meeting_length,
                                  half_hours=False):
    # single day version
    # work_start_datetime and work_end_datetime : datetime.datetime objects
    # busy_list_merged : busy_list after applying merge_slots_with_buffer
    
    inc = 30*60 if half_hours else 60*60 # meeting start time increment
    
    start_stamp = work_start_datetime.timestamp()  # timestamps
    end_stamp = work_end_datetime.timestamp()
    
    start_stamp = inc * ((start_stamp + inc - 0.01) // inc)  # timestamps rounded
    end_stamp = inc * (end_stamp // inc)
    
    delta = meeting_length * 60  # meeting_length in seconds
    
    ans = []
    blen = len(busy_list_merged)
    ptr = 0 # pointer that will traverse busy_list_merged
    
    while (start_stamp + delta <= end_stamp):
        # move ptr to the correct busy_time, which can potentially cause overlap
        while ptr<blen:
            if busy_list_merged[ptr].end_time().timestamp() \
                >= start_stamp: break
            ptr += 1
        obstacle = None if ptr >= blen else busy_list_merged[ptr]
        prev_obstacle = None if ptr == 0 else busy_list_merged[ptr-1]
        
        if not obstacle \
            or obstacle.start_time().timestamp() >= start_stamp + delta:
                # non_overlapping case
                start = datetime.fromtimestamp(start_stamp)
                end = datetime.fromtimestamp(start_stamp+delta)
                slot = TimeSlot(start, end, 0)
                
                # set last_end and next_start for slot
                # next_start:
                if not obstacle: slot.set_next_start(work_end_datetime)
                else: slot.set_next_start(obstacle.start_time())
                
                # last_end:
                if not prev_obstacle: slot.set_last_end(work_start_datetime)
                else: slot.set_last_end(prev_obstacle.end_time())
                
                ans.append(slot)
        
        # Do nothing when the current timeslot overlaps with obstacle
                
        start_stamp += inc  #increment the start_stamp
    
    return ans

