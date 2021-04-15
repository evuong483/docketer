#-----------------------------------------------------------------------------
# db_tests.py
# 
# Tests for all db related methods
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

    def test_setup(self):
        self.drop_tables()

        # verify they don't exist
        cursor = self.conn.cursor()
        cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables' +
                       ' WHERE table_name=%s)', ('users',))
        self.assertFalse(cursor.fetchone()[0])

        cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables' +
                       ' WHERE table_name=%s)', ('urls',))
        self.assertFalse(cursor.fetchone()[0])

        # create Dorm and check tables exist
        dorm = Dorm(DB_NAME)
        cursor = self.conn.cursor()
        cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables' +
                       ' WHERE table_name=%s)', ('users',))
        self.assertTrue(cursor.fetchone()[0])

        cursor.execute('SELECT EXISTS(SELECT * FROM information_schema.tables' +
                       ' WHERE table_name=%s)', ('urls',))
        self.assertTrue(cursor.fetchone()[0])
        
        # create another dorm and verify no errors are thrown
        new_dorm = Dorm(DB_NAME)

    def test_user_simple(self):
        cursor = self.conn.cursor()
        dorm = Dorm(DB_NAME)

        # verify users table empty
        cursor.execute('SELECT * FROM users')
        self.assertEqual(len(cursor.fetchall()), 0)

        user_id = 'evuong'
        name = 'Erin Vuong'
        refresh_key = 'awoeisld3$#9o'
        optimal_hour = datetime.time(hour=10, minute=30)
        optimal_day = 1
        email = 'evuong@princeton.edu'
        default_scaling_factor = 1.2
        user = User(user_id, name, refresh_key, optimal_hour, optimal_day, email)

        # create user
        dorm.create_user(user)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        self.assertEqual(len(users), 1)
        user_found = users[0]
        self.assertEqual(len(user_found), 7)
        self.assertEqual(user_found[0], user_id)
        self.assertEqual(user_found[1], name)
        self.assertEqual(user_found[2], refresh_key)
        self.assertEqual(user_found[3], optimal_hour)
        self.assertEqual(user_found[4], optimal_day)
        self.assertEqual(user_found[5], email)
        self.assertEqual(user_found[6], default_scaling_factor)

        # get user
        get_user = dorm.get_user(user_id)
        self.assert_users_equal(get_user, user)

        # update refresh key
        refresh_key = 'sd9w3lsdkfsodi'
        dorm.update_refresh_key(user_id, refresh_key)

        # update optimal hour
        optimal_hour = datetime.time(hour=11, minute=30)
        dorm.update_optimal_hour(user_id, optimal_hour)

        # update optimal day
        optimal_day = 2
        dorm.update_optimal_day(user_id, optimal_day)

        # check info updated
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        self.assertEqual(len(users), 1)
        user_found = users[0]
        self.assertEqual(len(user_found), 7)
        self.assertEqual(user_found[0], user_id)
        self.assertEqual(user_found[1], name)
        self.assertEqual(user_found[2], refresh_key)
        self.assertEqual(user_found[3], optimal_hour)
        self.assertEqual(user_found[4], optimal_day)
        self.assertEqual(user_found[5], email)
        self.assertEqual(user_found[6], default_scaling_factor)

        # get user
        user = User(user_id, name, refresh_key, optimal_hour, optimal_day, email)
        get_user = dorm.get_user(user_id)
        self.assert_users_equal(get_user, user)

        # delete user
        dorm.delete_user(user_id)

        # verify users table empty
        cursor.execute('SELECT * FROM users')
        self.assertEqual(len(cursor.fetchall()), 0)

        # try getting a nonexistent user
        no_user = dorm.get_user(user_id)
        self.assertEqual(no_user, None)

        # try deleting a nonexistent user
        dorm.delete_user(user_id)

    def test_delete_user_and_links(self):
        cursor = self.conn.cursor()
        dorm = Dorm(DB_NAME)

        user_id = 'evuong'
        name = 'Erin Vuong'
        refresh_key = 'awoeisld3$#9o'
        optimal_hour = datetime.time(hour=10, minute=30)
        optimal_day = 1
        email = 'evuong@princeton.edu'
        default_scaling_factor = 1.2
        user = User(user_id, name, refresh_key, optimal_hour, optimal_day, email)

        # create user
        dorm.create_user(user)

        # create a few link
        dorm.add_scheduling_link(user_id)
        dorm.add_scheduling_link(user_id)

        # delete user
        dorm.delete_user(user_id)

        # verify users table empty
        cursor.execute('SELECT * FROM users')
        self.assertEqual(len(cursor.fetchall()), 0)

if __name__ == '__main__':
    unittest.main()
