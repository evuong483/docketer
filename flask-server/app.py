#!/usr/bin/env python
#-----------------------------------------------------------------------------
# app.py
# Author: Erin Vuong
# Base app for calendar react application
#-----------------------------------------------------------------------------
import time
import json
from os import environ as env
from database_methods import Dorm
from objects import User, sort_slots
import os
from werkzeug.exceptions import HTTPException
import http.client
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from datetime import datetime
from auth_methods import get_refresh_token
from email_methods import send_guest_email, send_host_email, send_host_refresh_email

import google.oauth2.credentials
import google_auth_oauthlib.flow

from calendar_methods import get_freebusy, add_event, get_avail

from scheduling_methods import parse_free_busy, generate_time_slots

from dotenv import load_dotenv, find_dotenv

from flask import Flask, request, make_response, render_template, redirect
from flask import url_for, jsonify, session

#-----------------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates/')
app.secret_key = b'YOUR_SECRET_KEY_HERE'
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='YOUR_CLIENT_ID_HERE',
    client_secret='YOUR_CLIENT_SECRET_HERE',
    api_base_url='https://rank-scheduling.us.auth0.com',
    access_token_url='https://rank-scheduling.us.auth0.com/oauth/token',
    authorize_url='https://rank-scheduling.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

#-----------------------------------------------------------------------------

@app.route('/login')
def login():
    connection_scope='https://www.googleapis.com/auth/calendar.readonly, ' + \
        'https://www.googleapis.com/auth/calendar.events'
    return auth0.authorize_redirect(
        redirect_uri=url_for('callback_handling', _external=True),
        connection_scope=connection_scope,
        access_type='offline')

@app.route('/login_force')
def login_force():
    connection_scope='https://www.googleapis.com/auth/calendar.readonly, ' + \
        'https://www.googleapis.com/auth/calendar.events'
    return auth0.authorize_redirect(
        redirect_uri=url_for('callback_handling', _external=True),
        connection_scope=connection_scope,
        access_type='offline',
        approval_prompt='force')

@app.route('/logout')
def logout():
    # Clear session stored data
    session.pop('profile')
    if 'jwt_payload' in session:
        session.pop('jwt_payload')
    if 'error' in session:
        session.pop('error')
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True),
              'client_id': 'YOUR_CLIENT_ID_HERE'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/logout_force')
def logout_force():
    # Clear session stored data
    session.pop('profile')
    session.pop('error')
    session.pop('jwt_payload')
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('login_force', _external=True),
              'client_id': 'YOUR_CLIENT_ID_HERE'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


# callback for Auth0 login (not tested in flask tests)
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session (used for checking login)
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    # check if user in db
    db = Dorm()
    user = db.get_user(userinfo['sub'])
    refresh_key = ''
    if not user:
        # get refresh key
        refresh_key = get_refresh_token(userinfo['sub'])
        user = User(userinfo['sub'],
                    userinfo['name'],
                    refresh_key,
                    email=userinfo['email'])
        db.create_user(user)
    else:
        refresh_key = get_refresh_token(userinfo['sub'], True)
        # update refresh key
        if refresh_key:
            db.update_refresh_key(userinfo['sub'], refresh_key)

        # check refresh key validity and force refresh if not valid
        else:
            success = True
            try:
                refresh_key = db.get_user(userinfo['sub']).get_refresh_key()
                success = get_avail(refresh_key)
            except:
                success = False
            if not success:
                session['error'] = 'refresh_key_error'
            
    return redirect(url_for('home'))

@app.route('/change_hour', methods=['POST'])
def change_hour():
    hour = datetime.strptime(request.json['hour'], '%H:%M').time()
    db = Dorm()
    db.update_optimal_hour(session['profile']['user_id'], hour)
    return make_response(json.dumps(request.json['hour']))

@app.route('/change_day', methods=['POST'])
def change_day():
    # updating day
    day = request.json['weekday']
    db = Dorm()
    db.update_optimal_day(session['profile']['user_id'], day)
    return make_response(json.dumps(day))

