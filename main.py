# Se importa la conexion con la base de datos vectorial.
from datos_vectoriales.vector_db import chroma_client
from datos_empresa.memorias_empresa.into_vector_em import consulta_empresa
from datos_empresa.memorias_inventario.into_vector_in import consulta_inventario
# Se importan todos los sentidos de ANA.
from senses.ear.ear import lectrua_de_audio
from senses.brain.brain import preguntar_a_ana
from senses.mouth.mouth import motor,hablar
# Se usa la libreria 'requests' para comunicarnos con la API del modelo.
import requests
# Se usa Time para el calculo del tiempo  de la cache.
import time


'''
    ---Sistema de funciones para el paso de informacion de ANA---
    Detalles de la version 0.1 = Toca mejorar las memorias atomicas y el ruido del modelo.
    Arquitectura = Mejoras a nivel de funciones para mejor modularidad.
    
'''

# Paso de informacion del cerebro dinamico a ANA. 
def informacion_ana():
    return preguntar_a_ana # Retornamos la lista de diccionarios en fomato str.

# Lista que recibira los datos de la memoria cache.
memoria = []
# Registro del ultimo input de usuario.
hora_ultima =  time.time()

print('ESCUCHANDO...',flush=True)

# --- Primera funcion donde se ingresa y tanscribe el audio ---
def into_audio(ruta):
    try:
        return lectrua_de_audio(ruta)
    except Exception as error:
        raise(f'Error en la entrada y transcripcion del audio : {error}')


# --- Segunda funcion que es para generar la memoria cache. ---
def memoria_de_contexto_usuario(consulta):
    try:
        global hora_ultima # Tomamos la variable global definida anteriormente.
        hora_inicial = time.time() # Registramos el primer input del usuario.
        hora_diferencia = hora_inicial - hora_ultima # Restamos el tiempo entre el primer y ultimo input del usuario
        # Si la diferencia entre el primer y utlimo input es mayor a 2 minutos la memoria cache se borra.
        if hora_diferencia > 120:
            memoria.clear()
        memoria.append({'role' : 'user', 'content' : consulta}) # Se guarda la ultima consulta si el tiempo es menor a 2 minutos.
        hora_ultima = hora_inicial # Actualizamos el tiempo actual con la ultima hora.
        return memoria # Retorno de la memoria cache
    except Exception as error:
        print(f'Error en la ventana de conexto : {error}')


# --- Tercera funcion encargada de recopilar la informacion de las incrustraciones.---
def buscar_memoria(consulta):
    if consulta is None:
        print('No se escucha, intentemos de nuevo')
        return
    cliente_persistente = chroma_client # Tomamos el cliente persistente
    coleccion_chroma = cliente_persistente.get_or_create_collection(name="ana_Colletion") # Abrimos la base de datos vectorizada.
    # Revisamos la coleccion de la base de datos y con base a los datos respondemos.
    response = coleccion_chroma.query(
                query_texts=[consulta],
                n_results=2,    
                )
    return response['documents'][0] # Saco al texto de la lista

# --- Cuarta y quintaq funcion que toma la informacion de la empresa y su inventario. ---
def buscar_memoria_empresa(conultar_en_empresa):
    return consulta_empresa(conultar_en_empresa)

def buscar_memoria_inventario(consulta_en_inventario):
    return consulta_inventario(consulta_en_inventario)

