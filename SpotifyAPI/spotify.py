from flask import Flask, redirect, request, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'temp'

CLIENT_ID = '14263120370a49fba72e10301ce51290'
CLIENT_SECRET = 'e9169ecc7d3247be99a980bf57515f38'
REDIRECT_URI = 'localhost:5000/callback'

@app.get('/') #endpoint 1
def index():
    if 'access_token' in session:
        return redirect(url_for('top_tracks'))
    else:
        return '<a href = "/login"> Login with Spotify </a>'

@app.get('/login') #endpoint 2
def login():
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'user-top-read' #info from own acct
    }

    query_params = []
    for key, value in payload.items():
        query_params.append(f"{key}={value}")

    AUTH_URL = 'https://accounts.spotify.com/authorize'
    redirect_url = 'https://accounts.spotify.com/authorize' + '?' + '&' .join(query_params)

    return redirect(redirect_url)

#need callback

@app.get('/callback')
def callback():
    code = request.args.get('code')
    payload = {
        'grant_type':'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post('https://account.spotify.com/api/token', data = payload)
    access_token = response.json()['access_token']
    return redirect(url_for('top_tracks'))

#last endpoint
@app.get('/top-tracks')
def top_tracks():
    print('hi')

if __name__ == '__main__':
    app.run(debug=True)

