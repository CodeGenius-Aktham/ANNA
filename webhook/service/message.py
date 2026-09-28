from flask import request
from senses.brain import cerebro_ana
from dotenv import load_dotenv
import requests
import os


load_dotenv()

def informacion_ana():
    return cerebro_ana



#ruta_info_empresa = 'load_empresa/services/info_company.json'
#ruta_info_inventario = 'load_inventory/services/company_inventory.json'
url_facebook = 'https://graph.instagram.com/v25.0/me/messages'

'''
with open(ruta_info_empresa,'r') as empresa:
    info_empresa = json.load(empresa)

with open(ruta_info_inventario,'r') as inventario:
    info_inventario = json.load(inventario)
'''

def ingreso_mensaje():
    try:
        url_model = r'http://127.0.0.1:11434/api/generate'
        respuesta = request.json
        print(respuesta)
        entrada = respuesta['entry'][0]
        mensajeria = entrada['changes'][0]['value']
        cliente_id = mensajeria['sender']['id']
        cliente_mensaje = mensajeria['message']['text']
        datos_modelo = {
                'model' : 'llama3.2',
                'prompt' : (
                            f'ROL E IDENTIDAD\n'
                            f'Eres ANA, un asistente evolutivo. Tu personalidad y datos de la empresa que te creo son: {cerebro_ana}\n\n'
                            f'### TAREA ACTUAL\n'
                            f'Basándote en todo lo anterior, responde a la última consulta del usuario de forma natural y amable.\n'
                            f'Consulta actual: {cliente_mensaje}\n\n'
                            f'RESTRICCIONES DE ESTILO\n'
                            f'Evita usar listas numeradas o viñetas.\n'
                            f'No seas demasiado breve, pero tampoco te extiendas innecesariamente.\n'
                        ),
                'stream' : False
                }
        peticion_ollama = requests.post(url_model,json=datos_modelo) # Usamos el metodo post para mandar la informacion al modelo.
        if peticion_ollama.status_code == 200:
            respuesta_json = peticion_ollama.json()
            respuesta_ana = respuesta_json.get('response')
            respuesta_mensaje(cliente_id,respuesta_ana)
            return "MENSAJE_ENVIADO", 200
        else:
            return "RESPUESTA_INVALIDA",404
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR DE RED OLLAMA/FACEBOOK: {e}")
        return f'Error en la generacion de la respuesta: {e}',400
    except KeyError as key:
        print(f"❌ Error buscando una llave en el JSON de Meta: {key}")
        return "EVENTO_NO_SOPORTADO", 200
    except Exception as error:
        print(f"❌ ERROR INTERNO DETECTADO: {error}")
        return f'error interno en la API: {error}',400




def respuesta_mensaje(client_id,texto_enviar):
    try:
        with open('token_largo.txt','r') as token:
            token_largo = token.read()
        headers = {
            'content-type' : 'application/json',
            'Authorization' : f'Bearer {token_largo}'
        }
        data = {
            'recipient' : {
                'id' : client_id
            },
            'message' : {
                'text' : texto_enviar
            }
        }
        envio_meta = requests.post(url_facebook,headers=headers,json=data)
        if envio_meta.status_code == 200:
            return 'RESPUESTA_GENERADA',200
        else:
            return 'RESPUESTA_INVALIDA',404
    except Exception as error:
        print(f"❌ ERROR INTERNO DETECTADO: {error}")
        return f'error interno en la API: {error}',400