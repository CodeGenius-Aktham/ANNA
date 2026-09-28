# Importacion del cliente de chromadb para vectorizar la informacion
import chromadb
import json

# Apertura del archivo json cargado en las APIS de ingreso del inventario.
def archivo_json(ruta):
    with open(ruta,'r') as inventory:
        company_inventory = json.load(inventory)
    return company_inventory

# Ingreso y vectorizacion del inventario de la empresa.
def apertura_memoria_inventario(company_inventory):
    try:
        companies = company_inventory['companies'][0]
        name_company = companies['name_company']
        sector = companies['sector']
        last_update = companies['last_update']

        details = companies['details']
        description = details['description']
        employees_count = details['employees_count']
        location = details['location']

        inventory = companies['inventory'][0]
        id_s = inventory['id']
        item = inventory['item']
        category = inventory['category']
        stock = inventory['stock']
        price = inventory['price']

        documento_unificado = (
            f"La empresa {name_company}, ubicada en {location} y dedicada al sector de {sector} enfocada en actividades {description}, "
            f"cuenta actualmente con {employees_count} empleados. Su ultima actualizacion fue el {last_update}. "
            f"En su inventario registra el producto {item} (ID: {id_s}) de la categoria {category}, "
            f"con un stock disponible de {stock} unidades a un precio de {price} pesos. "
        )

        metadatos_de_control = {
            'source' : 'inventario_compañia',
            'name_company' : name_company,
            'item_id' : id_s,
            'category' : category,
            'last_update' : last_update
        }

        id_unico = f'{name_company}_prod_{id_s}'

        inventory_memories = chromadb.PersistentClient(path='./datos_empresa/memorias_inventario/inventario_db')
        collection_inventory = inventory_memories.get_or_create_collection(name='inventory')
        collection_inventory.upsert(
            documents=[documento_unificado],
            metadatas=[metadatos_de_control],
            ids=[id_unico]
            )

        return 'Inventario de la empresa subido con exito.'
    except Exception as error:
        print(f'Error en el traspaso del inventario a la base de datos vectorial: {error}.')


# Se usa la consulta si se necesita ver el cargue efectivo del inventario.
def consulta_inventario(consulta):
    if consulta is None:
        return 'No se escucho la consulta.'
    results_company = chromadb.PersistentClient(path='./datos_empresa/memorias_inventario/inventario_db')
    collection = results_company.get_collection(name='inventory')
    results = collection.query(
        query_texts= [consulta],
        n_results=1
    )
    return results['documents'][0]


ruta_inventory = r'D:\modelo_ana\ana\company\load_inventory\company_inventory.json'
archivo_json_inventory =  archivo_json(ruta_inventory)
print(apertura_memoria_inventario(archivo_json_inventory))
