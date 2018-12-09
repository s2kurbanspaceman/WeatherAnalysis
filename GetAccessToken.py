#Python 3.3 and Flask core example from Netatmo dev portal
#create/add items to config/__init__.py file with params for your station(s)
#Add your client_id, client_secret, the scopes you want and a state

from flask import Flask, render_template, redirect
from flask import request as r
import requests

from config import (
CLIENT_ID,
CLIENT_SECRET,
SCOPE,
STATE
)

app = Flask(__name__)

@app.route('/')
def sign():
    return "<form action='/signin' method='get'><button type='submit'>Sign in</button></form>"

#Authorization Code type authentication flow
@app.route('/signin', methods=['GET'])
def signin():
    # Test if "code" is provided in get parameters (that would mean that user has already accepted the app and has been redirected here)
    if r.args.get('code'):
        code = r.args.get('code')
        payload = {'grant_type': 'authorization_code',
           'client_id': CLIENT_ID,
           'client_secret': CLIENT_SECRET,
           'code': code,
           'redirect_uri': 'http://localhost:5000/signin'}
        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()
            access_token=response.json()["access_token"]
            refresh_token=response.json()["refresh_token"]
            scope=response.json()["scope"]
            return "<p>Your access_token is:" + access_token + "</p>"

        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)
    # Test if "error" is provided in get parameters (that would mean that the user has refused the app)
    elif r.args.get('error') == 'access_denied':
        return "The user refused to give access to his Netatmo data"
    # If "error" and "code" are not provided in get parameters: the user should be prompted to authorize your app
    else:

        payload = {'client_id':CLIENT_ID,
                'redirect_uri': "http://localhost:5000/signin",
                'scope': SCOPE,
                'state':STATE}
        try:
            response = requests.post("https://api.netatmo.com/oauth2/authorize", params=payload)
            response.raise_for_status()
            return redirect(response.url, code=302)
        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)

if __name__ == "__main__":
    app.run()
