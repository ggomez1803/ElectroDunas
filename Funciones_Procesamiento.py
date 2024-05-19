import pandas as pd
import numpy as np
import os
import datetime as dt
from sklearn.impute import KNNImputer

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

#Función que agrega el sector del cliente
def agregar_sector(dataframes, ruta_archivo_sector):
    """
    Agrega la columna 'Sector' a cada DataFrame en la lista
    dataframes: Lista de DataFrames
    ruta_archivo_sector: Ruta del archivo Excel que contiene los sectores
    """
    # Lee el archivo Excel
    df_sector = pd.read_excel(ruta_archivo_sector)

    # Cambia los nombres de las columnas
    nuevos_nombres = ['Cliente', 'Sector']  # Lista con los nuevos nombres
    df_sector.columns = nuevos_nombres

    # Ajusta la columna 'Cliente' para que coincida con los DataFrames
    df_sector['Cliente'] = df_sector['Cliente'].apply(lambda x: "Cliente " + str(x.split(' ')[1]))

    # Itera sobre cada DataFrame en la lista para agregar la columna sector
    for i, df in enumerate(dataframes):
        # Combina el DataFrame con df_sector basándose en la columna 'Cliente'
        df_combinado = pd.merge(df, df_sector, on='Cliente', how='left')

        # Actualiza el DataFrame en la lista
        dataframes[i] = df_combinado

    return dataframes

#Función que verifica que todas las bases de datos tengan el mismo número de columnas y el mismo formato de fecha, además de imputar los datos faltantes utilizando el método KNN.
def preprocesar_dataframes(dataframes):
    """
    Preprocesa una lista de DataFrames
    dataframes: Lista de DataFrames a preprocesar
    """
    # Verifica que todas las bases de datos tengan el mismo número de columnas
    columnas_primer_df = set(dataframes[0].columns)

    # Inicializa una lista para almacenar los nombres de los DataFrames que no coinciden
    dfs_no_coinciden = []

    # Verifica que todas las bases de datos tengan el mismo número de columnas
    for i, df in enumerate(dataframes):
        if set(df.columns) != columnas_primer_df:
            dfs_no_coinciden.append(i)

    # Imprime el resultado y lanza una excepción si las columnas no coinciden
    if not dfs_no_coinciden:
        print("Todas las DataFrames tienen las mismas columnas.")
    else:
        print(f"Las columnas de las siguientes DataFrames no coinciden con el primer DataFrame: {dfs_no_coinciden}")
        raise ValueError("Las columnas de las DataFrames no coinciden.")

    # Verifica que todas las observaciones en la columna de fechas tengan el mismo formato
    formato_fecha = "%Y-%m-%d %H:%M:%S"
    todas_las_fechas_coinciden = all(
        all(pd.to_datetime(df['Fecha'], format=formato_fecha, errors='coerce').notnull())
        for df in dataframes
    )

    # Imprime el resultado
    if todas_las_fechas_coinciden:
        print("Todas las observaciones en la columna de fechas tienen el mismo formato.")
    else:
        print("NO todas las observaciones en la columna de fechas tienen el mismo formato. Se inicia proceso de transformación al formato ideal.")
        # Itera sobre cada DataFrame en la lista
        for i, df in enumerate(dataframes):
            try:
                # Intenta convertir las fechas al formato especificado
                df['Fecha'] = pd.to_datetime(df['Fecha'], format=formato_fecha)
            except ValueError as e:
                print(f"Error al convertir las fechas en el DataFrame {i}: {e}")
                # Aquí puedes manejar el error como prefieras
                # Por ejemplo, podrías reemplazar las fechas no válidas con NaT
                df['Fecha'] = pd.to_datetime(df['Fecha'], format=formato_fecha, errors='coerce')

            # Actualiza el DataFrame en la lista
            dataframes[i] = df
    
    # Verifica que todas las bases de datos no tengan datos faltantes
    # Inicializa un contador para los datos faltantes
    contador_datos_faltantes = 0

    # Itera sobre cada DataFrame en la lista
    for i, df in enumerate(dataframes):
        # Cuenta los datos faltantes en el DataFrame actual
        datos_faltantes = df.isnull().sum().sum()

        # Si hay datos faltantes, los imputa
        if datos_faltantes > 0:
            # Agrega al contador
            contador_datos_faltantes += datos_faltantes

            # Separa la columna 'Fecha'
            fechas = df['Fecha']
            df = df.drop(columns='Fecha')

            # Crea el imputador KNN
            imputador = KNNImputer(n_neighbors=3)

            # Imputa los datos faltantes con el imputador KNN
            df_imputado = imputador.fit_transform(df)

            # Convierte el resultado (que es un array de numpy) de nuevo a un DataFrame
            df = pd.DataFrame(df_imputado, columns=df.columns)

            # Vuelve a añadir la columna 'Fecha'
            df['Fecha'] = fechas

        # Actualiza el DataFrame en la lista
        dataframes[i] = df

    # Imprime el número total de datos faltantes que se tuvieron que cambiar
    if contador_datos_faltantes > 0:
        print(f"Se tuvieron que cambiar {contador_datos_faltantes} datos faltantes.")
    else:
        print("No se encontraron datos faltantes.")

    return dataframes