@app.route('/generate_link', methods=['POST'])
def generate_link():
    # necessary info from json request
    info = request.json
    meeting_len = int(info['meeting_len'])
    buffer = int(info['buffer'])
    workday_start = datetime.strptime(info['workday_start'], '%H:%M').time()
    workday_end = datetime.strptime(info['workday_end'], '%H:%M').time()
    days_out = int(info['days_out'])
    weeks_out = int(info['weeks_out'])
    weekdays = info['weekdays']
    half_hours = info['half_hours']

    # create db and create link
    db = Dorm()
    target = db.add_scheduling_link(session['profile']['user_id'],
                                    half_hours=half_hours,
                                    buffer_time=buffer,
                                    workday_start=workday_start,
                                    workday_end=workday_end,
                                    start_scheduling=days_out,
                                    weeks_out=weeks_out,
                                    weekdays=weekdays,
                                    meeting_length=meeting_len)

    # updating day
    return make_response(json.dumps(target.get_target()))

@app.route('/delete_link', methods=['POST'])
def delete_link():
    db = Dorm()
    db.delete_scheduling_link(request.json['target'])
    return make_response(json.dumps(''))

@app.route('/fetch_user', methods=['POST'])
def fetch_user():
    target = request.json['target']

    db = Dorm()
    user, _ = db.fetch_scheduling_link(target)
    if not user:
        return make_response(json.dumps({'error': 'No scheduling link found.'}))

    return make_response(json.dumps(user.for_json()))

@app.route('/schedule_meeting', methods=['POST'])
def schedule_meeting():
    try:
        info = request.json

        db = Dorm()
        user, _ = db.fetch_scheduling_link(info['target'])
        db.delete_scheduling_link(info['target'])
        
        if 'profile' not in session or session['profile']['user_id'] != 'test_user':
            # send emails
            send_guest_email(info, user.get_email(), user.get_name())
            send_host_email(info, user.get_email())

            # add to calendar/generate ical
            add_event(user.get_refresh_key(), user.get_email(), user.get_name(), info)

        return make_response(json.dumps('Meeting scheduled!'))
    except:
        return make_response(json.dumps(
            {'error': 'An error occurred. Please contact the system administrator.'}))

@app.route('/fetch_times', methods=['POST'])
def fetch_times():
    user = None
    try:
        target = request.json['target']

        DAYS_PER_WEEK = 7
        db = Dorm()
        user, link = db.fetch_scheduling_link(target)

        if not link:
            msg = 'This scheduling link is not available! Please contact ' + \
                  'the intended host for a working link.'
            return make_response(json.dumps({'error': msg}))

        busy = []
        # don't get times for tests
        if 'profile' not in session or session['profile']['user_id'] != 'test_user':
            busy = get_freebusy(user.get_refresh_key(),
                                user.get_email(),
                                link.get_start_scheduling(),
                                link.get_weeks_out() * DAYS_PER_WEEK)
            busy = parse_free_busy(busy)

        free = generate_time_slots(link.get_buffer_time(),
                                link.get_workday_start(),
                                link.get_workday_end(),
                                link.get_weekdays(),
                                busy,
                                link.get_meeting_length(),
                                link.get_weeks_out() * DAYS_PER_WEEK,
                                link.get_start_scheduling(),
                                link.get_half_hours())
        sort_slots(free)
    
        return make_response(json.dumps([slot.for_json() for slot in free]))
    except:
        if 'profile' not in session or session['profile']['user_id'] != 'test_user':
            send_host_refresh_email(user.get_email(), url_for('login_force', _external=True))
        return make_response(json.dumps(
            {'error': 'An error ocurred. The host has been notified of the issue. ' +
                      'Please contact them for further information.'}))

@app.route('/user_info', methods=['POST'])
def user_info():
    if 'profile' in session:
        db = Dorm()
        user = db.get_user(session['profile']['user_id'])
        return make_response(json.dumps(user.for_json()))
    return make_response(json.dumps('No user found'))

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
