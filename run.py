from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

from views import general
app.register_blueprint(general.mod)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True, use_reloader=True, threaded=True)
