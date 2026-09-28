from flask import Blueprint,request
from dotenv import load_dotenv
from webhook.service.message import ingreso_mensaje
from webhook.service.retorno_insta import informacion_de_intercambio
import os

load_dotenv()

webhook_instagram = Blueprint('message',__name__)
verify_token = os.getenv('VERIFY_TOKEN')


@webhook_instagram.route('/message_into',methods = ['POST','GET'])
def mensaje():
    if request.method == 'POST':
        return ingreso_mensaje()
    elif request.method == 'GET':
        if request.args.get('code'):
            auth_callback = request.args.get('code')
            return informacion_de_intercambio(auth_callback)
        elif request.args.get('hub.verify_token') == verify_token:
            challenge = request.args.get('hub.challenge')
            return str(challenge),200
        else:
            return "TOKEN_INVALIDO",403
    else:
        return "",405