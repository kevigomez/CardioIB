import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root@localhost/arcposbpocardio02')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
