from flask import Flask, Blueprint, send_file, render_template, request
import pandas as pd
import io
from app.views.vistas import login_required
from app.controllers.controler import obtener_citas, obtenerCitasPorFecha
from datetime import datetime

main = Blueprint('excel', __name__)

@main.route('/reportes_excel')
@login_required
def reportes_excel():
    return render_template('reportes_excel.html')

@main.route('/download-excel')
@login_required
def download_excel():
    citas = obtener_citas()
    
    # Filtrar las citas para excluir aquellas con status_id == 5
    citas = [cita for cita in citas if cita.status_id != 5]
    
    # Convertir los datos en un formato adecuado para el DataFrame
    data = {
        'ID': [cita.cita_id for cita in citas],
        'Fecha Inicio': [cita.start.strftime('%Y-%m-%d %H:%M:%S') for cita in citas],
        'Fecha Fin': [cita.end.strftime('%Y-%m-%d %H:%M:%S') if cita.end else '' for cita in citas],
        'Título': [cita.title for cita in citas],
        'Descripción': [cita.description for cita in citas],
        'Tipo': [cita.type_label for cita in citas],
        'Estado': [
            'Reprogramada' if cita.status_id == 1 else
            'Asignada' if cita.status_id == 2 else
            'Cancelada' if cita.status_id == 3 else
            'Eliminada' if cita.status_id == 4 else
            'Desconocido'
            for cita in citas
        ],
        'Prioridad': [cita.prioridad for cita in citas],
        'Registro Llamada': [cita.registro_llamada for cita in citas],
        'Cual': [cita.cual for cita in citas],
        'Edad': [cita.edad for cita in citas],
        'Recurso ID': [cita.resource_id for cita in citas]
    }
    
    # Crear un DataFrame
    df = pd.DataFrame(data)
    
    # Guardar el DataFrame en un objeto en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    output.seek(0)

    # Enviar el archivo Excel para su descarga
    return send_file(output, as_attachment=True, download_name='datos.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@main.route('/reportes-fecha-excel')
@login_required
def reportes_fecha_excel():
    return render_template('excel_por_fechas.html')

@main.route('/Excel-by-dates', methods=['GET'])
@login_required
def excelByDates():
    try:
        # Obtener las fechas del formulario
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        # Verificar que las fechas no sean nulas
        if not start_date_str or not end_date_str:
            return "Fechas no proporcionadas", 400

        # Convertir las fechas de string a datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # Obtener las citas en el rango de fechas
        citas = obtenerCitasPorFecha(start_date, end_date)

        # Filtrar las citas para excluir aquellas con status_id == 5
        citas = [cita for cita in citas if cita.status_id != 5]

        # Convertir los datos en un formato adecuado para el DataFrame
        data = {
            'ID': [cita.cita_id for cita in citas],
            'Fecha Inicio': [cita.start.strftime('%Y-%m-%d %H:%M:%S') for cita in citas],
            'Fecha Fin': [cita.end.strftime('%Y-%m-%d %H:%M:%S') if cita.end else '' for cita in citas],
            'Título': [cita.title for cita in citas],
            'Descripción': [cita.description for cita in citas],
            'Tipo': [cita.type_label for cita in citas],
            'Estado': [
                'Reprogramada' if cita.status_id == 1 else
                'Asignada' if cita.status_id == 2 else
                'Cancelada' if cita.status_id == 3 else
                'Eliminada' if cita.status_id == 4 else
                'Desconocido'
                for cita in citas
            ],
            'Prioridad': [cita.prioridad for cita in citas],
            'Registro Llamada': [cita.registro_llamada for cita in citas],
            'Cual': [cita.cual for cita in citas],
            'Edad': [cita.edad for cita in citas],
            'Recurso ID': [cita.resource_id for cita in citas]
        }

        # Crear un DataFrame
        df = pd.DataFrame(data)

        # Guardar el DataFrame en un objeto en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        output.seek(0)

        # Enviar el archivo Excel para su descarga
        return send_file(output, as_attachment=True, download_name=f'citas_{start_date_str}_to_{end_date_str}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        return f"Error: {str(e)}", 500
