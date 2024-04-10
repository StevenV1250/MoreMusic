import requests, os, urllib.parse
from flask import Flask, redirect, request, jsonify, session
from datetime import datetime, timedelta
import json

# from routes.authentication import authentication_bp
from backend.routes.playlists import playlists_bp
from backend.routes.tracks import tracks_bp
from backend.routes.artists import artists_bp
from backend.routes.user import user_bp

app = Flask(__name__)

# app.register_blueprint(authentication_bp)
app.register_blueprint(playlists_bp)
app.register_blueprint(tracks_bp)
app.register_blueprint(artists_bp)
app.register_blueprint(user_bp)

app.secret_key = '53d355f8-571a-4590-a310-1f9579440851'

CLIENT_ID = '9ff383952d84443bb06df68a202294df'
CLIENT_SECRET = 'fc753f180f2a4b50b7538947d8476844'
REDIRECT_URI = "http://localhost:5000/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

@app.route("/")
def index():
      return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
      scope = 'user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private'
      
      params = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'scope': scope,
            'redirect_uri': REDIRECT_URI,
            'show_dialog': True
      }

      auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

      return redirect(auth_url)



@app.route('/callback')
def callback():
      if 'error' in request.args:
            return jsonify({"error": request.args['error']})
      
      if 'code' in request.args:
            req_body = {
                  'code':request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': REDIRECT_URI,
                  'client_id': CLIENT_ID,
                  'client_secret': CLIENT_SECRET
            }

            response = requests.post(TOKEN_URL, data=req_body)
            token_info = response.json()

            session['access_token']  = token_info['access_token']
            session['refresh_token'] = token_info['refresh_token']
            session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']\
            
            return redirect('/all-time-top-tracks')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)