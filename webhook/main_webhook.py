from flask import Flask
from webhook.route.webhook_insta import webhook_instagram


app = Flask(__name__)
app.register_blueprint(webhook_instagram)