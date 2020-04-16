from flask import Blueprint, render_template, request, redirect, jsonify

from data import photos
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

@mod.route('/selfie')
def index():
    return render_template('selfie.html')


@mod.route('/publish', methods=['POST'])
def publish_photo():
    photo = photos.Photo()
    photo.dataURI = request.get_json()['photo']
    session = db_session.create_session()
    session.add(photo)
    session.commit()

    return 'OK'