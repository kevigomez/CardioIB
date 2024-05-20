from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)

    # Importar y registrar blueprints
    from .views.vistas import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Crear tablas si es necesario
    with app.app_context():
        db.create_all()

    return app
