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

    def __init__(self, date, time, user_id, description):
        self.date = date
        self.time = time
        self.user_id = user_id
        self.description = description

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
    document_type = db.Column(db.String(50), nullable=True, default=None)
    user_groups = db.relationship('UserGroup', back_populates='user')

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

class Group(db.Model):
    __tablename__ = 'groups'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(85), nullable=True)
    admin_group_id = db.Column(db.Integer, nullable=True)
    legacyid = db.Column(db.String(16), nullable=True)
    isdefault = db.Column(db.String(16), nullable=True)
    user_groups = db.relationship('UserGroup', back_populates='group')

    def __init__(self, name, admin_group_id=None, legacyid=None, isdefault=None):
        self.name = name
        self.admin_group_id = admin_group_id
        self.legacyid = legacyid
        self.isdefault = isdefault

class UserGroup(db.Model):
    __tablename__ = 'user_groups'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), primary_key=True)
    user = db.relationship('User', back_populates='user_groups')
    group = db.relationship('Group', back_populates='user_groups')

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
    prioridad = db.Column(db.String(85))
    registro_llamada = db.Column(db.Integer, nullable=False)
    cual = db.Column(db.Text)
    edad = db.Column(db.Integer, nullable=False)

    def __init__(self, series_id, start, end, title, description, type_id, status_id, owner_id, type_label, status_label, prioridad, registro_llamada, cual, edad):
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
        self.prioridad = prioridad
        self.registro_llamada = registro_llamada
        self.cual = cual
        self.edad = edad

class Resource(db.Model):
    __tablename__ = 'resources'

    resource_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=False)
    name = db.Column(db.String(85), nullable=False)
    location = db.Column(db.String(255))
    contact_info = db.Column(db.String(255))
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    min_duration = db.Column(db.Integer)
    min_increment = db.Column(db.Integer)
    max_duration = db.Column(db.Integer)
    unit_cost = db.Column(db.Numeric(7, 2))
    autoassign = db.Column(db.SmallInteger, nullable=False, default=1)
    requires_approval = db.Column(db.SmallInteger, nullable=False)
    allow_multiday_reservations = db.Column(db.SmallInteger, nullable=False, default=1)
    max_participants = db.Column(db.Integer)
    min_notice_time_add = db.Column(db.Integer)
    max_notice_time = db.Column(db.Integer)
    image_name = db.Column(db.String(50))
    schedule_id = db.Column(db.SmallInteger, nullable=False)
    legacyid = db.Column(db.String(16))
    admin_group_id = db.Column(db.SmallInteger)
    public_id = db.Column(db.String(20))
    allow_calendar_subscription = db.Column(db.SmallInteger, nullable=False, default=0)
    sort_order = db.Column(db.SmallInteger)
    resource_type_id = db.Column(db.Integer)
    status_id = db.Column(db.SmallInteger, nullable=False, default=1)
    resource_status_reason_id = db.Column(db.SmallInteger)
    buffer_time = db.Column(db.Integer)
    enable_check_in = db.Column(db.SmallInteger, nullable=False, default=0)
    auto_release_minutes = db.Column(db.SmallInteger)
    color = db.Column(db.String(10))
    allow_display = db.Column(db.SmallInteger, nullable=False, default=0)
    credit_count = db.Column(db.Numeric(7, 2))
    peak_credit_count = db.Column(db.Numeric(7, 2))
    min_notice_time_update = db.Column(db.Integer)
    min_notice_time_delete = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    additional_properties = db.Column(db.Text)

    def __init__(self, resource_id, name, location=None, contact_info=None, description=None, notes=None, min_duration=None, min_increment=None, max_duration=None, unit_cost=None, autoassign=1, requires_approval=None, allow_multiday_reservations=1, max_participants=None, min_notice_time_add=None, max_notice_time=None, image_name=None, schedule_id=None, legacyid=None, admin_group_id=None, public_id=None, allow_calendar_subscription=0, sort_order=None, resource_type_id=None, status_id=1, resource_status_reason_id=None, buffer_time=None, enable_check_in=0, auto_release_minutes=None, color=None, allow_display=0, credit_count=None, peak_credit_count=None, min_notice_time_update=None, min_notice_time_delete=None, date_created=None, last_modified=None, additional_properties=None):
        self.resource_id = resource_id
        self.name = name
        self.location = location
        self.contact_info = contact_info
        self.description = description
        self.notes = notes
        self.min_duration = min_duration
        self.min_increment = min_increment
        self.max_duration = max_duration
        self.unit_cost = unit_cost
        self.autoassign = autoassign
        self.requires_approval = requires_approval
        self.allow_multiday_reservations = allow_multiday_reservations
        self.max_participants = max_participants
        self.min_notice_time_add = min_notice_time_add
        self.max_notice_time = max_notice_time
        self.image_name = image_name
        self.schedule_id = schedule_id
        self.legacyid = legacyid
        self.admin_group_id = admin_group_id
        self.public_id = public_id
        self.allow_calendar_subscription = allow_calendar_subscription
        self.sort_order = sort_order
        self.resource_type_id = resource_type_id
        self.status_id = status_id
        self.resource_status_reason_id = resource_status_reason_id
        self.buffer_time = buffer_time
        self.enable_check_in = enable_check_in
        self.auto_release_minutes = auto_release_minutes
        self.color = color
        self.allow_display = allow_display
        self.credit_count = credit_count
        self.peak_credit_count = peak_credit_count
        self.min_notice_time_update = min_notice_time_update
        self.min_notice_time_delete = min_notice_time_delete
        self.date_created = date_created
        self.last_modified = last_modified
        self.additional_properties = additional_properties

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)
