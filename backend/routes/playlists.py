from flask import Blueprint, jsonify, redirect, session, render_template
from datetime import datetime
import requests

from backend.routes.user import get_user, get_user_id
import backend.routes.tracks
from backend.routes.tracks import get_all_time_top_tracks_recommendations

playlists_bp = Blueprint('playlists', __name__)

@playlists_bp.route('/playlists')
def get_playlists():
      if 'access_token' not in session:
            return redirect('/login')
      
      if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
      

      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
      playlists_data = response.json()

      if 'items' in playlists_data:
            playlists = [playlist['name'] for playlist in playlists_data['items']]
            return jsonify(playlists)
      else:
            return jsonify({"message": "No playlists found"})
      
@playlists_bp.route('/create-playlists')
def create_playlist():
      user_id = get_user()
      create_playlist_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
      headers = {
            "Authorization": f"Bearer {session['access_token']}",
            'Content-Type': 'application/json'
      }
      body = {
            "name": "i hate this",
            "public": False,
            "collaborative": False,
            "description": "Testing endpoint and route"
      }

      response = requests.post(create_playlist_url, headers=headers, json=body) 
      if response.status_code == 201:
            return "Playlist created successfully"
      else:
            return "Failed to create playlist"
      
@playlists_bp.route('/create-rec-playlists')
def create_rec_playlist():
      user_id = get_user_id()
      create_rec_playlist_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
      headers = {
            "Authorization": f"Bearer {session['access_token']}",
            'Content-Type': 'application/json'
      }
      body = {
            "name": "MoreMusic - 12 Month Playlist",
            "public": False,
            "collaborative": False,
            "description": "MoreMusic Playlist made up of song recommendations from your top 10 tracks of the year."
      }

      response = requests.post(create_rec_playlist_url, headers=headers, json=body) 
      
      playlist_id = response.json().get('id')
      
      add_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
      add_tracks_data = {"uris": session['uris']}
      add_tracks_response = requests.post(add_tracks_url, headers=headers, json=add_tracks_data)

      if add_tracks_response.status_code != 200:
            return jsonify({"error": "Failed to add tracks to playlist"}), add_tracks_response.status_code

      # return jsonify({"success": True, "playlist_id": playlist_id}), 201
      return render_template('playlist_created.html')

@playlists_bp.route('/create-recent-rec-playlists')
def create_recent_rec_playlist():
      user_id = get_user_id()
      create_rec_playlist_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
      headers = {
            "Authorization": f"Bearer {session['access_token']}",
            'Content-Type': 'application/json'
      }
      body = {
            "name": "More Music - 4 Week Playlist",
            "public": False,
            "collaborative": False,
            "description": "MoreMusic Playlist made up of song recommendations from your top 10 tracks of the past 4 weeks."
      }

      response = requests.post(create_rec_playlist_url, headers=headers, json=body) 
      
      playlist_id = response.json().get('id')
      
      add_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
      add_tracks_data = {"uris": session['recent_uris']}
      add_tracks_response = requests.post(add_tracks_url, headers=headers, json=add_tracks_data)

      if add_tracks_response.status_code != 200:
            return jsonify({"error": "Failed to add tracks to playlist"}), add_tracks_response.status_code

      # return jsonify({"success": True, "playlist_id": playlist_id}), 201
      return render_template('playlist_created.html')


@playlists_bp.route('/create-mid-rec-playlists')
def create_mid_rec_playlist():
      user_id = get_user_id()
      create_rec_playlist_url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
      headers = {
            "Authorization": f"Bearer {session['access_token']}",
            'Content-Type': 'application/json'
      }
      body = {
            "name": "MoreMusic - 6 Month Playlist",
            "public": False,
            "collaborative": False,
            "description": "MoreMusic Playlist made up of song recommendations from your top 10 tracks of the past 6 months"
      }

      response = requests.post(create_rec_playlist_url, headers=headers, json=body) 
      
      playlist_id = response.json().get('id')
      
      add_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
      add_tracks_data = {"uris": session['mid_uris']}
      add_tracks_response = requests.post(add_tracks_url, headers=headers, json=add_tracks_data)

      if add_tracks_response.status_code != 200:
            return jsonify({"error": "Failed to add tracks to playlist"}), add_tracks_response.status_code

      # return jsonify({"success": True, "playlist_id": playlist_id}), 201
      return render_template('playlist_created.html')

