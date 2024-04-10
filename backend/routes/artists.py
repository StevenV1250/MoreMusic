from flask import Blueprint, jsonify, redirect, session
from datetime import datetime
import requests
import json

artists_bp = Blueprint('artists', __name__)

@artists_bp.route('/all-time-top-artists')
def get_all_time_top_artists():
      if 'access_token' not in session:
            return redirect('/login')
      
      if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
      
      all_time_top_artists_url = 'https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=15&offset=1'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(all_time_top_artists_url, headers=headers)
      all_time_top_artists_data = response.json()

      # return jsonify(all_time_top_artists_data)

      if 'items' in all_time_top_artists_data:
            artists = [track['name'] for track in all_time_top_artists_data['items']]
            return jsonify(artists)
      else:
            return jsonify({"message": "No artists found"})
      
@artists_bp.route('/mid-top-artists')
def get_mid_top_artists():
      if 'access_token' not in session:
            return redirect('/login')
      
      if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
      
      mid_top_artists_url = 'https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=15&offset=1'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(mid_top_artists_url, headers=headers)
      mid_top_artists_data = response.json()

      # return jsonify(all_time_top_artists_data)

      if 'items' in mid_top_artists_data:
            artists = [track['name'] for track in mid_top_artists_data['items']]
            return jsonify(artists)
      else:
            return jsonify({"message": "No artists found"})
      
@artists_bp.route('/recent-top-artists')
def get_recent_top_artists():
      if 'access_token' not in session:
            return redirect('/login')
      
      if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
      
      recent_top_artists_url = 'https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=15&offset=1'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(recent_top_artists_url, headers=headers)
      recent_top_artists_data = response.json()

      # return jsonify(all_time_top_artists_data)

      if 'items' in recent_top_artists_data:
            artists = [track['name'] for track in recent_top_artists_data['items']]
            return jsonify(artists)
      else:
            return jsonify({"message": "No artists found"})