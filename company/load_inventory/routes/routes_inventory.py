# importacion de los servicios que van a usar los endpoints.
from flask import Blueprint
from company.load_inventory.services.inventory import get_inventory_info,get_only_inventory_info,inventory_info,update_inventory_info,delete_complete_inventory

load_inventory = Blueprint('inventory',__name__)

'''
    Endpoints centrales de la API para la recuperacion del inventario o la informacion completa, subir,
    actualizar y eliminar informacion.
'''

@load_inventory.route('/search/<nombre_empresa>',methods = ['GET'])
def get_inventorys(nombre_empresa):
    return get_inventory_info(nombre_empresa)

@load_inventory.route('/inventory/<nombre_empresa>',methods = ['GET'])
def get_inventory(nombre_empresa):
    return get_only_inventory_info(nombre_empresa)

@load_inventory.route('/load',methods = ['POST'])
def create_inventory():
    return inventory_info()

@load_inventory.route('/update/<nombre_empresa>',methods = ['PUT'])
def update_inventory(nombre_empresa):
    return update_inventory_info(nombre_empresa)

@load_inventory.route('/delete/<nombre_empresa>',methods = ['DELETE'])
def delete_inventory(nombre_empresa):
    return delete_complete_inventory(nombre_empresa)