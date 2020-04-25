import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from flask import Flask
from data import db_session

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY', 'vselfie_secret_key')
APP_ENV = os.getenv('APP_ENV', 'development')
app.config['SECRET_KEY'] = SECRET_KEY


from views import general
app.register_blueprint(general.mod)

db_session.global_init("db/vselfie.sqlite")

if __name__ == '__main__':
    if APP_ENV == 'production':
        port = int(os.environ.get("PORT", 8080))
        app.run(port=port, host='0.0.0.0')
    else:
        app.run(port=8080, host='127.0.0.1', debug=True, use_reloader=True, threaded=True)
