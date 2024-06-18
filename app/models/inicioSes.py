from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), unique=True, nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    salt = db.Column(db.String(100))
    organization = db.Column(db.String(100))
    position = db.Column(db.String(100))
    phone = db.Column(db.BigInteger, nullable=False)
    timezone = db.Column(db.String(100))
    language = db.Column(db.String(100))
    homepageid = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    lastlogin = db.Column(db.DateTime, default=db.func.current_timestamp())
    status_id = db.Column(db.Integer)
    legacyid = db.Column(db.String(100))
    legacypassword = db.Column(db.String(100))
    public_id = db.Column(db.String(100))
    allow_calendar_subscription = db.Column(db.String(100))
    default_schedule_id = db.Column(db.String(100))
    credit_count = db.Column(db.String(100))
    terms_date_accepted = db.Column(db.String(100))

    def __repr__(self):
        return f'<User {self.username}>'
