import rutas
import Funciones_Procesamiento as fp
import Funciones_Cluster as fc
import pandas as pd

# -------------------------- Procesar los datos --------------------------
# Leer los archivos de la carpeta 'datos'
dataframes = fp.leer_archivos(rutas.ruta_carpeta_consumos)

# Agregar columna de fecha a cada DataFrame
for i, df in enumerate(dataframes):
    dataframes[i] = fp.agregar_col_fecha(df)
    dataframes[i] = fp.agregar_factor_potencia(df)
    dataframes[i] = fp.agregar_desequilibrio_voltaje(df)
    dataframes[i] = fp.identificar_outliers(df)

# Definición de columnas para el proceso de clustering
['Active_energy', 'Reactive_energy', 'Voltaje_FA', 'Horario_laboral', 'Dia_semana']
df_copies = [df.copy() for df in dataframes]
for i, df in enumerate(df_copies):
    df_copies[i] = df_copies[i][['Active_energy', 'Reactive_energy', 'Voltaje_FA', 'Horario_laboral', 'Dia_semana']]


# -------------------------- Clusterizar los datos --------------------------
# Normalizar los datos
df_norm = [fc.normalizar_datos(df) for df in df_copies]

# Clusterizar los datos
n_clusters = 2
df_clusterizados = []
modelos_kmeans = []
for df in df_norm:
    df_clusterizado, modelo_kmeans = fc.clusterizar_consumos(df, n_clusters)
    df_clusterizados.append(df_clusterizado)
    modelos_kmeans.append(modelo_kmeans)

# Guardar el modelo KMeans
ruta_modelo = rutas.ruta_carpeta_exportacion
modelos_clientes = {}
for i, modelo_kmeans in enumerate(modelos_kmeans):
    modelo_cliente = fc.guardar_modelo_kmeans(i+1, modelo_kmeans, ruta_modelo)
    modelos_clientes.update(modelo_cliente)

# Convertir diccionario en un dataframe de clientes y rutas de modelo
df_modelos = pd.DataFrame(list(modelos_clientes.items()), columns=['Cliente', 'Ruta_modelo'])

# -------------------------- Exportar los datos --------------------------
# Agregar el cluster de cada cliente a cada dataframe
for i, df in enumerate(dataframes):
    dataframes[i]['Cluster'] = df_clusterizados[i]['Cluster']

# Agrupar los dataframes en un solo dataframe
df_final = pd.concat(dataframes, ignore_index=True)

# Exportar el dataframe final a un archivo CSV
ruta_exportacion = rutas.ruta_carpeta_exportacion + 'consumos_clusterizados.csv'
df_final.to_csv(ruta_exportacion, index=False)
