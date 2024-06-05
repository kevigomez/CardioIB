# app/views/vistas.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.controler import registrar_paciente, obtener_pacientes

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
    pacientes = obtener_pacientes()
    return render_template('usuarios.html', pacientes=pacientes)

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
        flash('Paciente registrado con éxito', 'success')
        return redirect(url_for('main.usuarios'))
    return render_template('form_registrousuarios.html')
