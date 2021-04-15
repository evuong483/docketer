from google.oauth2.credentials import Credentials 
from googleapiclient.discovery import build
import datetime
import json
import os
import pytz

GOOGLE_CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), 
                                          'client_secret.json')
CREDS = json.load(open(GOOGLE_CLIENT_SECRETS_FILE))

def add_event(refresh_token, host_email, host_name, args):
    credentials = Credentials(None, refresh_token=refresh_token, **CREDS['web'])
    service = build('calendar', 'v3', credentials=credentials)

    start = datetime.datetime.strptime(args['date'] + ' ' + args['start'],
                                       '%Y-%m-%d %I:%M %p')
    end = datetime.datetime.strptime(args['date'] + ' ' + args['end'],
                                       '%Y-%m-%d %I:%M %p')

    event = {
        'summary': 'Meeting with %s' % (args['name']),
        'location': 'TBD',
        'transparency': 'opaque',
        'description': '{} meeting with {} on {} from {} to {}.'\
                            .format(host_name, args['name'], args['pretty_date'],
                                    args['start'], args['end']),
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'America/New_York',
        },
        'attendees': [
            {'email': host_email,
             'displayName': host_name,
             'responseStatus': 'accepted'},
            {'email': args['email']},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

# used for checking refresh token validity
def get_avail(refresh_token):
    credentials = Credentials(None, refresh_token=refresh_token, **CREDS['web'])
    service = build('calendar', 'v3', credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary',
                                          timeMin=now,
                                          maxResults=10,
                                          singleEvents=True,
                                          orderBy='startTime').execute()

    return 'error' not in events_result

# gets free/busy from today to four days from now
def get_freebusy(refresh_token, email, start_days, end_days):
    credentials = Credentials(None, refresh_token=refresh_token, **CREDS['web'])
    service = build('calendar', 'v3', credentials=credentials)

    start = datetime.datetime.utcnow() + datetime.timedelta(days=start_days)
    end = start + datetime.timedelta(days=end_days)
    
    start = start.isoformat() + 'Z'
    end = end.isoformat() + 'Z'

    body = {
        'timeMin': start,
        'timeMax': end,
        'timeZone': 'America/New_York',
        'items': [{'id': email}]
    }
    
    event_results = service.freebusy().query(body=body).execute()

    # TODO: figure out which calendar would be correct
    cal_dict = event_results[u'calendars']
    dicts = [cal_dict[cal_name] for cal_name in cal_dict]
    return None if len(dicts) is 0 else dicts[0]
