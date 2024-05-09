from flask import Blueprint, jsonify, redirect, session, render_template
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
      id = user_data['id']
      email = user_data['email']
      membership = user_data['product']
      country = user_data['country']
      
      user_info = {
        'user_id': id,
        'email': email,
        'membership': membership,
        'country': country
      }
      
      return render_template('profile.html', **user_info)

@user_bp.route('/get-user-id')
def get_user_id():
      get_user_url = 'https://api.spotify.com/v1/me'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }
      
      response = requests.get(get_user_url, headers=headers)
      user_data = response.json()
      id = user_data['id']
      
      return (id)

@user_bp.route('/get-user-test')
def get_user_test():
      get_user_url = 'https://api.spotify.com/v1/me'
      headers = {
            "Authorization": f"Bearer {session['access_token']}"
      }
      
      response = requests.get(get_user_url, headers=headers)
      user_data = response.json()
      
      return (user_data)