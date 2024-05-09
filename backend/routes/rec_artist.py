from flask import Blueprint, render_template, request
from datetime import datetime
import requests

LASTFM_API_KEY = "12e51022ae7c34488cca965324171388"

recs_bp = Blueprint('recs', __name__)

@recs_bp.route('/artist-rec', methods=['GET', 'POST'])
def artist_recommendations():
    if request.method == 'POST':
        favorite_artists = request.form.get('favorite_artists')
        recommendations = recommend_artist(favorite_artists)
        return render_template('recsrecs.html', recommendations=recommendations)
    return render_template('artist_form.html')

def get_similar_artists(artist):
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={artist}&api_key={LASTFM_API_KEY}&format=json&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'similarartists' in data and 'artist' in data['similarartists']:
            similar_artists = [artist['name'] for artist in data['similarartists']['artist']]
            return similar_artists
        else:
            print("No similar artists found for", artist)
            return []
    else:
        print("Failed to fetch data.")
        return []

def recommend_artist(favorite_artists):
    recommendations = []
    for artist in favorite_artists.split(','):
        similar_artists = get_similar_artists(artist.strip())
        recommendations.extend(similar_artists)
    return recommendations
