#app/controllers/controler.py
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.modelo import Paciente, Appointment, User
from flask_sqlalchemy import SQLAlchemy

def registrar_usuarios(form_data):
    username = form_data['username']
    fname = form_data['fname']
    lname = form_data['lname']
    email = form_data['email']
    password = 'password'  # Asegúrate de manejar correctamente el hash del password
    salt = 'salt_value'  # Asegúrate de manejar correctamente el salt
    organization = form_data['organization']
    position = form_data.get('position', 'Cardio IB IPS')  # Valor predeterminado
    phone = form_data['phone']
    timezone = 'UTC'  # Ejemplo: Ajusta según necesites
    language = 'es'  # Ejemplo: Ajusta según necesites
    status_id = 1  # Ejemplo: Ajusta según necesites
    document_type = form_data['document_type']

    nuevo_usuario = User(
        fname=fname,
        lname=lname,
        username=username,
        email=email,
        password=password,
        salt=salt,
        organization=organization,
        position=position,
        phone=phone,
        timezone=timezone,
        language=language,
        status_id=status_id,
        document_type=document_type,
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return nuevo_usuario

def obtener_usuarios_paginados(page, per_page):
    try:
        users = User.query.paginate(page=page, per_page=per_page, error_out=False)
        return users
    except Exception as e:
        print(f"Error al obtener Usuarios: {e}")
        return None



def registrar_cita(form_data):
    date = form_data['date']
    time = form_data['time']
    user_id = form_data['user_id']
    description = form_data['description']

    nueva_cita = Appointment(
        date=date,
        time=time,
        user_id=user_id,
        description=description
    )
    db.session.add(nueva_cita)
    db.session.commit()

    return nueva_cita

def obtener_citas():
    return Appointment.query.all()


