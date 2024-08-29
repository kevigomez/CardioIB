from flask import Flask, Blueprint, send_file, render_template
import pandas as pd
import io
from app.views.vistas import login_required
from app.controllers.controler import obtener_citas

main = Blueprint('excel', __name__)

@main.route('/reportes_excel')
@login_required
def reportes_excel():
    return render_template('reportes_excel.html')

@main.route('/download-excel')
@login_required
def download_excel():
    citas = obtener_citas()
    
    # Convertir los datos en un formato adecuado para el DataFrame
    data = {
        'ID': [cita.cita_id for cita in citas],
        'Fecha Inicio': [cita.start.strftime('%Y-%m-%d %H:%M:%S') for cita in citas],
        'Fecha Fin': [cita.end.strftime('%Y-%m-%d %H:%M:%S') if cita.end else '' for cita in citas],
        'Título': [cita.title for cita in citas],
        'Descripción': [cita.description for cita in citas],
        'Tipo': [cita.type_label for cita in citas],
        'Estado': [cita.status_id for cita in citas],
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

