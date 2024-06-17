from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Improved Database URI Handling
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root@localhost/arcposbpocardio02')  # Default to sqlite

app = Flask(__name__)

# Set Database URI Using Environment Variable
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# Recommended Configuration for Performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import Blueprints After App and Database Setup
from app.views.vistas import main
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
