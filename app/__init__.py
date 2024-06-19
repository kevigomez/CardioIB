import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Crear las instancias de SQLAlchemy y Bcrypt fuera de la función create_app
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root@localhost/arcposbpocardio02')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de la clave secreta
    app.config['SECRET_KEY'] = os.urandom(24)

    # Inicializar la base de datos, migraciones y bcrypt con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Registrar Blueprints
    from app.views.vistas import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# Ejecutar la aplicación en modo de depuración si este archivo es el principal
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
