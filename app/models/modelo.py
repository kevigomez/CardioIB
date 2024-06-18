from app import db
from datetime import datetime

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    tname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.BigInteger, nullable=False)
    branch = db.Column(db.String(100))
    document_type = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    rut_cc = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, username, tname, phone, branch, document_type, email, lastname, rut_cc):
        self.username = username
        self.tname = tname
        self.phone = phone
        self.branch = branch
        self.document_type = document_type
        self.email = email
        self.lastname = lastname
        self.rut_cc = rut_cc

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
