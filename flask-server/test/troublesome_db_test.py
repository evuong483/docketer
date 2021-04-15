#-----------------------------------------------------------------------------
# troublesome_db_test.py
# 
# Test that was causing hanging
#-----------------------------------------------------------------------------

import sys
sys.path.insert(0, '..')

from objects import User, SchedulingLink
from database_methods import Dorm, PWD
from psycopg2 import connect
import datetime
import time

import unittest
DB_NAME = 'cal_db_test'

class TestDorm(unittest.TestCase):

    def drop_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS urls')
        cursor.execute('DROP TABLE IF EXISTS users')
        self.conn.commit()

    def clean_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM urls')
        cursor.execute('DELETE FROM users')
        self.conn.commit()

    def setUp(self):
        self.conn = connect(database=DB_NAME, user='postgres', password=PWD,
                        host='127.0.0.1', port='5432')
        self.clean_tables()

    def tearDown(self):
        self.clean_tables()
        self.conn.close()

    def assert_users_equal(self, user1, user2):
        self.assertEqual(user1.get_user_id(), user2.get_user_id())
        self.assertEqual(user1.get_name(), user2.get_name())
        self.assertEqual(user1.get_refresh_key(), user2.get_refresh_key())
        self.assertEqual(user1.get_optimal_hour(), user2.get_optimal_hour())
        self.assertEqual(user1.get_optimal_day(), user2.get_optimal_day())
        self.assertEqual(user1.get_email(), user2.get_email())
        self.assertEqual(user1.get_scaling_factor(), user2.get_scaling_factor())

    # Warning: running all tests in same file caused tests to hang?
    def test_scheduling_link_simple(self):
        cursor = self.conn.cursor()
        dorm = Dorm(DB_NAME)

        # have to add scheduling link to user
        user_id = 'evuong'
        name = 'Erin Vuong'
        refresh_key = 'awoeisld3$#9o'
        optimal_hour = datetime.time(hour=10, minute=30)
        optimal_day = 1
        email = 'evuong@princeton.edu'
        user = User(user_id, name, refresh_key, optimal_hour, optimal_day, email)

        # create user
        dorm.create_user(user)

        # add another user (cover fetching link from db with multiple users)
        user_id2 = 'sdfoiLESAFK'
        user2 = User(user_id2, name, refresh_key, optimal_hour, optimal_day, email)
        dorm.create_user(user2)
        
        # verify urls table empty
        cursor.execute('SELECT * FROM urls')
        self.assertEqual(len(cursor.fetchall()), 0)

        # add two links
        link1 = dorm.add_scheduling_link(user_id)
        link2 = dorm.add_scheduling_link(user_id, True, 15)
        self.assertEqual(link1.get_user_id(), user_id)
        self.assertEqual(link1.get_half_hours(), False)
        self.assertEqual(link1.get_buffer_time(), 10)
        self.assertEqual(len(link1.get_target()), 16)
        self.assertEqual(link2.get_user_id(), user_id)
        self.assertEqual(link2.get_half_hours(), True)
        self.assertEqual(link2.get_buffer_time(), 15)
        self.assertEqual(len(link2.get_target()), 16)

        # check they are there
        cursor.execute('SELECT * FROM urls')
        links = cursor.fetchall()
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0][0], user_id)
        self.assertEqual(len(links[0][1]), 16)
        self.assertEqual(links[1][0], user_id)
        self.assertEqual(len(links[1][1]), 16)

        # get the links
        link_user, lin1_found = dorm.fetch_scheduling_link(link1.get_target())
        self.assert_users_equal(link_user, user)

        link2_user, link2_found = dorm.fetch_scheduling_link(link2.get_target())
        self.assert_users_equal(link2_user, user)

        # remove the links
        dorm.delete_scheduling_link(link1.get_target())
        dorm.delete_scheduling_link(link2.get_target())

        # verify urls table empty
        cursor.execute('SELECT * FROM urls')
        self.assertEqual(len(cursor.fetchall()), 0)

        # get link that's not there
        self.assertEqual(dorm.fetch_scheduling_link('Not a target'), (None, None))

        # delete a link that's not there
        dorm.delete_scheduling_link('Not a target')

        # verify urls table empty
        cursor.execute('SELECT * FROM urls')
        self.conn.commit()
        self.assertEqual(len(cursor.fetchall()), 0)
        self.conn.commit()

if __name__ == '__main__':
    unittest.main()