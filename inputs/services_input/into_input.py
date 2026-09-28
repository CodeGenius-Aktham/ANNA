from flask import request,jsonify,send_file
from werkzeug.utils import secure_filename
from main import into_audio, informacion_ana, memoria_de_contexto_usuario,buscar_memoria,buscar_memoria_empresa,buscar_memoria_inventario,respuesta_modelo,memoria_de_contexto_ana,ingreso_respuesta,respuesta_de_voz_ana


def captura_audio():
    pista_audio = request.files.get("audio")
    if pista_audio:
        nombre_seguro = secure_filename(pista_audio.filename)
        ruta = f"./services_input/{nombre_seguro}"
        pista_audio.save(ruta)

        texto = into_audio(ruta)
        if not texto:
            return jsonify({'Error':'No se encontro la pista de audio'}),500
        return jsonify({'texto' : texto}),200


def response_modelo(texto):
        try:
            cache = memoria_de_contexto_usuario('Usuario: ' + texto + '.') # Pasamos la consulta del usuario en la memoria cache.
            datos = buscar_memoria(texto) # Busca los datos correspondientes respecto al input del usuario.
            consulta_empresarial = buscar_memoria_empresa(texto)
            consulta_de_inventario = buscar_memoria_inventario(texto)
            output = respuesta_modelo(datos,cache,texto,consulta_empresarial,consulta_de_inventario,memorias=informacion_ana()) # Toma tanto los datos generados por las memorias atomicas, la cache, la entrada del usuario y la informacion del cerebro
            cache_model = memoria_de_contexto_ana(' '+ output + '.') # Guarda la respuesta del modelo en la cache.
            return jsonify({'output' : output}),200
        except Exception as error:
            return jsonify({'Error' : f'error en el paso de la generacion de la respuesta : {error}'}),400                                                     


def generate_model(output):
        try:
            ingreso_a_conversion_voz = ingreso_respuesta(output + ' . ') # Pasa la respuesta al modelo TTS de generacion de voz.
            respuesta_de_voz = respuesta_de_voz_ana(ingreso_a_conversion_voz) # Genera la respuesta de voz del modelo.
            return send_file(respuesta_de_voz, mimetype='audio/wav'),200
        except Exception as error:
            return jsonify({'Error' : f'error en la generacion de la respuesta en voz : {error}'}),500