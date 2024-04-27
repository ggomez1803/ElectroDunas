import pandas as pd
import os
import datetime as dt

# Funciones de procesamiento
def leer_archivos(ruta_carpeta: str) -> list:
    """
    Lee todos los archivos de una carpeta y los guarda en un diccionario
    ruta_carpeta: Ruta de la carpeta que contiene los archivos CSV
    """
    dataframes = []
    # Iterar sobre cada archivo en la carpeta
    for archivo in os.listdir(ruta_carpeta):
        # Verificar si el archivo es un archivo CSV
        if archivo.endswith('.csv'):
            # Construir la ruta completa al archivo
            ruta_completa = os.path.join(ruta_carpeta, archivo)
            # Leer el archivo CSV en un DataFrame y agregarlo a la lista
            df = pd.read_csv(ruta_completa)
            # Agregar el DataFrame a la lista
            dataframes.append(df)
    return dataframes

def agregar_col_cliente(df: pd.DataFrame, cliente: int) -> pd.DataFrame:
    """
    Agrega una columna con el número de cliente a un DataFrame
    df: DataFrame al que se le agregará la columna de cliente
    cliente: Número de cliente a agregar
    """
    df['Cliente'] = 'Cliente ' + str(cliente)
    return df

def agregar_col_fecha(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega una columna con la fecha a un DataFrame y la convierte a formato de fecha
    df: DataFrame al que se le agregará la columna de fecha
    """
    # Dar formato de fecha a la columna de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    # Crear una columna de mes
    df['Mes'] = df['Fecha'].dt.month
    # Crear una columna de año
    df['Año'] = df['Fecha'].dt.year
    # Crear una columna de día
    df['Dia'] = df['Fecha'].dt.day
    # Crear columna de hora
    df['Hora'] = df['Fecha'].dt.hour
    # Crear una columna de nombre del día
    df['Nombre_dia'] = df['Fecha'].dt.day_name()
    # Cambiar el formato de la fecha
    df['Fecha'] = df['Fecha'].dt.strftime('%d/%m/%Y')
    # Crear columna para fin de semana
    df['Fin_de_semana'] = df['Nombre_dia'].apply(lambda x: 1 if x in ['Saturday', 'Sunday'] else 0)
    # Crear columna para horario laboral. 1 para turno 1 y 2 para turno 2
    df['Horario_laboral'] = df['Hora'].apply(lambda x: 1 if x in range(8, 19) else 0)
    # Crear columna para día de la semana
    df['Dia_semana'] = df['Fecha'].apply(lambda x: dt.datetime.strptime(x, '%d/%m/%Y').weekday())
    
    return df