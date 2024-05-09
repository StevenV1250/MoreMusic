from flask import Blueprint, jsonify, redirect, session, render_template
from datetime import datetime
import requests

tracks_bp = Blueprint('tracks', __name__)

@tracks_bp.route('/all-time-top-tracks')
def get_all_time_top_tracks():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    all_time_top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=10&offset=1'
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    response = requests.get(all_time_top_tracks_url, headers=headers)
    all_time_top_tracks_data = response.json()

    if 'items' in all_time_top_tracks_data:
        tracks_with_artists = []
        track_ids =[]
        for item in all_time_top_tracks_data['items']:
            track_name = item['name']
            artists = [artist['name'] for artist in item['artists']]
            track_id = item['id']
            image_url = item['album']['images'][0]['url']
            tracks_with_artists.append({"track_name": track_name, "artists": artists, 'image_url':image_url})
            track_ids.append(track_id)
            data = jsonify(tracks_with_artists, track_ids)
        return render_template('top_tracks.html', data=tracks_with_artists)
    else:
        return jsonify({"message": "No tracks found"})


@tracks_bp.route('/mid-top-tracks')
def get_mid_top_tracks():
      if 'access_token' not in session:
            return redirect('/login')
      
      if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
      
      mid_top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=10&offset=1'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(mid_top_tracks_url, headers=headers)
      mid_top_tracks_data = response.json()

      if 'items' in mid_top_tracks_data:
        tracks_with_artists = []
        track_ids =[]
        for item in mid_top_tracks_data['items']:
            track_name = item['name']
            artists = [artist['name'] for artist in item['artists']]
            track_id = item['id']
            image_url = item['album']['images'][0]['url']
            tracks_with_artists.append({"track_name": track_name, "artists": artists, "image_url": image_url})
            track_ids.append(track_id)
            data = jsonify(tracks_with_artists, track_ids)
        return render_template('mid_tracks.html', data=tracks_with_artists)
      else:
        return jsonify({"message": "No tracks found"})

@tracks_bp.route('/recent-top-tracks')
def get_recent_top_tracks():
      if 'access_token' not in session:
            return redirect('/login')
      
      if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
      
      recent_top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=10&offset=1'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(recent_top_tracks_url, headers=headers)
      recent_top_tracks_data = response.json()

      if 'items' in recent_top_tracks_data:
        tracks_with_artists = []
        track_ids =[]
        for item in recent_top_tracks_data['items']:
            track_name = item['name']
            artists = [artist['name'] for artist in item['artists']]
            track_id = item['id']
            image_url = item['album']['images'][0]['url']
            tracks_with_artists.append({"track_name": track_name, "artists": artists, "image_url": image_url})
            track_ids.append(track_id)
            data = jsonify(tracks_with_artists, track_ids)
        return render_template('recent_tracks.html', data=tracks_with_artists)
      else:
        return jsonify({"message": "No tracks found"})

@tracks_bp.route("/get-song")
def get_song():

      get_tracks_url = 'https://api.spotify.com/v1/tracks/6sMPFkWOGqEGBqnHEZ2jfy'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }

      response = requests.get(get_tracks_url, headers=headers)
      get_tracks_data = response.json()

      return jsonify(get_tracks_data)

@tracks_bp.route('/all-time-top-tracks-recommendations')
def get_all_time_top_tracks_recommendations():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    all_time_top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=10&offset=1'
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    response = requests.get(all_time_top_tracks_url, headers=headers)
    all_time_top_tracks_data = response.json()

    if 'items' in all_time_top_tracks_data:
        tracks = [track['id'] for track in all_time_top_tracks_data['items']]  # Extract track IDs
        recommendations = []
        track_ids = []
        artists = []
        
        for track_id in tracks:
            recommendations_url = f'https://api.spotify.com/v1/recommendations?seed_tracks={track_id}&limit=1'
            recommendations_response = requests.get(recommendations_url, headers=headers)
            # if recommendations_response.status_code == 200:
            #      return("Passed")
            # if recommendations_response.status_code == 401:
            #      return("401") 
            # if recommendations_response.status_code == 403:
            #      return("403")
            # if recommendations_response.status_code == 429:
            #      return("429")
            # recommendations_url = f'https://api.spotify.com/v1/recommendations?seed_tracks={track_id}&limit=1'
            # recommendations_response = requests.get(recommendations_url, headers=headers)
            recommendations_data = recommendations_response.json()
            
            if 'tracks' in recommendations_data:
                # Extract song names and artists from recommendations
                for track in recommendations_data['tracks']:
                    track_name = track['name']
                    artists = (artist['name'] for artist in track['artists'])
                    id = track['id']
                    image_url = track['album']['images'][0]['url']  # Get the first image URL
                    recommendations.append({"track_name": track_name, "artists": artists, "image_url": image_url})
                    track_ids.append(id)
                    
        spotify_uris = [f'spotify:track:{track_id}' for track_id in track_ids]
        session['uris'] = spotify_uris


        return render_template('top_tracks_recs.html', data=recommendations)
    else:
        return jsonify({"message": "No tracks found"})

