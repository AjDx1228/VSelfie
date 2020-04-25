from data import db_session
from data import photos

def get_prev_photos(offset=0): 
    MAX_PHOTOS = 5
    if offset == None or int(offset) < 0:
        offset = 0
    offset = int(offset)

    session = db_session.create_session()

    last_el = (session).query(photos.Photo) \
                      .order_by(photos.Photo.id.desc()) \
                      .first()
                          
    if not last_el:
        return []

    last_read_id = last_el.id - offset + 1
    result = []
    rows = (session).query(photos.Photo) \
                      .order_by(photos.Photo.id.desc()) \
                      .filter(photos.Photo.id < last_read_id) \
                      .limit(MAX_PHOTOS)

    for photo in rows:
        result.append(photo.dataURI)

    return result

def get_photos_with_vk_id(vk_id):
    result = []
    session = db_session.create_session()
    rows = (session).query(photos.Photo) \
                    .order_by(photos.Photo.id.desc()) \
                    .filter(photos.Photo.user_id == vk_id)
    
    for photo in rows:
        result.append(photo.dataURI)
    
    return result


def add_photo_to_db(current_user_id, photo_data):
    photo = photos.Photo()
    photo.user_id = current_user_id
    photo.dataURI = photo_data
    session = db_session.create_session()
    session.add(photo)
    session.commit()
