# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/arcposbpocardio02'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu_clave_secreta'

db = SQLAlchemy(app)

# Importar Blueprints después de crear la app y db para evitar dependencias circulares
from app.views.vistas import main
app.register_blueprint(main)
