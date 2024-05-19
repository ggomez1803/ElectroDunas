import pandas as pd
import numpy as np
import os
import datetime as dt

# Funciones de procesamiento
def leer_archivos(ruta_carpeta: str) -> list:
    """
    Lee todos los archivos de una carpeta y los guarda en un diccionario
    ruta_carpeta: Ruta de la carpeta que contiene los archivos CSV
    """
    # Lista para almacenar los DataFrames
    dataframes = []

    # Iterar sobre cada archivo en la carpeta
    for archivo in os.listdir(ruta_carpeta):
        # Verificar si el archivo es un archivo CSV
        if archivo.endswith('.csv'):
            # Construir la ruta completa al archivo
            ruta_completa = os.path.join(ruta_carpeta, archivo)
            # Extraer el nombre del archivo sin la extensión para usar el nombre del cliente en la tabla
            nombre_cliente = archivo.replace('.csv', '')
            # Remover "DATOS" del nombre del cliente
            nombre_cliente = nombre_cliente.replace('DATOS', '')
            # Separar "CLIENTE" del numero de cliente
            nombre_cliente = nombre_cliente.replace('CLIENTE', 'CLIENTE ')
            # Escribir la primera letra en mayúscula
            nombre_cliente = nombre_cliente.title()
            # Leer el archivo CSV en un DataFrame y agregarlo a la lista
            df = pd.read_csv(ruta_completa)
            # Agregar una columna con el nombre del cliente
            df['Cliente'] = nombre_cliente
            dataframes.append(df)

    return dataframes

# Función que agrega la columna fecha a un DataFrame
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
    df['Dia_semana'] = df['Fecha'].apply(lambda x: dt.datetime.strptime(x, '%m/%d/%Y').weekday())
    
    return df

# Función que agrega las columnas Potencia Aparente y Factor de Potencia al dataframe
def agregar_factor_potencia(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega una columna con el factor de potencia a un DataFrame
    df: DataFrame al que se le agregará la columna de factor de potencia
    """
    # Calcular el factor de potencia
    df['Potencia_Aparente'] = np.sqrt(df['Active_energy']**2 + df['Reactive_energy']**2)
    df['Factor_Potencia_%'] = (df['Active_energy'] / (df['Potencia_Aparente'] + 1e-10))
    
    return df

# Función que agrega las columnas Desequilibrio Voltaje y Desequilibrio Voltaje porcentual al dataframe
def agregar_desequilibrio_voltaje(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega una columna con el desequilibrio de voltaje a un DataFrame
    df: DataFrame al que se le agregará la columna de desequilibrio de voltaje
    """
    # Calcular el desequilibrio de voltaje
    df['Desequilibrio_Voltaje'] = abs(df['Voltaje_FA'] - df['Voltaje_FC'])
    df['Desequilibrio_Voltaje_%'] = (df['Desequilibrio_Voltaje'] / (df[['Voltaje_FA', 'Voltaje_FC']].min(axis=1) + 1e-10))
    
    return df

# Función para remover los datos atípicos del dataframe
def identificar_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remueve los datos atípicos de un DataFrame
    df: DataFrame al que se le removerán los datos atípicos
    """
    # Calcular el rango intercuartílico para el factor de potencia
    Q1 = df['Factor_Potencia_%'].quantile(0.25)
    Q3 = df['Factor_Potencia_%'].quantile(0.75)
    IQR = Q3 - Q1
    # Identificar los outliers en 'Factor_Potencia_%'
    df['Anomalia_FP'] = ((df['Factor_Potencia_%'] < (Q1 - 1.5 * IQR)) | (df['Factor_Potencia_%'] > (Q3 + 1.5 * IQR))).astype(np.int)

    # Calcular el rango intercuartílico para el 'Desequilibrio_Voltaje_%'
    Q1 = df['Desequilibrio_Voltaje_%'].quantile(0.25)
    Q3 = df['Desequilibrio_Voltaje_%'].quantile(0.75)
    IQR = Q3 - Q1

    # Identificar los outliers en 'Desequilibrio_Voltaje_%'
    df['Anomalias_Voltaje'] = ((df['Desequilibrio_Voltaje_%'] < (Q1 - 1.5 * IQR)) | (df['Desequilibrio_Voltaje_%'] > (Q3 + 1.5 * IQR))).astype(np.int)
    
    return df