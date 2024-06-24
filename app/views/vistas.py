from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.controllers.controler import registrar_paciente, obtener_usuarios
from app.models.modelo import Paciente, Appointment, User
from datetime import datetime
from app import db, bcrypt  # Importa db y bcrypt desde tu aplicación principal
import hashlib
import logging

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.DEBUG)

def is_bcrypt_hash(hash_string):
    # Verifica si el hash tiene el formato típico de bcrypt
    return hash_string.startswith('$2b$') or hash_string.startswith('$2a$') or hash_string.startswith('$2y$')

def verify_password_sha1(stored_password, provided_password):
    hashed_provided_password = hashlib.sha1(provided_password.encode()).hexdigest()
    logging.debug(f"Hashed provided password: {hashed_provided_password}")
    logging.debug(f"Stored password: {stored_password}")
    return stored_password == hashed_provided_password

def migrate_password_to_bcrypt(user, provided_password):
    hashed_bcrypt_password = bcrypt.generate_password_hash(provided_password).decode('utf-8')
    user.password = hashed_bcrypt_password
    db.session.commit()
    logging.debug(f"Password for user {user.username} migrated to bcrypt.")

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Realizar la consulta utilizando el modelo User
        user = User.query.filter_by(username=username).first()
        
        if user:
            logging.debug(f"User {username} found in database.")
            if is_bcrypt_hash(user.password):
                logging.debug(f"User {username} has a bcrypt password hash.")
                # Intentar verificar con bcrypt
                if bcrypt.check_password_hash(user.password, password):
                    logging.debug(f"Password for user {username} verified using bcrypt.")
                    session['user_id'] = user.user_id
                    flash('Inicio de sesión exitoso!', 'success')
                    return redirect(url_for('main.dashboard'))
            else:
                logging.debug(f"User {username} has a SHA-1 password hash.")
                # Verificar usando SHA-1 y migrar a bcrypt si es exitoso
                if verify_password_sha1(user.password, password):
                    logging.debug(f"Password for user {username} verified using SHA-1.")
                    migrate_password_to_bcrypt(user, password)
                    session['user_id'] = user.user_id
                    flash('Inicio de sesión exitoso! Contraseña migrada a bcrypt.', 'success')
                    return redirect(url_for('main.dashboard'))
                else:
                    logging.debug(f"Password for user {username} could not be verified using SHA-1.")
        
        logging.debug(f"User {username} login failed.")
        # Si la verificación falla, renderizar la página de error de credenciales
        return render_template("credencialesError.html")
    
    # Si la solicitud es GET o el inicio de sesión no tuvo éxito, renderizar la página de inicio de sesión.
    return render_template("index.html")


@main.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        return render_template('view_administrator.html', user_id=user_id)
    else:
        flash('Acceso no autorizado. Inicia sesión primero.', 'warning')
        return redirect(url_for('main.index'))

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('main.index'))

@main.route('/usuarios')
def usuarios():
    usuarios = obtener_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)

@main.route('/citas')
def citas():
    return render_template('calendariocitas.html')

@main.route('/calendario')
def calendario():
    return render_template('calendario.html')

@main.route('/reg_usuarios', methods=['GET', 'POST'])
def reg_usuarios():
    if request.method == 'POST':
        form_data = request.form
        registrar_paciente(form_data)
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('main.usuarios'))

    usuarios = obtener_usuarios()
    return render_template('form_registrousuarios.html', usuarios=usuarios)

@main.route('/get_appointments', methods=['GET'])
def get_appointments():
    date = request.args.get('date')
    appointments = Appointment.query.filter_by(date=date).all()
    appointments_list = [{'id': appt.id, 'time': appt.time.strftime('%H:%M'), 'description': appt.description} for appt in appointments]
    return jsonify(appointments_list)

@main.route('/add_appointment', methods=['POST'])
def add_appointment():
    data = request.json
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    time = datetime.strptime(data['time'], '%H:%M').time()
    description = data['description']
    user_id = data['user_id']
    appointment = Appointment(date=date, time=time, user_id=user_id, description=description)
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'status': 'success'})
