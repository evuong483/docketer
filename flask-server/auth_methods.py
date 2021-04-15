#------------------------------------------------------------------------------
# auth_methods.py
# Author: Erin Vuong
# Authorization token methods
#------------------------------------------------------------------------------
import http.client
import json

def get_refresh_token(user_id, check=False):
    # get user access token
    conn = http.client.HTTPSConnection('rank-scheduling.us.auth0.com')

    token_type, manager_token = get_manager_authorization()
    headers = { 'authorization': token_type + ' ' + manager_token }

    conn.request('GET',
                '/api/v2/users/' + user_id,
                headers=headers)

    res = conn.getresponse()
    client_data = res.read()
    client_data = json.loads(client_data.decode('utf-8'))
    if check:
        return None if 'refresh_token' not in \
            client_data['identities'][0] else \
                client_data['identities'][0]['refresh_token'] 
    return client_data['identities'][0]['refresh_token']

def get_manager_authorization():
    # get manager token
    conn = http.client.HTTPSConnection('rank-scheduling.us.auth0.com')

    payload = ('{\"client_id\":\"YOUR_CLIENT_ID_HERE\",'
        '\"client_secret\":\"YOUR_CLIENT_SECRET_HERE\",'
        '\"audience\":\"https://rank-scheduling.us.auth0.com/api/v2/\",'
        '\"grant_type\":\"client_credentials\"}')

    headers = { 'content-type': 'application/json' }

    conn.request('POST', '/oauth/token', payload, headers)

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode('utf-8'))
    return data['token_type'], data['access_token']