#app/controllers/controler.py
from flask import render_template, request, flash, redirect, url_for
from app import db
from app.models.modelo import Paciente, Appointment, User, Cita, Settings
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

def obtenerCitas_paginas(page, per_page):
    try:
        citas = Cita.query.filter(Cita.status_id != 4).paginate(page=page, per_page=per_page, error_out=False)
        return citas
    except Exception as e:
        logging.error(f"Error al obtener Citas: {e}")
        return None

def obtener_intervalo():
    setting = Settings.query.filter_by(name='time_interval').first()
    return int(setting.value) if setting else 15

def actualizar_intervalo(nuevo_intervalo):
    setting = Settings.query.filter_by(name='time_interval').first()
    if setting:
        setting.value = str(nuevo_intervalo)
    else:
        setting = Settings(name='time_interval', value=str(nuevo_intervalo))
        db.session.add(setting)
    db.session.commit()

    

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

    try:
        # Extraer el ID del paciente de la cadena
        paciente_id = paciente.split('(')[-1].strip(')')
        paciente_id = int(paciente_id)
    except (ValueError, IndexError) as e:
        logging.error(f"Error al extraer el ID del paciente: {e}")
        return None

    nueva_cita = Cita(
        series_id=1,  # Ajustar este valor según la lógica de series
        start=inicio_datetime,
        end=fin_datetime,
        title=title,
        description=description,
        type_id=1,  # Ajustar según la lógica de tipo
        status_id=int(estado),  # Asegurándonos de que 'estado' sea un entero
        owner_id=paciente_id,  # Usar el ID extraído del paciente
        type_label=repetir,
        status_label=autorizacion,
        prioridad=prioridad,
        registro_llamada=registro_llamada,
        cual=cual,
        edad=edad
    )

    db.session.add(nueva_cita)
    db.session.commit()

    return nueva_cita

def obtener_intervalo():
    setting = db.session.query(Settings).filter_by(name='time_interval').first()
    return int(setting.value) if setting else 15

def actualizar_intervalo(nuevo_intervalo):
    setting = db.session.query(Settings).filter_by(name='time_interval').first()
    if setting:
        setting.value = str(nuevo_intervalo)
    else:
        setting = Settings(name='time_interval', value=str(nuevo_intervalo))
        db.session.add(setting)
    db.session.commit()
    
def obtener_usuario_por_id(user_id):
    return User.query.get(user_id)

def actualizar_usuario(user_id, form_data):
    usuario = obtener_usuario_por_id(user_id)
    
    if not usuario:
        logging.error(f"Usuario con ID {user_id} no encontrado.")
        return None

    # Actualizar los campos del usuario
    usuario.fname = form_data.get('fname', usuario.fname)
    usuario.lname = form_data.get('lname', usuario.lname)
    usuario.username = form_data.get('username', usuario.username)
    usuario.email = form_data.get('email', usuario.email)
    usuario.organization = form_data.get('organization', usuario.organization)
    usuario.position = form_data.get('position', usuario.position)
    usuario.phone = form_data.get('phone', usuario.phone)
    usuario.document_type = form_data.get('document_type', usuario.document_type)

    try:
        db.session.commit()
        logging.info(f"Usuario con ID {user_id} actualizado correctamente.")
        return usuario
    except Exception as e:
        logging.error(f"Error al actualizar el usuario: {e}")
        db.session.rollback()
        return None



def obtener_cita_por_id(cita_id):
    return Cita.query.get(cita_id)

def actualizar_cita(cita_id, form_data):
    cita = obtener_cita_por_id(cita_id)
    if cita:
        title = form_data.get('title')
        description = form_data.get('description')
        inicio_fecha = form_data.get('inicio_fecha')
        inicio_hora = form_data.get('inicio_hora')
        fin_fecha = form_data.get('fin_fecha')
        fin_hora = form_data.get('fin_hora')
        repetir = form_data.get('repetir')
        estado = int(form_data.get('estado'))
        edad = form_data.get('edad')
        prioridad = form_data.get('prioridad')
        registro_llamada = form_data.get('registro_llamada')
        cual = form_data.get('cual')

        try:
            cita.start = datetime.strptime(f"{inicio_fecha} {inicio_hora}", '%Y-%m-%d %H:%M')
            if fin_fecha and fin_hora:
                cita.end = datetime.strptime(f"{fin_fecha} {fin_hora}", '%Y-%m-%d %H:%M')
            else:
                cita.end = None
            cita.title = title
            cita.description = description
            cita.type_label = repetir
            cita.status_id = estado
            cita.edad = edad
            cita.prioridad = prioridad
            cita.registro_llamada = registro_llamada
            cita.cual = cual
            db.session.commit()
            return cita
        except ValueError as e:
            logging.error(f"Error al convertir fechas: {e}")
            return None
    return None


