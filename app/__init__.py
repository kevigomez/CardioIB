import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Crear instancias de extensiones
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

    # Inicializar las extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Registrar blueprints
    from app.views.vistas import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Inicializar configuraciones antes de la primera solicitud
    with app.app_context():
        initialize_settings()

    return app

def initialize_settings():
    from app.models.modelo import Settings
    if not Settings.query.filter_by(name='time_interval').first():
        default_setting = Settings(name='time_interval', value='15')
        db.session.add(default_setting)
        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)