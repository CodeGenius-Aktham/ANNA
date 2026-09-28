from flask import request,Blueprint
from inputs.services_input.into_input import captura_audio, response_modelo, generate_model

ingreso_audio = Blueprint('input',__name__)


@ingreso_audio.route('/into',methods = ['POST'])
def into_info():
    return captura_audio()

@ingreso_audio.route('/response',methods = ['POST'])
def response_ana():
    data = request.get_json()
    response = data.get("texto")
    return response_modelo(response)

@ingreso_audio.route('/generate',methods = ['POST'])
def speak_ana():
    data = request.get_json()
    generate = data.get("texto")
    return generate_model(generate)