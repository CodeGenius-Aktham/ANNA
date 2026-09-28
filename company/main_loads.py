# Uso de las librerias necesarias como flask e importaciones de los endpoints de la API.
from flask import Flask
from flask_cors import CORS
from company.load_empresa.routes.routes import memory_company
from company.load_inventory.routes.routes_inventory import load_inventory


# Construccion completa de la API junto con los endpoints y sus rutas.
app = Flask(__name__)
app.register_blueprint(memory_company,url_prefix='/empresa')
app.register_blueprint(load_inventory,url_prefix='/inventario')
CORS(app,origins='https://codegenius-aktham.github.io',supports_credentials=True,methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type', 'ngrok-skip-browser-warning'])
