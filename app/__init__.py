import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root@localhost/arcposbpocardio02')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de la clave secreta
app.config['SECRET_KEY'] = os.urandom(24)

# Inicializar la base de datos y las migraciones
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Registrar Blueprints
from app.views.vistas import main as main_blueprint
app.register_blueprint(main_blueprint)

# Ejecutar la aplicación en modo de depuración si este archivo es el principal
if __name__ == '__main__':
    app.run(debug=True)

