from flask import Blueprint, jsonify, redirect, session
from datetime import datetime
import requests

user_bp = Blueprint('user', __name__)

@user_bp.route('/get-user')
def get_user():
      get_user_url = 'https://api.spotify.com/v1/me'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }
      
      response = requests.get(get_user_url, headers=headers)
      user_data = response.json()

      return(user_data['id'])