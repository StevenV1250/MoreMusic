import requests, os, urllib.parse
from flask import Flask, redirect, request, jsonify, session
from datetime import datetime, timedelta
import json

# from routes.authentication import authentication_bp
from backend.routes.playlists import playlists_bp
from backend.routes.tracks import tracks_bp
from backend.routes.artists import artists_bp
from backend.routes.user import user_bp
from backend.routes.rec_artist import recs_bp
from backend.routes.rec_track import track_recs_bp

app = Flask(__name__)

# app.register_blueprint(authentication_bp)
app.register_blueprint(playlists_bp)
app.register_blueprint(tracks_bp)
app.register_blueprint(artists_bp)
app.register_blueprint(user_bp)
app.register_blueprint(recs_bp)
app.register_blueprint(track_recs_bp)


app.secret_key = '53d355f8-571a-4590-a310-1f9579440851'

CLIENT_ID = '8496cd00eb66495c84325ea43c868291'
CLIENT_SECRET = 'd7d7baa47f754b1296b0adf0cb16322a'
REDIRECT_URI = "http://localhost:5000/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

@app.route("/")
def index():
      return """
    <html>
<head>
    <title>Welcome to my Spotify App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
            text-align: center;
            color: #444;
        }
        .container {
            max-width: 600px;
            margin: 100px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #007bff;
            margin-bottom: 20px;
        }
        p {
            font-size: 18px;
            line-height: 1.6;
            margin-bottom: 30px;
            margin-right: 20px;
            margin-left: 20px;
        }
        a {
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: #fff;
            border-radius: 5px;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }
        .btn:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to MoreMusic!</h1>
        <p>MoreMusic allows you to discover new music and view your favorite songs and artists in Spotify!</p>
        <a href="/login" class="btn">Login with Spotify</a>
    </div>
</body>
</html>
    """

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
            session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
            
            return redirect('/all-time-top-tracks')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)