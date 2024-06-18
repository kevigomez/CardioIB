from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User
from app import db

controlador = Blueprint('controlador', __name__)

@controlador.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('controlador.dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

@controlador.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ha cerrado sesión correctamente', 'success')
    return redirect(url_for('controlador.login'))

@controlador.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Debe iniciar sesión para acceder al panel', 'error')
        return redirect(url_for('controlador.login'))
    # Lógica para mostrar el dashboard
    return render_template('dashboard.html')
