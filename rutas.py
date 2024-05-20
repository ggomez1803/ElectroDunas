# rutas.py
import json
import os

base_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(base_path, 'config.json')

# Función para cargar las rutas de configuración desde config.json
def cargar_rutas():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

# Cargar las rutas y asignarlas a variables
config_rutas = cargar_rutas()
ruta_carpeta_consumos = config_rutas['ruta_carpeta_consumos']
ruta_sector_clientes = config_rutas['ruta_sector_clientes']
ruta_carpeta_exportacion = config_rutas['ruta_carpeta_exportacion']
