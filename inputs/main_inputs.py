from flask import Flask
from flask_cors import CORS
from inputs.routes.rutas import ingreso_audio


app = Flask(__name__)
app.register_blueprint(ingreso_audio, url_prefix ='/query')
CORS(app,origins='https://codegenius-aktham.github.io',supports_credentials=True,methods=['POST'],allow_headers=['Content-Type', 'ngrok-skip-browser-warning'])

