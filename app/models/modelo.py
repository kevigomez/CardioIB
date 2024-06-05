#app/models/modelo.py

from app import db
class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.BigInteger, nullable=False)
    branch = db.Column(db.String(100))
    document_type = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    timezone = db.Column(db.String(50))
    rut_cc = db.Column(db.String(50), nullable=False)
    group_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, username, name, phone, branch, document_type, email, lastname, timezone, rut_cc, group_name):
        self.username = username
        self.name = name
        self.phone = phone
        self.branch = branch
        self.document_type = document_type
        self.email = email
        self.lastname = lastname
        self.timezone = timezone
        self.rut_cc = rut_cc
        self.group_name = group_name
