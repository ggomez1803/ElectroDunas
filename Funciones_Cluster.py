import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib
from scipy.spatial import distance
from scipy.stats import chi2
import matplotlib.pyplot as plt
import os

def normalizar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los datos de un DataFrame
    df: DataFrame con los datos a normalizar
    """
    # Inicializar el objeto StandardScaler
    scaler = StandardScaler()
    # Normalizar los datos
    df_norm = scaler.fit_transform(df)
    # Convertir los datos normalizados a un DataFrame
    df_norm = pd.DataFrame(df_norm, columns=df.columns)
    return df_norm

def clusterizar_consumos(df: pd.DataFrame, n_clusters: int) -> pd.DataFrame:
    """
    Agrupa a los clientes en clusters
    df: DataFrame con los datos de los clientes
    n_clusters: Número de clusters a formar
    """
    # Inicializar el modelo KMeans
    kmeans = KMeans(n_clusters=n_clusters)
    # Entrenar el modelo
    kmeans.fit(df)
    # Predecir los clusters
    clusters = kmeans.predict(df)
    # Agregar los clusters al DataFrame original
    df['Cluster'] = clusters
    return df, kmeans

def guardar_modelo_kmeans(cliente: int, kmeans: KMeans, ruta: str):
    """
    Guarda un modelo KMeans en un diccionario que contenga los modelos para cada cliente
    cliente: Número de cliente
    kmeans: Modelo KMeans a guardar
    ruta: Ruta del archivo donde se guardará el modelo
    """
    modelos_clientes = {}
    # Construir la ruta completa al archivo
    ruta_completa = ruta + 'kmeans_cliente_' + str(cliente) + '.pkl'
    # Agregar el modelo al diccionario
    modelos_clientes['Cliente ' + str(cliente)] = ruta_completa
    # Guardar el modelo en un archivo
    joblib.dump(kmeans, ruta_completa)
    return modelos_clientes

def clusterizacion_basado_distancias(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recibe un DataFrame, filtra los valores que no son anomalías y realiza una clusterización.
    df: DataFrame que se procesará
    """
    # Filtrar el dataframe para incluir solo los valores que no son anomalías y hacer una copia explícita
    df_no_anomalias = df[df['Anomalia'] == 0].copy()

    # Calcular la matriz de covarianza inversa
    cov_inv = np.linalg.inv(df_no_anomalias[['Factor_Potencia_%', 'Desequilibrio_Voltaje_%']].cov())

    # Calcular la distancia de Mahalanobis de cada punto al centroide (1, 0)
    df_no_anomalias['Distancia'] = df_no_anomalias.apply(lambda row: distance.mahalanobis([row['Factor_Potencia_%'], row['Desequilibrio_Voltaje_%']], [1, 0], cov_inv), axis=1)

    # Calcular el cuantil de la distribución chi cuadrado para un nivel de significancia de 0.01
    threshold = chi2.ppf((1 - 0.01), df=2)

    # Clasificar los puntos según su distancia de Mahalanobis
    df_no_anomalias['Anomalia'] = (df_no_anomalias['Distancia'] > np.sqrt(threshold)).astype(int)

    # Actualizar las filas del DataFrame original con los nuevos valores de 'Anomalia'
    df.update(df_no_anomalias)

    return df

def visualizar_anomalias(df: pd.DataFrame, agrupar_por: str):
    """
    Visualiza una matriz de gráficos de dispersión de la variable "Anomalia", uno para cada grupo en 'agrupar_por'.
    df: DataFrame que se procesará
    agrupar_por: Columna del DataFrame por la que se agruparán los datos ('Cliente' o 'Sector')
    """
    # Obtener la lista de grupos únicos
    grupos = df[agrupar_por].unique()

    # Para cada grupo
    for grupo in grupos:
        # Filtrar el DataFrame para este grupo
        df_grupo = df[df[agrupar_por] == grupo]

        # Crear una figura y un eje para el gráfico
        fig, ax = plt.subplots()

        # Crear un gráfico de dispersión para las anomalías y las no anomalías
        ax.scatter(df_grupo[df_grupo['Anomalia'] == 0]['Factor_Potencia_%'], df_grupo[df_grupo['Anomalia'] == 0]['Desequilibrio_Voltaje_%'], label='No Anomalía')
        ax.scatter(df_grupo[df_grupo['Anomalia'] == 1]['Factor_Potencia_%'], df_grupo[df_grupo['Anomalia'] == 1]['Desequilibrio_Voltaje_%'], label='Anomalía')

        # Configurar el gráfico
        ax.set_xlabel('Factor_Potencia_%')
        ax.set_ylabel('Desequilibrio_Voltaje_%')
        ax.set_title(f'Distribución de Anomalías para {agrupar_por} {grupo}')
        ax.legend()

        # Mostrar el gráfico
        plt.show()

def guardar_como_csv(df, nombre_archivo, ruta_exportacion):
    """
    Guarda un DataFrame en un archivo .csv en la ruta especificada
    df: DataFrame que se guardará
    nombre_archivo: Nombre del archivo .csv donde se guardará el DataFrame
    ruta_exportacion: Ruta donde se guardará el archivo .csv
    """
    # Unir la ruta de exportación y el nombre del archivo
    ruta_completa = os.path.join(ruta_exportacion, nombre_archivo)
    
    # Guardar el DataFrame en la ruta completa
    df.to_csv(ruta_completa, index=False)

