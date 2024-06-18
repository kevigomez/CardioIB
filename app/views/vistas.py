#app/vistas.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.controllers.controler import registrar_paciente, obtener_pacientes, db, Appointment
from app.models.modelo import Paciente, Appointment
from datetime import datetime
from app.models.inicioSes import User, db
from flask_bcrypt import bcrypt

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User = username.query.filter_by(password=password).first()
        if User:
            # Si la contraseña no está cifrada, verifica sin cifrar
         if User.password == password and User.username==username or (User.username and bcrypt.check_password_hash(User.username, username)):
                session['user_id'] = User.user_id
                flash('Inicio de sesión exitoso!', 'success')
                return redirect(url_for('main.dashboard')) 
         return render_template("credencialesError.html")
    # If the request is GET or the login was unsuccessful, render the login page.
    return render_template("index.html")

# Ejemplo de función para el dashboard (debes definir esta función)
@main.route('/dashboard')
def dashboard():
    # Aquí puedes implementar la lógica para obtener datos del usuario
    # Asegúrate de verificar si el usuario tiene una sesión activa
    if 'username' in session:
        username = session['username']
        # Renderiza la plantilla del dashboard con los datos del usuario
        return render_template('view_administrator.html', username=username)
    else:
        # Si el usuario no tiene una sesión activa, redirige al inicio de sesión
        flash('Acceso no autorizado. Inicia sesión primero.', 'warning')
        return redirect(url_for('main.index'))

# Ejemplo de función para cerrar sesión
@main.route('/logout')
def logout():
    # Elimina el nombre de usuario de la sesión
    session.pop('username', None)
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('main.index'))

@main.route('/usuarios')
def usuarios():
    usuarios = obtener_pacientes()
    print(f"Usuarios obtenidos en la vista: {usuarios}")  # Línea de depuración
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

    usuarios = obtener_pacientes()
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
