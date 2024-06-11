from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Asegúrate de que 'config.Config' sea correcto

    db.init_app(app)
    migrate = Migrate(app, db)

    # Importar Blueprints después de crear la app y db para evitar dependencias circulares
    from app.views.vistas import main
    app.register_blueprint(main)

    return app
