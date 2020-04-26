from flask import Blueprint, render_template, request, jsonify, session 
from models.photos import *

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
