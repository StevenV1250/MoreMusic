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
      
      all_time_top_artists_url = 'https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=10&offset=1'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(all_time_top_artists_url, headers=headers)
      all_time_top_artists_data = response.json()

      if 'items' in all_time_top_artists_data:
            artists = [track['name'] for track in all_time_top_artists_data['items']]
            id = [track['id'] for track in all_time_top_artists_data['items']]
            session['all_time_artist_id'] = id
            return jsonify(artists, session['all_time_artist_id'])
      else:
            return jsonify({"message": "No artists found"})
      
@artists_bp.route('/mid-top-artists')
def get_mid_top_artists():
      if 'access_token' not in session:
            return redirect('/login')
      
      if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
      
      mid_top_artists_url = 'https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=10&offset=1'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(mid_top_artists_url, headers=headers)
      mid_top_artists_data = response.json()

      if 'items' in mid_top_artists_data:
            artists = [track['name'] for track in mid_top_artists_data['items']]
            id = [track['id'] for track in mid_top_artists_data['items']]
            session['mid_time_artist_id'] = id
            return jsonify(artists, session['mid_time_artist_id'])
      else:
            return jsonify({"message": "No artists found"})
      
@artists_bp.route('/recent-top-artists')
def get_recent_top_artists():
      if 'access_token' not in session:
            return redirect('/login')
      
      if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
      
      recent_top_artists_url = 'https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=10&offset=1'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(recent_top_artists_url, headers=headers)
      recent_top_artists_data = response.json()

      if 'items' in recent_top_artists_data:
            artists = [track['name'] for track in recent_top_artists_data['items']]
            id = [track['id'] for track in recent_top_artists_data['items']]
            session['recent_time_artist_id'] = id
            return jsonify(artists, session['recent_time_artist_id'])
      else:
            return jsonify({"message": "No artists found"})
      

@artists_bp.route("/get-artists")
def get_artists():
      
      get_artists_url = 'https://api.spotify.com/v1/artists/6OBGbSaBUvQtk9wpQfDbOE'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(get_artists_url, headers=headers)
      artists_data = response.json()

      return(artists_data)

@artists_bp.route("/get-related-artists")
def get_related_artists():
    related_artists_url = 'https://api.spotify.com/v1/artists/6OBGbSaBUvQtk9wpQfDbOE/related-artists'
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(related_artists_url, headers=headers)
    related_artists_data = response.json()

    if 'artists' in related_artists_data:
        related_artists = [artist['name'] for artist in related_artists_data['artists']]
        return jsonify(related_artists)
    else:
        return jsonify({"message": "No related artists found"})