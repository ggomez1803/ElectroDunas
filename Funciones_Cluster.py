import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib

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
