# app.py
from flask import Flask, request, jsonify
import os
import subprocess
import rutas

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    files = request.files.getlist('files')
    for file in files:
        if file and file.filename.endswith('.csv'):
            filename = file.filename
            file.save(os.path.join(rutas.ruta_carpeta_consumos, filename))
    return jsonify({'message': 'Archivos subidos correctamente'})

@app.route('/execute-script', methods=['GET'])
def execute_script():
    try:
        subprocess.run(['python', 'app.py'], check=True)
        return jsonify({'message': 'Script ejecutado correctamente'})
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Error al ejecutar el script', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
