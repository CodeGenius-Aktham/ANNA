from flask import request,jsonify
from datetime import datetime
import json


# Crea la memoria de la informacion de la empresa.
def company_info():
    try:
        data = request.get_json()
        source_filename = datetime.now().strftime('%d-%m-%Y')
        name = str(data.get('name'))
        company = str(data.get('company'))
        color = str(data.get('color'))
        tone = str(data.get('tone'))
        voice = str(data.get('voice'))
        lang = str(data.get('lang'))
        tags = str(data.get('tags'))
        restrictions = data.get('restrictions')
        role = str(data.get('role'))

        companyInfo = data['companyInfo']
        biz = str(companyInfo.get('biz'))
        does = str(companyInfo.get('does'))
        mission = str(companyInfo.get('mission'))
        values = str(companyInfo.get('values'))
        vision= str(companyInfo.get('vision'))

        socials = data['socials']
        instagram = str(socials.get('instagram'))
        facebook = str(socials.get('facebook'))
        linkedin = str(socials.get('linkedin'))
        whatsapp = str(socials.get('whatsapp'))

        
        data = {
                "name" : name,
                "company" : company,
                "color" : color,
                "tone" : tone,
                "voice" : voice,
                "lang" : lang,
                "tags" : tags,
                "restrictions" : restrictions,
                "role" : role,
                "companyInfo": {
                    "biz" : biz,
                    "does" : does,
                    "mission" : mission,
                    "values" : values,
                    "vision" : vision
                },
                "socials": {
                    "instagram": instagram,
                    "facebook" : facebook,
                    "linkedin" : linkedin,
                    "whatsapp" : whatsapp
                },
                "Last_update" : source_filename
            }

        # Crea y escribe el archivo json de la memoria de la empresa.
        with open(r'\modelo_ana\ana\company\load_empresa\info_company.json','w') as information:
            json.dump(data,information,indent=4)
        return jsonify(data),200
    
    except Exception as error:
        return jsonify({'Error' : f'error interno en la API : {error}.'}),400


# Nos deja ver el registro de toda la empresa.
def get_company_info(nombre_empresa):
    try:
        # regista el nombre de la empresa.
        company = str(nombre_empresa)

        with open(r'\modelo_ana\ana\company\load_empresa\info_company.json','r') as lectrua:
            dicc_compañia = json.load(lectrua)

        # Se busca que el nombre coincida con la empresa para registrada.
        if company == dicc_compañia['company']:
            return jsonify(dicc_compañia),200
        else:
            return jsonify('NOT FOUND'),404
    except Exception as error:
        return jsonify({'Error' : f'error interno en la API : {error}'}),400



# Actualizacion en especifico de la API.
def update_complete_company_info(nombre_empresa):
    try:
        data = request.get_json()

        source_filename = datetime.now().strftime('%d-%m-%Y')
        company = str(nombre_empresa)

        name = str(data.get('name'))
        company = str(data.get('company'))
        color = str(data.get('color'))
        tone = str(data.get('tone'))
        voice = str(data.get('voice'))
        lang = str(data.get('lang'))
        tags = str(data.get('tags'))
        restrictions = data.get('restrictions')
        role = str(data.get('role'))

        companyInfo = data['companyInfo']
        biz = str(companyInfo.get('biz'))
        does = str(companyInfo.get('does'))
        vision= str(companyInfo.get('vision_company'))
        mission = str(companyInfo.get('mision_company'))
        values = str(companyInfo.get('valores_company'))

        socials = data['socials']
        instagram = str(socials.get('instagram'))
        facebook = str(socials.get('facebook'))
        linkedin = str(socials.get('linkedin'))
        whatsapp = str(socials.get('whatsapp'))

        with open(r'\modelo_ana\ana\company\load_empresa\info_company.json','r') as update:
            info_company = json.load(update)

        if company == info_company.get('company'):
            data_new = {
                "name" : name,
                "company" : company,
                "color" : color,
                "tone" : tone,
                "voice" : voice,
                "lang" : lang,
                "tags" : tags,
                "restrictions" : restrictions,
                "role" : role,
                "companyInfo": {
                    "biz" : biz,
                    "does" : does,
                    "vision" : vision,
                    "mission" : mission,
                    "values" : values
                },
                "socials": {
                    "instagram": instagram,
                    "facebook" : facebook,
                    "linkedin" : linkedin,
                    "whatsapp" : whatsapp
                },
                "Last_update" : source_filename
            }

            with open(r'\modelo_ana\ana\company\load_empresa\info_company.json','w') as new:
                json.dump(data_new,new,indent=4)
            return jsonify(data_new),200
        else:
            return jsonify('NOT FOUND'),404

    except Exception as error:
        return jsonify({'Error' : f'Error en la actualizacion del contenido de la API : {error}.'}),400


# Elimina el registro.
def delete_complete_company_info(nombre_empresa):
    try:
        company_name = str(nombre_empresa)

        with open(r'\modelo_ana\ana\company\load_empresa\info_company.json','r') as delete:
            info_company = json.load(delete)

        if company_name == info_company.get('company'):
                info_company.clear()
                with open('info_company.json','w') as new_file:
                    json.dump(info_company,new_file,indent=4)
                return jsonify(info_company),200
        else:
            return jsonify('NOT FOUND'),404

    except Exception as error:
        return jsonify({'Error' : f'error en la eliminacion de informacion de la API : {error}'}),400