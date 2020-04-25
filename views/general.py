import os

from flask import Blueprint, render_template, request, redirect, jsonify, session 
import requests
from data import photos, db_session, users
from models.photos import *
from models.users import *
import secrets

mod = Blueprint('general', __name__)
CLIENT_ID = os.getenv('CLIENT_ID', secrets.CLIENT_ID)
CLIENT_SECRET = os.getenv('CLIENT_SECRET', secrets.CLIENT_SECRET)

@mod.route('/')
def lenta():
    try: 
        photos = get_prev_photos()

        return render_template('lenta.html', photos=photos)
    except:
        return render_template('error.html')

@mod.route('/photos')
def get_html_photos():
    try: 
        offset = request.args.get('offset')
        photos = get_prev_photos(offset)

        return jsonify(photos)
    except:
        return jsonify([])

@mod.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile.html')
    else:
        return render_template('error.html')

@mod.route('/my_photos')
def my_photos():
    user = session.get('user')
    if user:
        vk_id = user['id']
        my_photos = get_photos_with_vk_id(vk_id)
        return jsonify(my_photos)
    else:
        return 'You are not authorized for this operation'


@mod.route('/selfie')
def index():
    return render_template('selfie.html')

@mod.route('/callback/vk/code')
def callback_vk():
    code = request.args.get('code')
    return render_template('authorize.html', code=code)

@mod.route('/authorize/vk')
def authorize_vk():
    try:
        code = request.args.get('code')
        response_data = requests.post(
            'https://oauth.vk.com/access_token',
            data={
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri':'{}://{}/callback/vk/code'.format(request.scheme, request.host),
                'code':code
            }).json()
        access_token = response_data['access_token']
        user = requests.post(
            'https://api.vk.com/method/users.get',
            data={
                'user_ids':response_data['user_id'],
                'fields':'photo_50',
                'access_token':response_data['access_token'],
                'v':'5.103'
            }).json()['response'][0]
        
        add_user_to_db(user)

        # Добавление сессии юзера
        session['user'] = user

        return user
    except:
        return {"error": "Unexpected error"}

@mod.route('/callback/vk/access_token')
def callback_vk_access_token():
    access_token = response_data['access_token']
    response = requests.post(
        'https://api.vk.com/method/users.get',
        data={
            'user_ids':response_data['user_id'],
            'fields':'photo_50',
            'access_token':response_data['access_token'],
            'v':'5.103'
        }).json()


@mod.route('/publish', methods=['POST'])
def publish_photo():
    user = session.get('user')
    if user:
        current_user_id = user['id']
    else:
        current_user_id = -1

    photo = request.get_json()['photo']
    add_photo_to_db(current_user_id, photo)

    return 'OK'

@mod.route('/logout')
def logout():
    session.pop('user')
    return 'OK'
