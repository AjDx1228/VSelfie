from data import db_session
from data import photos

db_session.global_init("db/photos.sqlite")

def get_prev_photos(offset=0): 
    MAX_PHOTOS = 5
    if offset == None or int(offset) < 0:
        offset = 0
    offset = int(offset)

    session = db_session.create_session()

    last_read_id = (session).query(photos.Photo) \
                      .order_by(photos.Photo.id.desc()) \
                      .first().id - offset + 1

    result = []
    rows = (session).query(photos.Photo) \
                      .order_by(photos.Photo.id.desc()) \
                      .filter(photos.Photo.id < last_read_id) \
                      .limit(MAX_PHOTOS)

    for photo in rows:
        result.append(photo.dataURI)

    return result