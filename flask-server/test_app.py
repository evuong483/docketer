# !/usr/bin/env python
#-----------------------------------------------------------------------------
# test_app.py
# Author: Erin Vuong
# Test flask server app for frontend testing
#-----------------------------------------------------------------------------

import json
from datetime import datetime
from flask import Flask, request, make_response, render_template, redirect
from flask import url_for, session

#-----------------------------------------------------------------------------

LINKS = [{'target': 'wo24SDFosdle'}, {'target': 'w8sfek39913f'}]

NEW_TARGET = 'os249DFdidl3'

USER_INFO = {'name': 'Erin Vuong',
             'optimal_hour': '10:00',
             'optimal_day': '2',
             'email': 'evuong@gmail.com' }

TIMES = [{'start': '09:00 AM',
          'end': '10:00 AM',
          'buffer_time': 10,
          'date': '2021-03-23',
           'pretty_date': 'Tuesday, March 23, 2021'},
         {'start': '10:00 AM',
          'end': '11:00 AM',
          'buffer_time': 10,
          'date': '2021-03-23',
          'pretty_date': 'Tuesday, March 23, 2021'},
         {'start': '01:00 PM',
          'end': '02:00 PM',
          'buffer_time': 10,
          'date': '2021-03-23',
          'pretty_date': 'Tuesday, March 23, 2021'}]
#-----------------------------------------------------------------------------

def create_app():
    app = Flask(__name__, template_folder='./templates/')
    app.secret_key = b'awoe@)$lsdkw4r23-0'

    @app.route('/login')
    def login():
        session['profile'] = USER_INFO
        session['links'] = LINKS.copy()
        return redirect(url_for('home'))

    @app.route('/logout')
    def logout():
        session.pop('profile')
        return redirect(url_for('home'))

    @app.route('/delete_link', methods=['POST'])
    def delete():
        delete = 0
        new_links = []
        for i in range(len(session['links'])):
            if session['links'][i]['target'] != request.json['target']:
                new_links.append(session['links'][i])
        session['links'] = new_links
        return make_response(json.dumps(''))

    @app.route('/logout_force')
    def logout_force():
        # Clear session stored data
        session.pop('error')
        return redirect(url_for('home'))

    @app.route('/change_hour', methods=['POST'])
    def change_hour():
        # TODO: check what was sent to app
        return make_response(json.dumps(request.json['hour']))

    @app.route('/change_day', methods=['POST'])
    def change_day():
        # TODO: check what was sent to app
        day = request.json['weekday']
        return make_response(json.dumps(day))

    @app.route('/generate_link', methods=['POST'])
    def generate_link():
        # TODO: check what was sent to app
        return make_response(json.dumps(NEW_TARGET))

    @app.route('/delete_link', methods=['POST'])
    def delete_link():
        # TODO: check what was sent to app
        return make_response(json.dumps(''))

    @app.route('/fetch_user', methods=['POST'])
    def fetch_user():
        # TODO: check what was sent to app
        return make_response(json.dumps(USER_INFO))

    @app.route('/schedule_meeting', methods=['POST'])
    def schedule_meeting():
        # TODO: check what was sent to app
        return make_response(json.dumps('Meeting scheduled!'))

    # needed a place to paste copied text to check
    @app.route('/copy_help', methods=['GET'])
    def copy_help():
        return make_response('<input type="text">')

    @app.route('/fetch_times', methods=['POST'])
    def fetch_times():
        # TODO: check what was sent to app
        target = request.json['target']
        if target == 'error':
            return make_response(json.dumps(
            {'error': 'An error ocurred. The host has been notified of the issue. ' +
                      'Please contact them for further information.'}))
        return make_response(json.dumps(TIMES))

    @app.route('/user_info', methods=['POST'])
    def user_info():
        return make_response(json.dumps({**USER_INFO, 'links': session['links']}))

    @app.route('/', methods=['GET'])
    @app.errorhandler(404)
    def home(e=None):
        error = 'T' if 'error' in session else 'F'
        isLoggedIn = 'T' if 'profile' in session else 'F' 
        html = render_template('index.html',
                            title='Docketer',
                            isLoggedIn=isLoggedIn,
                            error=error)
        response = make_response(html)
        return response
    
    return app

#-----------------------------------------------------------------------------
# Run the test app
#-----------------------------------------------------------------------------
from sys import argv, exit, stderr
import logging

PORT = 3000

def main(argv):
  # suppress flask server output
  logger = logging.getLogger('werkzeug')
  handler = logging.FileHandler('server.log')
  logger.addHandler(handler)
  app = create_app()
  app.logger.addHandler(handler)

  app.run(host='0.0.0.0', port=PORT, debug=True)

if __name__ == '__main__':
  main(argv)
