#get an access token with GetAccessToken.py
#create/add item to config/__init__.py file with params for your station(s)
import requests

from config import (
ACCESS_TOKEN,
DEVICE_ID #optional

)

params = {
    'access_token': ACCESS_TOKEN
    #'device_id': DEVICE_ID
}

try:
    response = requests.post("https://api.netatmo.com/api/getstationsdata", params=params)
    response.raise_for_status()
    data = response.json()["body"]
    print (str(data))
except requests.exceptions.HTTPError as error:
    print(error.response.status_code, error.response.text)
