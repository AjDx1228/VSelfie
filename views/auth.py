import os

from flask import Blueprint, render_template, request, jsonify, session 
import requests
from models.users import *

mod = Blueprint('auth', __name__)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
APP_ENV = os.getenv('APP_ENV', 'development')

if (not CLIENT_ID or not CLIENT_SECRET):
    print('Create .env file with CLIENT_ID, CLIENT_SECRET')
    exit()

@mod.route('/callback/vk/code')
def callback_vk():
    code = request.args.get('code')
    return render_template('authorize.html', code=code)

@mod.route('/authorize/vk')
def authorize_vk():
    code = request.args.get('code')
    protocol = 'https'
    if APP_ENV == 'development':
        protocol = 'http'
    response_data = requests.post(
        'https://oauth.vk.com/access_token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri':'{}://{}/callback/vk/code'.format(protocol, request.host),
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
    
    add_user_to_db(user)

    # Добавление сессии юзера
    session['user'] = user

    return user

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

@mod.route('/logout')
def logout():
    session.pop('user', None)
    return 'OK'

@mod.route('/client_id')
def client_id():
    return jsonify(CLIENT_ID)