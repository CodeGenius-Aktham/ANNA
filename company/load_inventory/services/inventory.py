from flask import request,jsonify
from datetime import datetime
import json


# Crea la memoria del inventario.
def inventory_info():
    try:
        # Se maneja el archivo form mandado desde el Fronted.
        archivo = request.files.get('inventory')
        contenido = archivo.read()
        data = json.loads(contenido)

        # Informacion de la compañia.
        source_filename = datetime.now().strftime('%d-%m-%Y')
        # Clave raiz del json para acceder a las demas claves internas.
        compañia = data['companies'][0]
        name_company = compañia['name_company']
        sector = compañia['sector']

        # Clave intermedia para los detalles de la empresa desde la raiz del json
        descripcion = compañia['details']

        # Informacion detallada de la compañia.
        company_description = descripcion['description']
        employees_count = descripcion['employees_count']
        location = descripcion['location']

        # Clave intermedia para el inventario desde la raiz del json
        inventario = compañia['inventory']
        lista_inventario = []
        for producto in inventario:
            # Informacion del inventario.
            lista_inventario.append(producto)

        inventory = {
        "companies": [
            {
                "name_company": name_company,
                "sector": sector,
                "last_update": source_filename,
                "details": {
                    "description": company_description,
                    "employees_count": employees_count,
                    "location": location
                },
                "inventory": lista_inventario
                }
            ]
        }

        with open(r'D:\modelo_ana\ana\company\load_inventory\company_inventory.json','w') as load:
            json.dump(inventory,load,indent=4)
        return jsonify(inventory),200
    
    except Exception as error:
        return jsonify({'Error' : f'error interno en la API : {error}'})

# Muetra toda la informacion de la memoria.
def get_inventory_info(nombre_empresa):
    try:
        name_company = str(nombre_empresa)
        
        with open(r'D:\modelo_ana\ana\company\load_inventory\company_inventory.json','r') as show:
            company_inventory = json.load(show)
        for linea in company_inventory['companies']:
            if linea['name_company'] == name_company:
                return jsonify(company_inventory),200
            else:
                return jsonify('NOT FOUND'),404
    except Exception as error:
        return jsonify({'Error' : f'Error interno en la muestra del archivo Json del inventario : {error}'})

# Muestra solamente la informacion del inventario.
def get_only_inventory_info(nombre_empresa):
    try:
        name_company = str(nombre_empresa)

        with open(r'D:\modelo_ana\ana\company\load_inventory\company_inventory.json','r') as one:
            company_inventory = json.load(one)
        for linea in company_inventory['companies']:
            if linea['name_company'] == name_company:
                return jsonify(linea['inventory']),200
            else:
                return jsonify('NOT FOUND'),404
    
    except Exception as error:
        return jsonify({'Error' : f'Error interno en la muestra del inventario : {error}.'}),400

# Actualiza la memoria del inventario.
def update_inventory_info(nombre_empresa):
    try:
        data = request.get_json()

        source_filename = datetime.now().strftime('%d-%m-%Y')
        name_company = str(nombre_empresa)

        # Clave raiz del json para acceder a las demas claves internas.
        compañia = data['companies'][0]
        name_company = compañia['name_company']
        sector = compañia['sector']

        # Clave intermedia para los detalles de la empresa desde la raiz del json
        descripcion = compañia['details']

        # Informacion detallada de la compañia.
        company_description = descripcion['description']
        employees_count = descripcion['employees_count']
        location = descripcion['location']

        # Clave intermedia para el inventario desde la raiz del json
        inventario = compañia['inventory']
        lista_inventario = []
        for producto in inventario:
            # Informacion del inventario.
            lista_inventario.append(producto)

        with open(r'D:\modelo_ana\ana\company\load_inventory\company_inventory.json','r') as one:
            company_inventory = json.load(one)
        for linea in company_inventory['companies']:
            if linea['name_company'] == name_company:
                inventory_update = {
                    "companies": [
                        {
                            "name_company": name_company,
                            "sector": sector,
                            "last_update": source_filename,
                            "details": {
                                "description": company_description,
                                "employees_count": employees_count,
                                "location": location
                            },
                            "inventory": lista_inventario
                            }
                        ]
                    }
                
                with open(r'D:\modelo_ana\ana\company\load_inventory\company_inventory.json','w') as upload:
                    json.dump(inventory_update,upload,indent=4)
                return jsonify(inventory_update),200
            else:
                return jsonify('NOT FOUND'),404

    except Exception as error:
        return jsonify({'Error' : f'Error interno en la actualizacion de una clave del inventario : {error}'}),400

# Elimina la memoria completa.
def delete_complete_inventory(nombre_empresa):
    try:
        name_company = str((nombre_empresa))

        with open(r'D:\modelo_ana\ana\company\load_inventory\company_inventory.json','r') as inventory:
            company_inventory = json.load(inventory)
        for linea in company_inventory['companies']:
            if linea['name_company'] == name_company:
                company_inventory.clear()
                with open(r'D:\modelo_ana\ana\company\load_inventory\company_inventory.json','w') as delete:
                    json.dump(company_inventory,delete,indent=4)
                return jsonify(company_inventory),200
            else:
                return jsonify('NOT FOUND'),404
    except Exception as error:
        return jsonify({'Error' : f'Error interno en la eliminacion del inventrario : {error}'}),400