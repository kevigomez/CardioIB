# app/controllers/controller.py
from app import db
from app.models.modelo import Paciente

def registrar_paciente(form_data):
    username = form_data['username']
    name = form_data['name']
    phone = form_data['phone']
    branch = form_data['branch']  # Valor predeterminado de la sucursal
    document_type = form_data['document_type']
    email = form_data['email']
    lastname = form_data['lastname']
    timezone = form_data['timezone']
    rut_cc = form_data['rut_cc']
    group_name = form_data['group']

    nuevo_paciente = Paciente(
        username=username,
        name=name,
        phone=phone,
        branch=branch,
        document_type=document_type,
        email=email,
        lastname=lastname,
        timezone=timezone,
        rut_cc=rut_cc,
        group_name=group_name
    )
    db.session.add(nuevo_paciente)
    db.session.commit()

    return nuevo_paciente

def obtener_pacientes():
    return Paciente.query.all()
