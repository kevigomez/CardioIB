# app/views/vistas.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

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
