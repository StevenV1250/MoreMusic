from flask import Blueprint, jsonify, redirect, session, render_template
from datetime import datetime
import requests
import json

artists_bp = Blueprint('artists', __name__)

import requests
from flask import render_template, redirect, session, jsonify
from datetime import datetime

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
    artist_data = []

    if 'items' in all_time_top_artists_data:
        for artist in all_time_top_artists_data['items']:
            name = artist['name']
            id = artist['id']
            image_url = artist['images'][0]['url'] if artist['images'] else None
            artist_data.append({"name": name, "id": id, "image_url": image_url})

        session['all_time_artist_id'] = [artist['id'] for artist in artist_data]
        return render_template('top_artists.html', data=artist_data)
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
      artist_data = []

      if 'items' in mid_top_artists_data:
        for artist in mid_top_artists_data['items']:
            name = artist['name']
            id = artist['id']
            image_url = artist['images'][0]['url'] if artist['images'] else None
            artist_data.append({"name": name, "id": id, "image_url": image_url})

        session['mid_artist_id'] = [artist['id'] for artist in artist_data]
        return render_template('mid_artists.html', data=artist_data)
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
      artist_data = []

      if 'items' in recent_top_artists_data:
        for artist in recent_top_artists_data['items']:
            name = artist['name']
            id = artist['id']
            image_url = artist['images'][0]['url'] if artist['images'] else None
            artist_data.append({"name": name, "id": id, "image_url": image_url})

        session['recent_artist_id'] = [artist['id'] for artist in artist_data]
        return render_template('recent_artists.html', data=artist_data)
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