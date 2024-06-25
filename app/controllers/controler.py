#app/controllers/controler.py
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models.modelo import Paciente, Appointment, User

def registrar_usuarios(form_data):
    username = form_data['username']
    fname = form_data['fname']
    phone = form_data['phone']
    branch = form_data['branch']  # Valor predeterminado de la sucursal
    document_type = form_data['document_type']
    email = form_data['email']
    lastname = form_data['lastname']
    rut_cc = form_data['rut_cc']

    nuevo_usuario = User(
        username=username,
        fname=fname,
        phone=phone,
        branch=branch,
        document_type=document_type,
        email=email,
        lastname=lastname,
        rut_cc=rut_cc,
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



def upgrade():
    op.create_table('user_groups',
        sa.Column('group_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),  # Asegúrate de que autoincrement no esté aquí
        sa.Column('additional_column', sa.String(50), nullable=False),  # columna adicional de ejemplo
        # Añade cualquier otra columna que necesites
    )
    # Añade cualquier otra operación de migración que necesites
