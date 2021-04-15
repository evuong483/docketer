#-----------------------------------------------------------------------------
# flask_tests.py
# 
# Tests for test-able paths in Flask (see README for untestable)
#-----------------------------------------------------------------------------
import sys
sys.path.insert(0, '..')

from flask_testing import TestCase
import flask
from app import app
from database_methods import Dorm
from urllib.parse import urlparse, urljoin
import json
from objects import User

import unittest

class TestBase(TestCase):
    
    user_id = 'test_user'
    name = 'Test User'
    refresh = 'test_refresh'
    user = User(user_id, name, refresh)

    def setUp(self):
        # set up test user in db
        db = Dorm()
        db.delete_user(self.user_id)
        db.create_user(User(self.user_id, self.name, self.refresh))

    def tearDown(self):
        # delete test user
        db = Dorm()
        db.delete_user(self.user_id)

    def create_app(self):
        return app

    def assertRedirectsRegex(self, response, location, message=None):
        parts = urlparse(location)

        if parts.netloc:
            expected_location = location
        else:
            server_name = self.app.config.get('SERVER_NAME') or 'localhost'
            expected_location = urljoin('http://%s' % server_name, location)

        valid_status_codes = (301, 302, 303, 305, 307)
        valid_status_code_str = ', '.join(str(code) for code in valid_status_codes)
        not_redirect = 'HTTP Status %s expected but got %d' % (valid_status_code_str, response.status_code)
        self.assertTrue(response.status_code in valid_status_codes, message or not_redirect)
        self.assertRegex(response.location, expected_location)

