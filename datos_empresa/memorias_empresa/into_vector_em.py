# Importacion del cliente de Chromabd para la vectorizacion de informacion
import chromadb
import json

# Lectura del archivo Json de la informacion de la empresa.
def archivo_json(ruta):
    with open(ruta,'r') as info_company:
        info_company = json.load(info_company)
    return info_company

# Vectorizacion de la informacion pasada por el Json de la informacion de la empresa.
def apertura_memoria_empresa(info_company):
    try:
        name = info_company['name']
        company = info_company['company']
        color = info_company['color']
        tone = info_company['tone']
        voice = info_company['voice']
        lang = info_company['lang']
        tags = info_company['tags']
        restrictions = info_company['restrictions']
        role = info_company['role']

        companyInfo = info_company['companyInfo']
        biz = companyInfo['biz']
        does = companyInfo['does']
        mission = companyInfo['mission']
        values = companyInfo['values']
        vision= str(companyInfo.get('vision'))

        socials = info_company['socials']
        instagram = socials['instagram']
        facebook = socials['facebook']
        linkedin = socials['linkedin']
        whatsapp = socials['whatsapp']
        last_update = info_company['Last_update']

        company_memories = chromadb.PersistentClient(path='./datos_empresa/memorias_empresa/empresa_db')
        collecton_company = company_memories.get_or_create_collection(name='company')
        collecton_company.upsert(
            documents= [name,company,color,tone,voice,lang,tags,restrictions,role,biz,does,mission,values,vision,instagram,facebook,linkedin,whatsapp,last_update],
            metadatas= [{'source':'name'},
                        {'source':'company'},
                        {'source':'color'},
                        {'source':'tone'},
                        {'source':'voice'},
                        {'source':'lang'},
                        {'source':'tags'},
                        {'source':'restrictions'},
                        {'source':'role'},
                        {'source':'biz'},
                        {'source':'does'},
                        {'source':'mission'},
                        {'source':'values'},
                        {'source':'vision'},
                        {'source':'instagram'},
                        {'source':'facebook'},
                        {'source':'linkedin'},
                        {'source':'whatsapp'},
                        {'source':'last_update'}],
            ids = [f'{name}_id1',f'{company}_id2',f'{color}_id3',f'{tone}_id4',f'{voice}_id5',f'{lang}_id6',f'{tags}_id7',
                    f'{restrictions}_id8',f'{role}_id9',f'{biz}_id10',f'{does}_id11',f'{mission}_id12',f'{values}_id13',
                    f'{vision}_id14',f'{instagram}_id15',f'{facebook}_id16',f'{linkedin}_id17',f'{whatsapp}_id18',f'{last_update}_id19']
            )
        return 'Memoria de la empresa subida con exito.'
    except Exception as error:
        print(f'Error en el traspaso de informacion de las memorias de la empresa a la base de datos vectorial: {error}.')

# Uso de la consulta por si se necesita verificar el estado de la incrustracion.
def consulta_empresa(consulta):
    if consulta is None:
        return 'No se escucho la consulta.'
    results_company = chromadb.PersistentClient(path='./datos_empresa/memorias_empresa/empresa_db')
    collection = results_company.get_collection(name='company')
    results = collection.query(
        query_texts= [consulta],
        n_results=1
    )
    return results['documents'][0]



ruta_company = r'\modelo_ana\ana\company\load_empresa\info_company.json'
archivo_json_company = archivo_json(ruta_company)
print(apertura_memoria_empresa(archivo_json_company))

