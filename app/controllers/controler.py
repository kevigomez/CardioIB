#app/controllers/controler.py
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.modelo import Paciente, Appointment, User, Cita
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

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




    

def obtener_citas():
    return Appointment.query.all()


def register_cita(form_data):
    logging.debug(f"Datos recibidos en register_cita: {form_data}")

    title = form_data.get('title')
    description = form_data.get('description')
    inicio_fecha = form_data.get('inicio_fecha')
    inicio_hora = form_data.get('inicio_hora')
    fin_fecha = form_data.get('fin_fecha')
    fin_hora = form_data.get('fin_hora')
    repetir = form_data.get('repetir')
    recursos = form_data.get('recursos')
    paciente = form_data.get('paciente')
    edad = form_data.get('edad')
    estado = form_data.get('estado')
    autorizacion = form_data.get('autorizacion')
    prioridad = form_data.get('prioridad')
    registro_llamada = form_data.get('registro_llamada')
    cual = form_data.get('cual')

    logging.debug(f"Inicio Fecha: {inicio_fecha}, Inicio Hora: {inicio_hora}")
    logging.debug(f"Fin Fecha: {fin_fecha}, Fin Hora: {fin_hora}")

    if not all([inicio_fecha, inicio_hora]):
        logging.error('Fecha y hora de inicio son requeridas.')
        return None

    try:
        inicio_datetime = datetime.strptime(f"{inicio_fecha} {inicio_hora}", '%Y-%m-%d %H:%M')
        fin_datetime = datetime.strptime(f"{fin_fecha} {fin_hora}", '%Y-%m-%d %H:%M') if fin_fecha and fin_hora else None
    except ValueError as e:
        logging.error(f"Error al convertir fechas: {e}")
        return None

    nueva_cita = Cita(
        series_id=1,  # Ajustar este valor según la lógica de series
        start=inicio_datetime,
        end=fin_datetime,
        title=title,
        description=description,
        type_id=1,  # Ajustar según la lógica de tipo
        status_id=int(estado),  # Asegurándonos de que 'estado' sea un entero
        owner_id=int(paciente),  # Asegurándonos de que 'paciente' sea un entero
        type_label=repetir,
        status_label=autorizacion
    )

    db.session.add(nueva_cita)
    db.session.commit()

    return nueva_cita
