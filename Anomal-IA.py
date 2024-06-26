# backend.py
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import json
from app import procesar_y_clusterizar_datos

app = Flask(__name__)

# Ruta para servir la interfaz de usuario
@app.route('/')
def index():
    return render_template('interfaz.html')

# Ruta para subir archivos
@app.route('/upload', methods=['POST'])
def upload_files():
    # Obtener la ruta del archivo que está en la dirección ./_internal/config.json
    config_path = get_config_path()
    # Leer la configuración actual
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    ruta_carpeta_consumos = config['ruta_carpeta_consumos']
    
    # Asegúrate de que la carpeta existe
    os.makedirs(ruta_carpeta_consumos, exist_ok=True)
    
    files = request.files.getlist('files')
    for file in files:
        if file and file.filename.endswith('.csv'):
            filename = file.filename
            file.save(os.path.join(ruta_carpeta_consumos, filename))
    
    return jsonify({'message': 'Archivos subidos correctamente'})

# Ruta para ejecutar el script de Python
@app.route('/execute-script', methods=['GET'])
def execute_script():
    try:
        # Llama a la función que procesa y clusteriza los datos
        procesar_y_clusterizar_datos()
        return jsonify({'message': 'Script ejecutado correctamente'})
    except Exception as e:
        return jsonify({'message': 'Error al ejecutar el script', 'error': str(e)}), 500

def get_config_path():
    # Obtener la ruta del archivo que está en la dirección ./_internal/config.json
    base_path = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(base_path, 'config.json')
    return config_path

# Ruta para obtener la configuración actual
@app.route('/get-config', methods=['GET'])
def get_config():
    config_path = get_config_path()
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return jsonify(config)

# Función auxiliar para actualizar el archivo config.json
def update_config(config_key, new_path):
    #with open('_internal/config.json', 'r+') as config_file:
    config_path = get_config_path()
    with open(config_path, 'r+') as config_file:
        config = json.load(config_file)
        config[config_key] = new_path  # Actualiza la ruta específica
        config_file.seek(0)  # Vuelve al inicio del archivo
        json.dump(config, config_file, indent=4)
        config_file.truncate()  # Elimina el resto del archivo

# Ruta para actualizar la configuración de la ruta de carpeta de consumos
@app.route('/update-config/ruta_carpeta_consumos', methods=['POST'])
def update_ruta_carpeta_consumos():
    new_path = request.json.get('new_path')
    if not new_path:
        return jsonify({'message': 'No se proporcionó una nueva ruta'}), 400
    update_config('ruta_carpeta_consumos', new_path)
    return jsonify({'message': 'Configuración de ruta_carpeta_consumos actualizada correctamente'})

# Ruta para actualizar la configuración de la ruta de sector clientes
@app.route('/update-config/ruta_sector_clientes', methods=['POST'])
def update_ruta_sector_clientes():
    new_path = request.json.get('new_path')
    if not new_path:
        return jsonify({'message': 'No se proporcionó una nueva ruta'}), 400
    update_config('ruta_sector_clientes', new_path)
    return jsonify({'message': 'Configuración de ruta_sector_clientes actualizada correctamente'})

# Ruta para actualizar la configuración de la ruta de carpeta de exportación
@app.route('/update-config/ruta_carpeta_exportacion', methods=['POST'])
def update_ruta_carpeta_exportacion():
    new_path = request.json.get('new_path')
    if not new_path:
        return jsonify({'message': 'No se proporcionó una nueva ruta'}), 400
    update_config('ruta_carpeta_exportacion', new_path)
    return jsonify({'message': 'Configuración de ruta_carpeta_exportacion actualizada correctamente'})

# Ruta para servir archivos estáticos (si es necesario)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
