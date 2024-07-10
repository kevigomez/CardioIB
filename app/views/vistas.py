#app/views/vistas.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.controllers.controler import registrar_usuarios, obtener_usuarios_paginados, register_cita, obtenerCitas_paginas
from app.models.modelo import Paciente, Appointment, User
from app import db
from flask_paginate import Pagination, get_page_parameter
import hashlib
import logging
from passlib.hash import pbkdf2_sha256
from flask_cors import CORS
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

main = Blueprint('main', __name__)

CORS(main)

appointments = {}

@main.route('/')
def home():
    # Devuelve una plantilla llamada 'index.html'
    return render_template('index.html')


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        logging.debug(f"Contraseña ingresada: {password}")
        # Realizar la consulta utilizando el modelo User
        user = User.query.filter_by(username=username).first()
        
        if user:
            # Hash la contraseña ingresada usando SHA-1
            logging.debug(f"Contraseña almacenada (hash): {user.password}")
            password_hash = hashlib.sha1(password.encode()).hexdigest()
            logging.debug(f"Hash de la contraseña ingresada: {password_hash}")
            
            # Verificar si el hash de la contraseña ingresada coincide con el hash almacenado
            if user.password == password_hash:
                session['user_id'] = user.user_id
                flash('Inicio de sesión exitoso!', 'success')
                return redirect(url_for('main.dashboard'))
        
        # Si la verificación falla, mostrar un mensaje de error
        flash('Credenciales incorrectas. Inténtalo de nuevo.', 'danger')
        return render_template("credencialesError.html")
    
    # Si el método es GET, renderizar la página de inicio de sesión
    return render_template("index.html")



@main.route('/dashboard')
def dashboard():
    return render_template('view_administrator.html')
    

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('main.index'))

@main.route('/usuarios')
def usuarios():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    paginated_users = obtener_usuarios_paginados(page, per_page)
    if paginated_users:
        return render_template('usuarios.html', users=paginated_users)
    else:
        return render_template('usuarios.html', users=[])

@main.route('/citas')
def citas():
    return render_template('calendariocitas.html')
          
@main.route('/calendario')
def calendario():
    return render_template('calendario.html')

@main.route('/reg_usuarios', methods=['GET', 'POST'])
def reg_usuarios():
    logging.debug(f"Formulario de datos recibidos: {request.form}")
    if request.method == 'POST':
        form_data = request.form
        registrar_usuarios(form_data)
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('main.usuarios'))
    return render_template('form_registrousuarios.html')


@main.route('/reg_citas', methods=['GET', 'POST'])
def reg_citas():
    logging.debug(f"Formulario de datos recibidos: {request.form}")
    if request.method == 'POST':
        form_data = request.form.to_dict()
        nueva_cita = register_cita(form_data)
        if nueva_cita:
            flash('Cita registrada exitosamente', 'success')
        else:
            flash('Error al registrar la cita', 'danger')
        return redirect(url_for('main.reg_citas'))
    return render_template('view_administrator.html')

@main.route('/search_user')
def search_user():
    query = request.args.get('query')
    if query:
        users = User.query.filter(User.rut_cc.like(f"%{query}%")).all()
        results = [
            {'fname': user.fname, 'lname': user.lname, 'email': user.email, 'rut_cc': user.rut_cc}
            for user in users
        ]
        return jsonify(results=results)
    return jsonify(results=[])




@main.route('/Consul_citas')
def Con_Citas():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    paginated_appointments = obtenerCitas_paginas(page, per_page)
    
    if paginated_appointments:
        no_canceladas = [cita for cita in paginated_appointments.items if cita.status_id != 2]
        canceladas = [cita for cita in paginated_appointments.items if cita.status_id == 2]
        citas_ordenadas = no_canceladas + canceladas

        paginated_appointments.items = citas_ordenadas

        return render_template('citas.html', citas=paginated_appointments)
    else:
        return render_template('citas.html', citas=[])






    

@main.route('/appointments/<date>', methods=['GET'])
def get_appointments(date):
    return jsonify(appointments.get(date, {}))

@main.route('/appointments', methods=['POST'])
def save_appointment():
    data = request.get_json()
    date = data['date']
    time = data['time']
    appointment = data['appointment']
    
    if date not in appointments:
        appointments[date] = {}
    appointments[date][time] = appointment
    
    return jsonify(success=True)