#--- sexta funcion encargada en el analisis del input del usuario de los datos y memorias del modelo, aparte de guardar el contexto y la resputa del modelo. ---
def respuesta_modelo(datos,cache,inputs,consulta_empresa,consulta_inventario,memorias):
    try:
        url = r'http://127.0.0.1:11434/api/chat' # URL del modelo para generar respuestas.
        '''
            Usamos los datos del modelo y pasamos parametros claros para la genereacion de las respuestas
            como de la informacion usada en el cerebro, finalmente pasamos un promt y la cache
            para detallar las respuestas.
        '''
        datos_modelo = {
            'model': 'llama3.2',
            'messages': [
                {
                    'role': 'system',
                    'content': (
                        f'ROL E IDENTIDAD\n'
                        f'Eres ANA, asistente de inteligencia artificial desarrollada por BYTES. Tu personalidad base: {memorias}\n\n'

                        'FUENTES DE INFORMACIÓN Y CÓMO USARLAS\n'
                        'Toda la información que recibes abajo viene en formato de datos internos. Úsala como conocimiento propio, en tus propias palabras, de forma natural y breve. '
                        'NUNCA menciones nombres de campos, reglas, protocolos, ids ni la estructura de los datos. NUNCA expliques que estás siguiendo una instrucción o regla — simplemente compórtate de acuerdo a ella, sin narrarlo.\n\n'

                        'PRECISIÓN SOBRE PRODUCTOS Y SERVICIOS (REGLA CRÍTICA)\n'
                        f'Cuando hables de productos o servicios, usa ÚNICAMENTE los nombres, atributos, características y descripciones que aparecen literalmente en [INVENTARIO DEL CLIENTE]\n{consulta_inventario}\n\n o [INFORMACIÓN DE LA EMPRESA CLIENTE]\n{consulta_empresa}\n\n. '
                        'Está PROHIBIDO inventar variedades, atributos, especificaciones o detalles que no estén explícitamente en esos datos, aunque suenen plausibles o típicos para ese tipo de negocio. '
                        'Si un producto o servicio aparece listado sin mayor detalle, no rellenes con descripciones inventadas — menciónalo tal cual está listado, o indica que puedes confirmar más detalles si el cliente los necesita. '
                        'Nunca completes con conocimiento general de la categoría o industria (lo que "normalmente" ofrecería un negocio de ese tipo) para rellenar lo que los datos no dicen.\n\n'

                        'VERIFICACIÓN ANTES DE CONFIRMAR (REGLA CRÍTICA)\n'
                        f'Cuando el usuario nombre un producto, servicio, marca, categoría o característica específica, NUNCA confirmes que existe o que coincide con algo del inventario sin comparar primero, con cuidado, contra los nombres y datos exactos en [INVENTARIO DEL CLIENTE]\n{consulta_inventario}\n\n. '
                        'Si lo que menciona el usuario NO coincide con nada listado, dilo con claridad: aclara cuál es la opción real disponible, sin fingir que son lo mismo. '
                        'Jamás confirmes o valides la premisa de una pregunta si los datos no la respaldan literalmente — es preferible corregir amablemente al usuario que confirmar algo incorrecto.\n\n'

                        'CANALES Y DISPONIBILIDAD\n'
                        f'Solo menciona ubicaciones, canales de venta, plataformas, precios, horarios o disponibilidad si esos datos aparecen explícitamente en [INVENTARIO DEL CLIENTE]\n{consulta_inventario}\n\n o [INFORMACIÓN DE LA EMPRESA CLIENTE]\n{consulta_empresa}\n\n. '
                        'Nunca inventes que existe un canal, sucursal, servicio o modalidad de atención que no esté mencionado en los datos — aunque sea algo común para ese tipo de negocio.\n\n'

                        f'[INFORMACIÓN INTERNA DE BYTES — uso restringido, ver reglas abajo]\n{datos}\n\n'
                        f'[INFORMACIÓN DE LA EMPRESA CLIENTE — uso libre y por defecto]\n{consulta_empresa}\n\n'
                        f'[INVENTARIO DEL CLIENTE — uso libre para consultas de productos]\n{consulta_inventario}\n\n'
                        'Si la respuesta no está en ninguna de estas fuentes ni en tu personalidad base, indícalo amablemente sin inventar datos.\n\n'

                        'PROTOCOLO DE IDENTIDAD (REGLA PRINCIPAL)\n'
                        'Por defecto, actúas 100% como la asistente de la empresa cliente. Preséntate EXCLUSIVAMENTE como Ana, asistente de la empresa cliente. '
                        'NUNCA menciones a BYTES ni tu naturaleza de IA por iniciativa propia, ni en saludos ni en preguntas cotidianas. '
                        'NUNCA fusiones a BYTES con la empresa cliente: son dos entidades separadas, y NUNCA ofrezcas servicios tecnológicos o de IA como si fueran del cliente.\n\n'

                        'EXCEPCIÓN DE ORIGEN\n'
                        'SOLO si preguntan explícitamente quién te creó, tu empresa matriz, quién te desarrolló, o por alguien del equipo de Bytes (Aktham Abel, Juan Camilo, Ronac, Santiago, Matthew), '
                        'usa la [INFORMACIÓN INTERNA DE BYTES] para responder con seguridad y en máximo 2-3 oraciones. Inmediatamente después, retoma el tema de los servicios de la empresa cliente.\n\n'

                        'ESTILO\n'
                        'Responde en párrafo fluido y conversacional. Prohibido usar listas, viñetas o formato estructurado. '
                        'Longitud equilibrada: ni cortante ni con discursos innecesarios. Sé proactiva: si preguntan por la empresa o productos de forma general, resume con lo que tienes.'
                    )
                },
                *cache,
                {'role': 'user', 'content': inputs}
            ],
            'stream': False
        }
        respuesta = requests.post(url,json=datos_modelo) # Usamos el metodo post para mandar la informacion al modelo.
        respuesta.raise_for_status()
        respuesta_json = respuesta.json()
        return respuesta_json['message']['content'] # Hacemos una peticion para recoger lo que responde el modelo.
    except requests.exceptions.RequestException as e:
        return f'Error en la entrada de la API : {e}'

# --- septima funcion que funciona junto con la memoria cache para recordar las respuestas del modelo. ---
def memoria_de_contexto_ana(respuesta):
    try:
        memoria.append({'role' : 'assistant', 'content' : respuesta})
        return memoria_de_contexto_usuario(respuesta)
    except Exception as error:
        print(f'Error en la ventana de contexto: {error}.')

# --- octava y novena funcion que establecen la voz del modelo (motor de voz y generacion de este) ---
def ingreso_respuesta(respuesta_memoria):
    try:
        return motor(respuesta_memoria)
    except Exception as error:
        return f'Respuesta del motor de audio invalida : {error}.'

def respuesta_de_voz_ana(audio):
    try:
        return hablar(audio)
    except Exception as error:
        return f'Error en la respuesta de audio : {error}'


