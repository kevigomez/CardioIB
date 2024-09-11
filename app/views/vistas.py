#app/views/vistas.py
from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash, jsonify
from app.controllers.controler import registrar_usuarios, obtener_usuarios_paginados, register_cita, obtenerCitas_paginas, actualizar_intervalo, obtener_cita_por_id, actualizar_cita, obtener_usuario_por_id, actualizar_usuario, registrar_usuariosAses, save_blocked_dates_to_appointments, obtenerSchedule, obtener_intervalo_time, obtenerSchedules_true, obtener_timeSet_porIdSchedule
from app.models.modelo import Paciente, Appointment, User, Cita, Resource, TimeSet
from app import db
from flask_paginate import Pagination, get_page_parameter
import hashlib
import logging
from passlib.hash import pbkdf2_sha256
from flask_cors import CORS
from datetime import datetime
import pytz
from app.models.modelo import db, Settings
from functools import wraps
from flask import request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from datetime import timedelta


logging.basicConfig(level=logging.DEBUG)

main = Blueprint('main', __name__)

CORS(main)

appointments = {}





def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return render_template('sesionCerrada.html')
        return f(*args, **kwargs)
    return decorated_function


@main.route('/')
def home():
    # Devuelve una plantilla llamada 'index.html'
    return render_template('index.html')

app = Flask(__name__)

# Configuración de la clave secreta
app.secret_key = 'tu_clave_secreta_aqui'

# Configuración del tiempo de vida de la sesión
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        logging.debug(f"Contraseña ingresada: {password}")
        # Realizar la consulta utilizando el modelo User
        user = User.query.filter_by(username=username).first()
        if user:
            # Obtener el salt almacenado
            salt = user.salt
            logging.debug(f"Salt almacenado: {salt}")
            
            # Hash la contraseña ingresada usando SHA-1 con el salt
            password_salted = password.encode('utf-8') + salt.encode('utf-8')
            password_hash = hashlib.sha1(password_salted).hexdigest()
            logging.debug(f"Hash de la contraseña ingresada: {password_hash}")
            
            # Verificar si el hash de la contraseña ingresada coincide con el hash almacenado
            if user.password == password_hash:
                session.permanent = True  # Establecer la sesión como permanente
                session['user_id'] = user.user_id
                session['username'] = user.username
                session['fname'] = user.fname
                session['lname'] = user.lname
                logging.debug(f"Usuario de sesion: {session['fname']}")
                return redirect(url_for('main.dashboard'))
        
        # Si la verificación falla, mostrar un mensaje de error
        return render_template("credencialesError.html")
    
    # Si el método es GET, renderizar la página de inicio de sesión
    return render_template("index.html")

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('fname', None)
    session.pop('lname', None)
    # Elimina otros datos de sesión

    return render_template('logout.html')



@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('view_administrator.html')
    

@main.route('/usuarios')
@login_required
def usuarios():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    group_id = 5  # Define el ID del grupo que deseas filtrar
    paginated_users = obtener_usuarios_paginados(page, per_page, group_id=group_id)
    if paginated_users:
        return render_template('usuarios.html', users=paginated_users)
    else:
        return render_template('usuarios.html', users=[])

@main.route('/citas', methods=['GET'])
@login_required
def citas():
    # Consulta para obtener solo algunos recursos
    Shedule = obtenerSchedules_true()

    # Verifica el tipo de Shedule
    print(Shedule)
    print(type(Shedule)) 

    if not Shedule:
        flash('No hay horarios disponibles.')
        return redirect(url_for('main.home'))

    # Asumiendo que Shedule es una lista de objetos y quieres enviar el primer schedule_id
    scheduleId = Shedule[0].schedule_id if Shedule else None

    return render_template('calendariocitas.html', Shedule=Shedule, scheduleId=scheduleId)



          
@main.route('/calendario')
@login_required
def calendario():
    return render_template('calendario.html')

@main.route('/reg_usuarios', methods=['GET', 'POST'])
@login_required
def reg_usuarios():
    logging.debug(f"Formulario de datos recibidos: {request.form}")
    if request.method == 'POST':
        form_data = request.form
        registrar_usuarios(form_data)
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('main.usuarios'))
    return render_template('form_registrousuarios.html')


@main.route('/reg_usuariosAses', methods=['GET', 'POST'])
@login_required
def reg_usuariosAses():
    logging.debug(f"Formulario de datos recibidos: {request.form}")
    if request.method == 'POST':
        form_data = request.form
        registrar_usuariosAses(form_data)
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('main.usuarios'))
    return render_template('formRegisAsesor.html')


@main.route('/reg_citas', methods=['GET', 'POST'])
@login_required
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
@login_required
def search_user():
    query = request.args.get('query')
    if query:
        users = User.query.filter(User.organization.like(f"%{query}%")).all()
        results = [
            {'fname': user.fname, 'lname': user.lname, 'email': user.email, 'organization': user.organization}
            for user in users
        ]
        return jsonify(results=results)
    return jsonify(results=[])


@main.route('/Consul_citas')
@login_required
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

