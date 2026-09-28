# --- Importacion del modelo sherpa para la conversion a voz ---
import sherpa_onnx
import numpy as np # Uso de numpy para crecion de matrices.
from io import BytesIO
import wave 


# --- Rutas del modelo de voz ---
modelo_voz = r'D:\modelo_ana\ana\senses\modelo_voz\es_MX-claude-high.onnx'
tokens_dicc = r'D:\modelo_ana\ana\senses\modelo_voz\tokens.txt'
data_dir = r'D:\modelo_ana\ana\senses\modelo_voz\espeak-ng-data'

config = sherpa_onnx.OfflineTtsConfig() # Configuracion del modelo de texto a voz.

'''
    Especificamos el alojamiento del modelo de voz,
    de los tokens o diccionario del modelo y el idioma.
'''
config.model.vits.model = modelo_voz
config.model.vits.tokens = tokens_dicc
config.model.vits.data_dir = data_dir



tts = sherpa_onnx.OfflineTts(config = config) # Pasamos la configuracion directo al modelo.



# --- Funcion que ingresa y sube el mensaje para pasarlo a audio ---
def motor(mensaje):
    try:
        audio = tts.generate(text = mensaje) # Genera el audio.
        return audio
    except Exception as error:
        print(f'Error en el programa : {error}')
        return None

# --- Funcion que saca el audio generado por la salida especificada ---
def hablar(audio):
    try:
        # --- Conversion del sample del audio de 64 bits a un punto flotante de 32 ---
        entero_64 = np.array(audio.samples, dtype= np.float32)
        # Se normaliza el audio para usar el 100% del volumen de la salida.
        max_val = np.max(np.abs(entero_64)) + 1e-6 
        audio_normalizado = (entero_64/max_val) * 32767
        enteros_16 = audio_normalizado.astype(np.int16)
        '''
            Aplana el audio y eliminamos diferentes dimensiones del array principal
            y sea mas facil el procesamiento de los datos.
        '''
        aplanamiento_uno = np.squeeze(enteros_16)
        # apila ambos arrays para una lectura exacta de la matriz.
        tasa_muestreo = audio.sample_rate
        archivo_wav = BytesIO()
        with wave.open(archivo_wav,"wb") as archivo:
            archivo.setnchannels(1)
            archivo.setsampwidth(2)
            archivo.setframerate(tasa_muestreo)

            datos_audio = aplanamiento_uno.tobytes()

            archivo.writeframes(datos_audio)
        archivo_wav.seek(0)
        return archivo_wav
    except Exception as error:
        print(f'error en el programa de habla : {error}')
        return None


