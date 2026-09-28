# Importancion de los servicios de funcionalidad de la API
from flask import Blueprint
from company.load_empresa.services.company import get_company_info,company_info,update_complete_company_info,delete_complete_company_info


memory_company = Blueprint('routes',__name__)

'''
    Endpoints centrales de la API para la recuperacion, subir,
    actualizar y eliminar informacion.
'''

@memory_company.route('search/<nombre_empresa>',methods = ['GET'])
def get_memorys(nombre_empresa):
    return get_company_info(nombre_empresa)


@memory_company.route('/carga', methods = ['POST'])
def create_memory():
    return company_info()

@memory_company.route('update/<nombre_empresa>',methods = ['PUT'])
def update_memory(nombre_empresa):
    return update_complete_company_info(nombre_empresa)


@memory_company.route('delete/<nombre_empresa>',methods = ['DELETE'])
def delete_memory(nombre_empresa):
    return delete_complete_company_info(nombre_empresa)