# @tracks_bp.route("/get-rec")
# def get_rec():
#     if 'access_token' not in session:
#         return redirect('/login')

#     if datetime.now().timestamp() > session['expires_at']:
#         return redirect('/refresh-token')

#     rec_url = 'https://api.spotify.com/v1/recommendations?seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical%2Ccountry&seed_tracks=0c6xIDDpzE81m2q797ordA'
#     headers = {
#         "Authorization": f"Bearer {session['access_token']}"
#     }

#     response = requests.get(rec_url, headers=headers)
#     return  jsonify(response.text)
    
@tracks_bp.route('/recent-top-tracks-recommendations')
def get_recent_top_tracks_recommendations():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    recent_top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=10&offset=1'
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    response = requests.get(recent_top_tracks_url, headers=headers)
    recent_top_tracks_data = response.json()

    if 'items' in recent_top_tracks_data:
        tracks = [track['id'] for track in recent_top_tracks_data['items']]  # Extract track IDs
        recommendations = []
        track_ids = []
        
        for track_id in tracks:
            recommendations_url = f'https://api.spotify.com/v1/recommendations?seed_tracks={track_id}&limit=1'
            recommendations_response = requests.get(recommendations_url, headers=headers)
            recommendations_data = recommendations_response.json()
            
            if 'tracks' in recommendations_data:
                # Extract song names and artists from recommendations
                for track in recommendations_data['tracks']:
                    track_name = track['name']
                    artists = (artist['name'] for artist in track['artists'])
                    id = track['id']
                    image_url = track['album']['images'][0]['url']  # Get the first image URL
                    recommendations.append({"track_name": track_name, "artists": artists, 'image_url': image_url})
                    track_ids.append(id)
                    
        spotify_recent_uris = [f'spotify:track:{track_id}' for track_id in track_ids]
        session['recent_uris'] = spotify_recent_uris


        return render_template('recent_tracks_recs.html', data=recommendations)
    else:
        return jsonify({"message": "No tracks found"})
    

@tracks_bp.route('/mid-top-tracks-recommendations')
def get_mid_top_tracks_recommendations():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    recent_top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=10&offset=1'
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    response = requests.get(recent_top_tracks_url, headers=headers)
    recent_top_tracks_data = response.json()

    if 'items' in recent_top_tracks_data:
        tracks = [track['id'] for track in recent_top_tracks_data['items']]  # Extract track IDs
        recommendations = []
        track_ids = []
        
        for track_id in tracks:
            recommendations_url = f'https://api.spotify.com/v1/recommendations?seed_tracks={track_id}&limit=1'
            recommendations_response = requests.get(recommendations_url, headers=headers)
            recommendations_data = recommendations_response.json()
            
            if 'tracks' in recommendations_data:
                # Extract song names and artists from recommendations
                for track in recommendations_data['tracks']:
                    track_name = track['name']
                    artists = (artist['name'] for artist in track['artists'])
                    id = track['id']
                    image_url = track['album']['images'][0]['url']  # Get the first image URL
                    recommendations.append({"track_name": track_name, "artists": artists, 'image_url': image_url})
                    track_ids.append(id)
                    
        spotify_recent_uris = [f'spotify:track:{track_id}' for track_id in track_ids]
        session['mid_uris'] = spotify_recent_uris


        return render_template('mid_tracks_recs.html', data=recommendations)
    else:
        return jsonify({"message": "No tracks found"})