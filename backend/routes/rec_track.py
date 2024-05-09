from flask import Blueprint, render_template, request
import requests

LASTFM_API_KEY = "12e51022ae7c34488cca965324171388"

track_recs_bp = Blueprint('track_recs', __name__)

# @track_recs_bp.route('/track-rec', methods=['GET', 'POST'])
# def track_recommendations():
#     if request.method == 'POST':
#         favorite_tracks = request.form.get('favorite_tracks')
#         recommendations = recommend_track(favorite_tracks)
#         return render_template('trackrecs.html', recommendations=recommendations)
#     return render_template('track_form.html')

# def get_similar_tracks(artist, track, limit=5):
#     url = f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={artist}&track={track}&api_key={LASTFM_API_KEY}&format=json&limit={limit}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if 'similartracks' in data and 'track' in data['similartracks']:
#             similar_tracks = [track['name'] for track in data['similartracks']['track']]
#             return similar_tracks
#         else:
#             print("No similar tracks found for", artist, "-", track)
#             return []
#     else:
#         print("Failed to fetch data:", response.text)
#         return []

# def recommend_track(favorite_tracks):
#     recommendations = []
#     for track in favorite_tracks.split(','):
#         similar_tracks = get_similar_tracks("Cher", track.strip())  # Example with artist "Cher"
#         recommendations.extend(similar_tracks)
#     return recommendations


# def get_similar_tracks(artist, track, api_key, limit=5):
#     url = f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={artist}&track={track}&api_key={api_key}&limit={limit}&format=json"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if 'similartracks' in data and 'track' in data['similartracks']:
#             similar_tracks = [track['name'] for track in data['similartracks']['track']]
#             return similar_tracks
#     return []

# # Example usage
# api_key = '12e51022ae7c34488cca965324171388'
# artist = 'juice wrld'
# track = 'lucid dreams'
# similar_tracks = get_similar_tracks(artist, track, api_key)
# print(similar_tracks)

@track_recs_bp.route('/track-rec', methods=['GET', 'POST'])
def track_recommendations():
    if request.method == 'POST':
        artist = request.form.get('artist')
        track = request.form.get('track')
        recommendations = get_similar_tracks(artist, track)
        return render_template('trackrecs.html', favorite_track=f"{artist} - {track}", similar_tracks=recommendations)
    return render_template('track_form.html')

def get_similar_tracks(artist, track, limit=10):
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={artist}&track={track}&api_key={LASTFM_API_KEY}&limit={limit}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'similartracks' in data and 'track' in data['similartracks']:
            similar_tracks = [track['name'] for track in data['similartracks']['track']]
            return similar_tracks
    return []