@main.route('/appointments', methods=['POST'])
@login_required
def save_appointment():
    data = request.get_json()
    date = data['date']
    time = data['time']
    appointment = data['appointment']
    
    if date not in appointments:
        appointments[date] = {}
    appointments[date][time] = appointment
    
    return jsonify(success=True)




@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        logging.debug("Procesando la solicitud POST en /admin")
        nuevo_intervalo = request.form.get('time-interval')
        schedule_id = request.form.get('schedule_id')
        weekday = request.form.get('weekday')
        tipo = request.form.get('tipo')

        logging.debug(f"Datos recibidos - Schedule ID: {schedule_id}, Weekday: {weekday}, Tipo: {tipo}, Intervalos: {nuevo_intervalo}")
    # Obtener los intervalos de tiempo organizados por día de la semana
    Schedules = obtenerSchedules_true()
    timeSet = obtenerSchedule()

    if request.method == 'POST':
        # Aquí procesas los datos enviados desde el formulario para actualizar los intervalos de tiempo
        nuevo_intervalo = request.form['time-interval']
        try:
            # Función que actualiza el intervalo en la base de datos
            actualizar_intervalo(nuevo_intervalo)
            flash('Intervalo de tiempo actualizado con éxito', 'success')
        except Exception as e:
            flash(f'Error al actualizar el intervalo de tiempo: {str(e)}', 'danger')

        return redirect(url_for('main.admin'))

    # Pasar el objeto `Schedules` a la plantilla para renderizar los intervalos en el modal
    return render_template('admin_int.html', timeSet=timeSet, Schedules=Schedules)






@main.route('/get_intervalos/<int:schedule_id>', methods=['GET'])
@login_required
def get_intervalos(schedule_id):
    # Obtener el día de la semana desde los parámetros
    weekDay = request.args.get('weekDay')

    # Obtener todos los intervalos para el schedule y día específicos
    intervals = db.session.query(TimeSet).filter_by(schedule_id=schedule_id, weekDay=weekDay).order_by(TimeSet.intervalStart).all()

    # Separar los intervalos en "citable" y "bloqueado"
    citables = [interval for interval in intervals if interval.tipe == 'citable']
    bloqueados = [interval for interval in intervals if interval.tipe == 'bloqueado']

    # Determinar el inicio y final del día usando los intervalos bloqueados
    if bloqueados:
        dia_inicio = bloqueados[0].intervalStart
        dia_fin = bloqueados[-1].intervalEnd

        # Convertir los valores de tiempo a objetos datetime si son cadenas
        if isinstance(dia_inicio, str):
            dia_inicio = datetime.strptime(dia_inicio, '%H:%M').time()
        if isinstance(dia_fin, str):
            dia_fin = datetime.strptime(dia_fin, '%H:%M').time()
    else:
        dia_inicio = datetime.strptime('00:00', '%H:%M').time()
        dia_fin = datetime.strptime('23:59', '%H:%M').time()

    # Ahora puedes llamar a strftime sin problemas
    dayStart = dia_inicio.strftime('%H:%M')
    dayEnd = dia_fin.strftime('%H:%M')

    # Transformar los intervalos citables en formato JSON
    response_intervals = [{
        'intervalStart': interval.intervalStart.strftime('%H:%M'),
        'intervalEnd': interval.intervalEnd.strftime('%H:%M')
    } for interval in citables]

    return jsonify({
        'intervals': response_intervals,
        'dayStart': dayStart,
        'dayEnd': dayEnd
    })




@main.route('/updateUsers/<int:user_id>', methods=['GET', 'POST'])
@login_required
def updateUsers(user_id):
    user = obtener_usuario_por_id(user_id)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        user_actualizado = actualizar_usuario(user_id, form_data)
        if user_actualizado:
            flash('Usuario actualizado exitosamente', 'success')
        else:
            flash('Error al actualizar el usuario', 'danger')
        return render_template('updateSucefull_users.html')
    return render_template('updateUsers.html', usuario=user)


