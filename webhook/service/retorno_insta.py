from flask import Blueprint,request,jsonify
from dotenv import load_dotenv
import requests
import os

intercambio_instagram = Blueprint('intercambio',__name__)

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirent_url = os.getenv('REDIRECT_URL')
url = 'https://api.instagram.com/oauth/access_token'

@intercambio_instagram.route('/intercambio',methods = ['POST'])
def informacion_de_intercambio(auth_callback):
    headers = {
    'User-Agent': 'Mozilla/5.0'
        }
    data={
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "authorization_code",
    "redirect_uri": redirent_url,
    "code": auth_callback
    }   
    respuesta_instagram = requests.post(url=url,data=data,headers=headers)
    respuesta_insta_json = respuesta_instagram.json()
    if respuesta_insta_json.get('access_token'):
        token_corto = respuesta_insta_json.get('access_token')
        user_id = respuesta_insta_json['user_id']
        if token_larga_duracion(token_corto):   
            return jsonify({'succes' : True ,'user_id' : user_id})
        else:
            return jsonify({'succes' : False,'error' : respuesta_insta_json})
    else:
        return jsonify({'success': False, 'error': respuesta_insta_json})
    



def token_larga_duracion(token_corto):
    url = 'https://graph.instagram.com/access_token'
    token_largo = requests.get(url, params={
    "grant_type": "ig_exchange_token",
    "client_secret": client_secret,
    "access_token": token_corto
    })
    if token_largo.status_code == 200:
        token_largo_json = token_largo.json()
        access_token = token_largo_json['access_token']
        with open('token_largo.txt','w') as token:
            token.write(access_token)
        return True
    else:
        return False