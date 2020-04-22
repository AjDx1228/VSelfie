from flask import Flask
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

from views import general
app.register_blueprint(general.mod)

db_session.global_init("db/vselfie.sqlite")

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True, use_reloader=True, threaded=True)