@main.route('/delete_users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_users(user_id):
    user = obtener_usuario_por_id(user_id)
    if user:
        # Cambia el estado del user a "eliminado"
        user.status_id = '3'
        db.session.commit()
        flash('El usuario ha sido desactivado correctamente', 'success')
        return render_template('eliminado_user.html')
    else:
        flash('usuario no encontrada', 'danger')

    return redirect(url_for('main.dashboard'))


@main.route('/update_citas/<int:cita_id>', methods=['GET', 'POST'])
@login_required
def update_citas(cita_id):
    cita = obtener_cita_por_id(cita_id)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        cita_actualizada = actualizar_cita(cita_id, form_data)
        if cita_actualizada:
            flash('Cita actualizada exitosamente', 'success')
        else:
            flash('Error al actualizar la cita', 'danger')
        return render_template('updateSucefull.html')
    return render_template('update_citas.html', cita=cita)

@main.route('/update_intervalos', methods=['POST'])
def update_intervalos():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    updated_intervals = data.get('updated_intervals')

    # Procesar y actualizar solo los intervalos que se hayan modificado
    for day, intervals in updated_intervals.items():
        if 'citable' in intervals:
            # Actualizar solo los intervalos citables para ese día
            actualizar_intervalo(schedule_id, day, 'citable', intervals['citable'])
        
        if 'bloqueado' in intervals:
            # Actualizar solo los intervalos bloqueados para ese día
            actualizar_intervalo(schedule_id, day, 'bloqueado', intervals['bloqueado'])

    return jsonify({"message": "Intervalos actualizados con éxito"})



@main.route('/delete_citas/<int:cita_id>', methods=['GET', 'POST'])
@login_required
def delete_citas(cita_id):
    cita = Cita.query.get(cita_id)
    if cita:
        # Cambia el estado del cita a "eliminado"
        cita.status_id = '4'
        db.session.commit()
        flash('El doctor ha sido desactivado correctamente', 'success')
        return render_template('eliminado.html')
    else:
        flash('cita no encontrada', 'danger')

    return redirect(url_for('main.dashboard'))


@main.route('/get_appointments', methods=['GET'])
def get_appointments():
    try:
        resource_id = request.args.get('resource_id', type=int)
        if not resource_id:
            return jsonify({'message': 'ID de recurso no proporcionado'}), 400

        filtered_appointments = Cita.query.filter_by(resource_id=resource_id).all()
        
        appointments = []
        for cita in filtered_appointments:
            if cita.start and cita.end:  # Verifica que start y end no sean None
                appointments.append({
                    "cita_id": cita.cita_id,
                    "start": cita.start.strftime('%Y-%m-%dT%H:%M:%S'),
                    "end": cita.end.strftime('%Y-%m-%dT%H:%M:%S'),
                    "title": cita.title
                })
            else:
                app.logger.warning(f"Cita con ID {cita.cita_id} tiene valores de fecha inválidos.")
        
        return jsonify({"appointments": appointments})
    except Exception as e:
        app.logger.error(f"Error al obtener las citas: {e}")
        return jsonify({"message": f"Error al obtener las citas: {str(e)}"}), 500




@main.route('/get_blocked_dates', methods=['GET'])
def get_blocked_dates():
    try:
        resource_id = request.args.get('resource_id', type=int)
        if not resource_id:
            return jsonify({'message': 'ID de recurso no proporcionado'}), 400
        
        # Define la zona horaria correcta
        tz = pytz.timezone('America/Bogota')  # Cambia a la zona horaria que corresponda
        
        # Obtiene las fechas bloqueadas
        blocked_dates = Cita.query.filter_by(status_id=5, resource_id=resource_id).with_entities(Cita.start).all()
        
        # Verifica si hay fechas bloqueadas
        if not blocked_dates:
            return jsonify({'blocked_dates': []})

        # Convierte las fechas a la zona horaria especificada
        blocked_dates_list = [date.start.astimezone(tz).date().isoformat() for date in blocked_dates]
        
        return jsonify({'blocked_dates': blocked_dates_list})

    except Exception as e:
        return jsonify({'message': str(e)}), 500



    

@main.route('/bloqueo_citas')
@login_required
def bloqueo_citas():

    selected_resource_ids = [1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 21, 22]  # IDs de los recursos que deseas mostrar
    recursos = Resource.query.filter(Resource.resource_id.in_(selected_resource_ids)).all()
    
    # Obtener el recurso seleccionado de los parámetros de la URL
    selected_resource_id = request.args.get('resource_id', recursos[0].resource_id)  # Si no hay recurso seleccionado, tomar el primero de la lista

    return render_template('block_dates.html', recursos=recursos, selected_resource_id=int(selected_resource_id))

@main.route('/block_dates', methods=['GET', 'POST'])
def block_dates():
    selected_resource_ids = [1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 21, 22]  # IDs de los recursos que deseas mostrar
    recursos = Resource.query.filter(Resource.resource_id.in_(selected_resource_ids)).all()
    
    # Obtener el recurso seleccionado de los parámetros de la URL
    selected_resource_id = request.args.get('resource_id', recursos[0].resource_id)  # Si no hay recurso seleccionado, tomar el primero de la lista

    if request.method == 'POST':
        # Obtén la fecha bloqueada desde el formulario
        blocked_date = request.form.get('block_date', '')
        
        # Asegúrate de que se haya seleccionado una fecha
        if not blocked_date:
            flash('Por favor selecciona una fecha válida.', 'error')
            return redirect(url_for('main.block_dates'))
        
        # Convertir la fecha en un objeto datetime
        try:
            date_obj = datetime.strptime(blocked_date, '%Y-%m-%d')
        except ValueError:
            flash('Formato de fecha inválido.', 'error')
            return redirect(url_for('main.block_dates'))
        
        # Guarda la fecha bloqueada como una nueva cita con el status 5
        form_data = request.form
        save_blocked_dates_to_appointments([blocked_date], form_data)  # Pasar la fecha como cadena, no como objeto datetime
        
        flash('Día bloqueado guardado con éxito.')
        return redirect(url_for('main.block_dates'))
    
    # En el caso de una solicitud GET, renderiza la página de bloqueo de fechas
    return render_template('block_dates.html', recursos=recursos, selected_resource_id=int(selected_resource_id))