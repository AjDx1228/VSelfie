from data import db_session
from data import users

def add_user_to_db(user): 
    session = db_session.create_session()
    rows = (session).query(users.User) \
                .filter(users.User.vk_id == user['id']).all()
                
    if rows:
        return

    user_db = users.User()
    user_db.vk_id = user['id']
    user_db.name = user['first_name']
    user_db.surname = user['last_name']
    user_db.vk_photo = user['photo_50']

    session.add(user_db)
    session.commit()