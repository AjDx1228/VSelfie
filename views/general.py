from flask import Blueprint, render_template, request, redirect, jsonify
import requests
from data import photos, db_session, users
from models.photos import *
from models.users import *


mod = Blueprint('general', __name__)

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
    return render_template('profile.html')

@mod.route('/my_photos/<vk_id>')
def my_photos(vk_id):
    my_photos = get_photos_with_vk_id(vk_id)
    return jsonify(my_photos)


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
                'client_id':'7413978',
                'client_secret':'8dFRRkGF7bCpCVQLK0L2',
                'redirect_uri':'http://127.0.0.1:8080/callback/vk/code',
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
        
        # Унести в метод add_user в модели
        
        user_db = users.User()
        user_db.vk_id = user['id']
        user_db.name = user['first_name']
        user_db.surname = user['last_name']
        user_db.vk_photo = user['photo_50']

        session = db_session.create_session()
        session.add(user_db)
        session.commit()

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

@mod.route('/publish/<vk_id>', methods=['POST'])
def publish_photo(vk_id):
    # Получить пользователя, если не удаломь то -1
    current_user_id = vk_id

    # Унести в метод add_photo в моделях
    photo = photos.Photo()
    photo.user_id = current_user_id
    photo.dataURI = request.get_json()['photo']
    session = db_session.create_session()
    session.add(photo)
    session.commit()

    return 'OK'