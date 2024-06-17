#app/controllers/controler.py
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models.modelo import Paciente, Appointment

def registrar_paciente(form_data):
    username = form_data['username']
    tname = form_data['tname']
    phone = form_data['phone']
    branch = form_data['branch']  # Valor predeterminado de la sucursal
    document_type = form_data['document_type']
    email = form_data['email']
    lastname = form_data['lastname']
    rut_cc = form_data['rut_cc']

    nuevo_paciente = Paciente(
        username=username,
        tname=tname,
        phone=phone,
        branch=branch,
        document_type=document_type,
        email=email,
        lastname=lastname,
        rut_cc=rut_cc,
    )
    db.session.add(nuevo_paciente)
    db.session.commit()

    return nuevo_paciente

def obtener_pacientes():
    try:
        pacientes = Paciente.query.all()
        print(f"Pacientes obtenidos: {pacientes}")
        return pacientes
    except Exception as e:
        print(f"Error al obtener pacientes: {e}")
        return []



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