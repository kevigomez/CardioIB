from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()



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
    timezone = db.Column(db.String(85), nullable=False)
    language = db.Column(db.String(10), nullable=False)
    homepageid = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lastlogin = db.Column(db.DateTime, nullable=True)
    status_id = db.Column(db.Integer, nullable=False)
    legacyid = db.Column(db.String(16), nullable=True)
    legacypassword = db.Column(db.String(32), nullable=True)
    public_id = db.Column(db.String(20), nullable=True)
    allow_calendar_subscription = db.Column(db.Boolean, default=False)
    default_schedule_id = db.Column(db.Integer, nullable=True)
    credit_count = db.Column(db.Numeric(7, 2), default=0.00)
    terms_date_accepted = db.Column(db.DateTime, nullable=True)

    def __init__(self, fname,lname,username,email,password,salt,organization, position, phone, timezone, lenguage,homepageid,date_created,last_modified,lastlogin,status_id,legacyid,legacypassword,public_id,allow_calendar_subscription,default_schedule_id,credit_count,terms_date_accepted,):
       self.fname = fname
       self.lname = lname
       self.username = username
       self.email = email
       self.password = password
       self.salt = salt
       self.organization = organization
       self.position = position
       self.position = phone
       self.timezone = timezone
       self.lenguage = lenguage 
       self.homepageid = homepageid
       self.date_created = date_created 
       self.last_modified = last_modified
       self.lastlogin = lastlogin
       self.status_id = status_id
       self.legacyid = legacyid
       self.legacypassword = legacypassword
       self.public_id = public_id
       self.allow_calendar_subscription = allow_calendar_subscription
       self.default_schedule_id = default_schedule_id
       self.credit_count = credit_count
       self.terms_date_accepted = terms_date_accepted