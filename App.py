from flask import Flask, render_template, request, redirect

from data import db_session
from data import photos

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init("db/photos.sqlite")

@app.route('/')
def lenta():
    try: 
        offset = request.args.get('offset')
        photos = get_prev_photos(offset)

        return render_template('lenta.html', photos=photos)
    except:
        return render_template('error.html')

@app.route('/selfie')
def index():
    return render_template('selfie.html')


@app.route('/publish', methods=['POST'])
def publish_photo():
    photo = photos.Photo()
    photo.dataURI = request.get_json()['photo']
    session = db_session.create_session()
    session.add(photo)
    session.commit()

    return 'OK'


def get_prev_photos(offset=0): 
    MAX_PHOTOS = 5
    if offset == None or int(offset) < 0:
        offset = 0
    offset = int(offset) + MAX_PHOTOS

    session = db_session.create_session()
    result = []
    rows = (session).query(photos.Photo) \
                      .order_by(photos.Photo.id.desc()) \
                      .limit(offset) \
                      .all()
    for photo in rows:
        result.append(photo.dataURI)

    return result

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True, use_reloader=True, threaded=True)
