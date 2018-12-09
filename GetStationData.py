#create/add item to config/__init__.py file with params for your station(s)
#retrieves an access token using a client credentials method; should use secrets (git ignore for now with template)

import requests
from ring_doorbell import Ring

from config import (
USER_EMAIL,
USER_PASSWORD,
CLIENT_ID,
CLIENT_SECRET,
SCOPE_SPACE_SEPARATED,
N_CLIENT_ID,
N_CLIENT_SECRET,
N_STATE,
N_AUTH_URL,
N_AUTHCODE,
R_USER,
R_PASS
)

def get_netatmo_access_token():
    payload = {'grant_type': 'password',
               'username': USER_EMAIL,
               'password': USER_PASSWORD,
               'client_id': CLIENT_ID,
               'client_secret': CLIENT_SECRET,
               'scope': SCOPE_SPACE_SEPARATED
               }
    try:
        response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
        response.raise_for_status()
        access_token=response.json()["access_token"]
        refresh_token=response.json()["refresh_token"]
        scope=response.json()["scope"]
        print("Your access token is:", access_token)
        print("Your refresh token is:", refresh_token)
        print("Your scopes are:", scope)
    
        params = {
            'access_token': access_token
        }
        return params

    except requests.exceptions.HTTPError as error:
        print(error.response.status_code, error.response.text)
        return error.response.text

def get_nest_access_token():
    try:
        url = "https://api.home.nest.com/oauth2/access_token"
        payload = "code=" + N_AUTHCODE + "&client_id=" + N_CLIENT_ID + "&client_secret=" + N_CLIENT_SECRET + "&grant_type=authorization_code"
        print ("Payload: " + payload)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, data=payload, headers=headers)
        accesstoken = response.text
        print("Nest Access Token: " + accesstoken + "; HTTP Response Code: " + str(response.status_code))
        return accesstoken
    except requests.exceptions.HTTPError as error:
        print(error.response.status_code, error.response.text)
        return error.response.text

def get_netatmo(auth):
    try:
        response = requests.post("https://api.netatmo.com/api/getstationsdata", params=auth)
        response.raise_for_status()
        filtereddata = response.json()["body"]
        return filtereddata
    except requests.exceptions.HTTPError as error:
        print(error.response.status_code, error.response.text)
        return error.response.text

def get_nest(nestauth):
    pass

def get_ring():
    '''
    auth and get battery information
    full list of properties: https://python-ring-doorbell.readthedocs.io/
    :return: list of devices with battery info
    '''
    rings = Ring(R_USER,R_PASS)
    print("Ring is Connected" + str(rings.is_connected))

    deviceinfo = []

    for dev in list(rings.stickup_cams + rings.chimes + rings.doorbells):
        # refresh data
        dev.update()
        devicename = dev.name
        batterystatus = dev.battery_life
        print('Device Name:  %s' % devicename, 'Battery Status: %s' % batterystatus)
        deviceinfo.append([devicename,batterystatus])

    print("Device Info %s" % str(deviceinfo))
    return list(deviceinfo)