class TestLoginLogout(TestBase):

    def test_login(self):
        response = self.client.get('/login')
        url = ('https://rank-scheduling.us.auth0.com/authorize\?'
               'response_type=code&client_id=[a-zA-Z0-9]*&'
               'redirect_uri=http%3A%2F%2Flocalhost%2Fcallback&scope=openid\+'
               'profile\+email&state=[a-zA-Z0-9]*&'
               'connection_scope=https%3A%2F%2Fwww\.googleapis\.com%2Fauth%2F'
               'calendar\.readonly%2C\+https%3A%2F%2Fwww\.googleapis\.com%2Fauth%2F'
               'calendar\.events&access_type=offline&nonce=[a-zA-Z0-9]*')
        self.assertRedirectsRegex(response, url)

    def test_login_force(self):
        response = self.client.get('/login_force')
        url = ('https://rank-scheduling.us.auth0.com/authorize\?'
               'response_type=code&client_id=[a-zA-Z0-9]*&'
               'redirect_uri=http%3A%2F%2Flocalhost%2Fcallback&scope=openid\+'
               'profile\+email&state=[a-zA-Z0-9]*&'
               'connection_scope=https%3A%2F%2Fwww\.googleapis\.com%2Fauth%2F'
               'calendar\.readonly%2C\+https%3A%2F%2Fwww\.googleapis\.com%2Fauth%2F'
               'calendar\.events&access_type=offline&approval_prompt=force&'
               'nonce=[a-zA-Z0-9]*')
        self.assertRedirectsRegex(response, url)

    def test_logout(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = 'Profile here'
                session['jwt_payload'] = 'More info here'
                session['error'] = 'Error here'

            response = self.client.get('/logout')
            self.assertTrue('profile' not in flask.session)
            self.assertTrue('jwt_payload' not in flask.session)
            self.assertTrue('error' not in flask.session)

            url = ('https://rank-scheduling\.us\.auth0\.com/v2/logout\?'
                   'returnTo=http%3A%2F%2Flocalhost%2F&client_id=[a-zA-Z0-9]*')
            self.assertRedirectsRegex(response, url)

    def test_logout_force(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = 'Profile here'
                session['jwt_payload'] = 'More info here'
                session['error'] = 'Error here'

            response = self.client.get('/logout_force')
            self.assertTrue('profile' not in flask.session)
            self.assertTrue('jwt_payload' not in flask.session)
            self.assertTrue('error' not in flask.session)

            url = ('https://rank-scheduling\.us\.auth0\.com/v2/logout\?'
                   'returnTo=http%3A%2F%2Flocalhost%2Flogin_force\&'
                   'client_id=[a-zA-Z0-9]*')
            self.assertRedirectsRegex(response, url)

class TestHostRoutes(TestBase):

    def test_change_hour(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            hour = '09:00'
            response = c.post('/change_hour', json={'hour': hour})
            self.assertEqual(json.loads(response.data), hour)

    def test_change_day(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            day = '1'
            response = c.post('/change_day', json={'weekday': day})
            self.assertEqual(json.loads(response.data), day)

    def test_user_info(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            response = c.post('/user_info')
            data = json.loads(response.data)
            self.assertEqual(data['name'], self.name)
            self.assertEqual(data['optimal_hour'], '10:00')
            self.assertEqual(data['optimal_day'], '2')
            self.assertEqual(data['email'], '')
            self.assertEqual(data['scaling_factor'], 1.2)
            self.assertEqual(data['links'], [])

class TestLinkRoutes(TestBase):

    def test_gen_link(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            meeting_len = '50'
            buffer = '10'
            start = '12:00'
            end = '16:00'
            days_out = '1'
            weeks_out = '1'
            half_hours = False
            weekdays = [1, 2, 3] # Tues, Wed, Thurs
            response = c.post('/generate_link',
                              json={'meeting_len': meeting_len,
                                    'buffer': buffer,
                                    'workday_start': start,
                                    'workday_end': end,
                                    'days_out': days_out,
                                    'weeks_out': weeks_out,
                                    'weekdays': weekdays,
                                    'half_hours': half_hours})

            target = json.loads(response.data)
            self.assertRegex(target, '[a-zA-Z0-9]{16}')

            db = Dorm()
            links = db.get_user(self.user_id).get_links()
            self.assertEqual(len(links), 1)
            self.assertEqual(links[0].get_target(), target)

    def test_delete_link(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            # add a link
            db = Dorm()
            db.add_scheduling_link(self.user_id)

            links = db.get_user(self.user_id).get_links()
            self.assertEqual(len(links), 1)

            response = c.post('/delete_link', json={'target': links[0].get_target()})
            self.assertEqual(json.loads(response.data), '')

            links = db.get_user(self.user_id).get_links()
            self.assertEqual(len(links), 0)

    def test_fetch_user(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            # add a link
            db = Dorm()
            db.add_scheduling_link(self.user_id)

            links = db.get_user(self.user_id).get_links()
            target = links[0].get_target()

            response = c.post('/fetch_user', json={'target': target})
            data = json.loads(response.data)
            self.assertEqual(data['name'], self.name)

    def test_fetch_user_error(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            response = c.post('/fetch_user', json={'target': 'not_a_target'})
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'No scheduling link found.')

    def test_schedule_meeting(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            # add a link
            db = Dorm()
            db.add_scheduling_link(self.user_id)

            links = db.get_user(self.user_id).get_links()
            target = links[0].get_target()

            response = c.post('/schedule_meeting', json={'target': target})
            self.assertEqual(json.loads(response.data), 'Meeting scheduled!')

    def test_fetch_times(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            # add a link
            meeting_len = '50'
            buffer = '10'
            start = '14:00'
            end = '16:00'
            days_out = '1'
            weeks_out = '1'
            half_hours = False
            weekdays = [1, 2] # Tues, Wed, Thurs
            response = c.post('/generate_link',
                              json={'meeting_len': meeting_len,
                                    'buffer': buffer,
                                    'workday_start': start,
                                    'workday_end': end,
                                    'days_out': days_out,
                                    'weeks_out': weeks_out,
                                    'weekdays': weekdays,
                                    'half_hours': half_hours})

            target = json.loads(response.data)
            self.assertRegex(target, '[a-zA-Z0-9]{16}')

            response = c.post('/fetch_times', json={'target': target})
            data = json.loads(response.data)

            self.assertTrue(len(data) <= 4) # maximum possible length

            # check data format
            for slot in data:
                self.assertTrue('start' in slot)
                self.assertTrue('end' in slot)
                self.assertTrue('buffer_time' in slot)
                self.assertTrue('date' in slot)
                self.assertTrue('pretty_date' in slot)

    def test_fetch_times_error(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['profile'] = {'user_id': self.user_id}

            response = c.post('/fetch_times', json={'target': 'not_a_target'})
            data = json.loads(response.data)

            msg = ('This scheduling link is not available! Please contact '
                   'the intended host for a working link.')
            self.assertEqual(data['error'], msg)

if __name__ == '__main__':
    unittest.main()