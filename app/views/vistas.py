from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.controllers.controler import registrar_paciente, obtener_pacientes, db, Appointment
from app.models.modelo import Paciente, Appointment
from app import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Sin verificación de credenciales por ahora
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Sesión cerrada', 'success')
    return redirect(url_for('main.index'))

@main.route('/dashboard')
def dashboard():
    return render_template('view_administrator.html')

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
        return redirect(url_for('main.reg_usuarios'))

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
