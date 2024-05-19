import rutas
import Funciones_Procesamiento as fp
import Funciones_Cluster as fc
import pandas as pd

# -------------------------- Procesar los datos --------------------------
# Leer los archivos de la carpeta 'datos'
dataframes = fp.leer_archivos(rutas.ruta_carpeta_consumos)

# Preprocesamos las dataframes
dataframes = fp.preprocesar_dataframes(dataframes)

# Agregamos la columna sector
ruta_archivo_sector = rutas.ruta_carpeta_consumos
dataframes = fp.agregar_sector(dataframes, ruta_archivo_sector)

# Agregar columna de fecha, FP y DV a cada DataFrame
dataframes = fp.agregar_col_fecha_lista(dataframes)
dataframes = fp.agregar_factor_potencia_lista(dataframes)
dataframes = fp.agregar_desequilibrio_voltaje_lista(dataframes)

#Unimos todos los dataframes
df_consolidada = fp.unir_dataframes(dataframes)

#Identificamos como outliers como anomalias (por sector)
df_consolidada_sin_outliers= fp.identificar_outliers(df_consolidada)

# -------------------------- Clusterizar los datos --------------------------
#Clusterizamos valores que no son outliers (por cliente)
df_consolidada_final = fc.clusterizacion_basado_distancias(df_consolidada_sin_outliers)

# -------------------------- Exportar los datos --------------------------
# Exportar el dataframe final a un archivo CSV
nombre_archivo = 'df_consolidada_final.csv'
ruta_exportacion = rutas.ruta_carpeta_exportacion
fc.guardar_como_csv(df_consolidada_final, nombre_archivo, ruta_exportacion)