def agregar_col_fecha_lista(dataframes: list) -> list:
    """
    Agrega una columna con la fecha a cada DataFrame en la lista
    dataframes: Lista de DataFrames
    """
    # Itera sobre cada DataFrame en la lista
    for i in range(len(dataframes)):
        df = dataframes[i]
        
        # Dar formato de fecha a la columna de fecha
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d %H:%M:%S')
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
        
        # Actualiza el DataFrame en la lista
        dataframes[i] = df

    return dataframes

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

def agregar_factor_potencia_lista(dataframes: list) -> list:
    """
    Agrega una columna con el factor de potencia a cada DataFrame en la lista
    dataframes: Lista de DataFrames
    """
    # Itera sobre cada DataFrame en la lista
    for i in range(len(dataframes)):
        dataframes[i] = agregar_factor_potencia(dataframes[i])
    return dataframes

def agregar_desequilibrio_voltaje_lista(dataframes: list) -> list:
    """
    Agrega una columna con el desequilibrio de voltaje a cada DataFrame en la lista
    dataframes: Lista de DataFrames
    """
    # Itera sobre cada DataFrame en la lista
    for i in range(len(dataframes)):
        dataframes[i] = agregar_desequilibrio_voltaje(dataframes[i])
    return dataframes

#Función para unir todos los dataframes
def unir_dataframes(dataframes: list) -> pd.DataFrame:
    """
    Une todas las DataFrames en la lista en una sola DataFrame
    dataframes: Lista de DataFrames
    """
    # Une todas las DataFrames
    df_consolidada = pd.concat(dataframes, ignore_index=True)

    return df_consolidada


def identificar_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica los datos atípicos en un DataFrame por cada sector
    df: DataFrame al que se le identificarán los datos atípicos
    """
    # Función para identificar outliers en un grupo
    def identificar_outliers_grupo(grupo):
        # Calcular el rango intercuartílico para el factor de potencia
        Q1_FP = grupo['Factor_Potencia_%'].quantile(0.25)
        Q3_FP = grupo['Factor_Potencia_%'].quantile(0.75)
        IQR_FP = Q3_FP - Q1_FP

        # Calcular el rango intercuartílico para el 'Desequilibrio_Voltaje_%'
        Q1_DV = grupo['Desequilibrio_Voltaje_%'].quantile(0.25)
        Q3_DV = grupo['Desequilibrio_Voltaje_%'].quantile(0.75)
        IQR_DV = Q3_DV - Q1_DV

        # Identificar los outliers en 'Factor_Potencia_%' y 'Desequilibrio_Voltaje_%'
        grupo['Anomalia'] = (
            (grupo['Factor_Potencia_%'] < (Q1_FP - 1.5 * IQR_FP)) | 
            (grupo['Factor_Potencia_%'] > (Q3_FP + 1.5 * IQR_FP)) |
            (grupo['Desequilibrio_Voltaje_%'] < (Q1_DV - 1.5 * IQR_DV)) | 
            (grupo['Desequilibrio_Voltaje_%'] > (Q3_DV + 1.5 * IQR_DV))
        ).astype(int)
        
        return grupo

    # Aplica la función a cada grupo de sector
    df = df.groupby('Sector').apply(identificar_outliers_grupo)

    return df

