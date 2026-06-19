from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from pymongo import MongoClient
import certifi
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
mail = Mail(app)


# MongoDB connection
mongoclient = MongoClient(
    app.config['MONGO_URI'],
    tls=True,
    tlsCAFile=certifi.where()
)
db = mongoclient['adsproject']
print("Connected to database")

# Import and register Blueprints
from app.views import auth_view, chat_view, form_view, report_view, main_view

app.register_blueprint(auth_view.auth_bp)
app.register_blueprint(chat_view.chat_bp)
app.register_blueprint(form_view.form_bp)
app.register_blueprint(report_view.report_bp)
app.register_blueprint(main_view.main_bp)
