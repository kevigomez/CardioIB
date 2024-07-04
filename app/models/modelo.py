#app/models/modelo.py
from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

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



class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(85), nullable=True)
    lname = db.Column(db.String(85), nullable=True)
    username = db.Column(db.String(85), nullable=True)
    email = db.Column(db.String(85), nullable=False)
    password = db.Column(db.String(85), nullable=False)
    salt = db.Column(db.String(85), nullable=False)
    organization = db.Column(db.String(85), nullable=True)
    position = db.Column(db.String(85), default='Cardio IB IPS')
    phone = db.Column(db.String(85), nullable=True)
    timezone = db.Column(db.String(85), nullable=False, default='UTC')
    language = db.Column(db.String(10), nullable=False, default='es')
    homepageid = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lastlogin = db.Column(db.DateTime, nullable=True)
    status_id = db.Column(db.Integer, nullable=False, default=1)
    legacyid = db.Column(db.String(16), nullable=True)
    legacypassword = db.Column(db.String(32), nullable=True)
    public_id = db.Column(db.String(20), nullable=True)
    allow_calendar_subscription = db.Column(db.Boolean, default=False)
    default_schedule_id = db.Column(db.Integer, nullable=True)
    credit_count = db.Column(db.Numeric(7, 2), default=0.00)
    terms_date_accepted = db.Column(db.DateTime, nullable=True)
    document_type = db.Column(db.String(50))

    def __init__(self, fname, lname, username, email, password, salt, organization, position, phone, timezone, language, homepageid=1, lastlogin=None, status_id=1, legacyid=None, legacypassword=None, public_id=None, allow_calendar_subscription=False, default_schedule_id=None, credit_count=0.00, terms_date_accepted=None, document_type=None):
       self.fname = fname
       self.lname = lname
       self.username = username
       self.email = email
       self.password = password
       self.salt = salt
       self.organization = organization
       self.position = position
       self.phone = phone
       self.timezone = timezone
       self.language = language
       self.homepageid = homepageid
       self.lastlogin = lastlogin
       self.status_id = status_id
       self.legacyid = legacyid
       self.legacypassword = legacypassword
       self.public_id = public_id
       self.allow_calendar_subscription = allow_calendar_subscription
       self.default_schedule_id = default_schedule_id
       self.credit_count = credit_count
       self.terms_date_accepted = terms_date_accepted
       self.document_type = document_type


class groups(db.Model):
    __tablename__='groups'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(85), nullable=True)
    admin_group_id = db.Column(db.Integer,  nullable=True)
    legacyid = db.Column(db.String(16), nullable=True)
    isdefault = db.Column(db.String(16), nullable=True)

    def __init__(self, group_id,name,admin_group_id,legacyid,isdefault):
        self.group_id = group_id
        self.name = name
        self.admin_group_id = admin_group_id
        self.legacyid = legacyid
        self.isdefault = isdefault
 
class User_groups(db.Model):
    __tablename__ = 'user_groups'
    user_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id   

class Cita(db.Model):
    __tablename__ = 'citas'

    cita_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    series_id = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime)
    title = db.Column(db.String(300))
    description = db.Column(db.Text)
    type_id = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)
    last_action_by = db.Column(db.Integer)
    type_label = db.Column(db.String(85))
    status_label = db.Column(db.String(85))

    def __init__(self, series_id, start, end, title, description, type_id, status_id, owner_id, type_label, status_label):
        self.series_id = series_id
        self.start = start
        self.end = end
        self.title = title
        self.description = description
        self.type_id = type_id
        self.status_id = status_id
        self.owner_id = owner_id
        self.type_label = type_label
        self.status_label = status_label
