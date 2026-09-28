# Librerias para el uso del modelo de transcripcion de voz a texto.
from faster_whisper import WhisperModel



#--- Traspaso de lo grabado a whisper ---
def lectrua_de_audio(audio):
    try:
        # ---- Datos del modelo a usar ---
        model_size = 'small'
        model = WhisperModel(model_size, device='cpu', compute_type='int8',cpu_threads=4)
        # Texto completo
        string_completo = ''
        # Desempaquetado de la transcripcion de audio con los filtros necesarios para ruido.
        segmentos,info = model.transcribe(audio,beam_size=5, no_speech_threshold=0.6,vad_filter=True,)
        consulta_completa = [] # Lista para integar todo la consulta completa.
        # Iterador en los degmentos del texto.
        for segment in segmentos:
            if len(segment.text) < 2: # si el texto es menor que 2 busca palabras que no sean ruido.
                continue
            consulta_completa.append(segment.text.strip()) # Adjunta todo el texto a la lista quitando los espacios en blanco.
            print("[%.2fs -> %.2fs] %s"  % (segment.start,segment.end,segment.text))
        string_completo = ' '.join(consulta_completa) # Insertamos toda la consulta a un texto.
        return string_completo # Retornamos los datos obtenidos.
    except Exception as error:
        print(f'Error en la transcripcion : {error}')
        return None


