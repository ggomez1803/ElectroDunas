## Anomal-IA, herramienta para detección de anomalías para ElectroDunas

Yolanda Franco
Daniel Rozo
José Hoyos
Gabriel Gómez

Este proyecto trata sobre la identificación de anomalías en el consumo de energía eléctrica para diferentes clientes de ElectroDunas.

### Tratamiento previo de los datos: 
#### Rutina de carga de información: 
En una primera etapa del proceso, se estableció una estructura de almacenamiento inicial para los datos de los clientes, a través de la creación de una carpeta designada. Esta carpeta sirve como un repositorio provisional donde se alojarán los archivos .csv que contienen información relevante sobre los consumos y comportamientos de los clientes. Se anticipa que este método de almacenamiento será reemplazado por un repositorio más sofisticado y dinámico en el futuro, especialmente si se logra acceder a los datos de los clientes en tiempo real. 
 
Los datos de los clientes se organizaron y manipularon utilizando el lenguaje de programación Python, aprovechando la potencia de las bibliotecas especializadas como Pandas. La información se cargó en memoria como una serie de dataframes (DF). Cada DF corresponde a un archivo .csv individual, representando los datos asociados a un cliente específico. Además de la información de consumo, se enriqueció cada DF agregando una columna que identifica el sector económico al que pertenece el cliente correspondiente. 
 
Así, se procedió a unir la información proporcionada por la empresa sobre los sectores económicos de los clientes. Esto se realizó mediante la incorporación de un archivo externo en formato Excel que contiene la clasificación de los clientes según sus respectivos sectores económicos. Se realizaron ajustes pertinentes en los nombres de las columnas y en el formato de los datos para asegurar una integración sin fisuras entre los datos de los clientes y la información sobre sus sectores económicos. 
 
#### Descriptivos: 
Para analizar la información proporcionada por el cliente, llevamos a cabo varios análisis descriptivos. Realizamos una evaluación gráfica para examinar los patrones de comportamiento mensual de los clientes en cada sector. Sin embargo, debido a las limitaciones de espacio en este documento, nuestro análisis descriptivo se centrará en una visión global de los datos. El objetivo de este análisis es identificar patrones de consumo y familiarizarnos con la información proporcionada. 

En un primer análisis, vamos a evaluar la correlación de las variables Energía Activa, Reactiva y Voltaje FA y FC. Esto nos permite comprender las relaciones entre diferentes variables en un conjunto de datos, facilitando tanto la reducción de la dimensionalidad como la identificación de anomalías. Por ejemplo, si dos variables suelen estar altamente correlacionadas y observamos un punto donde una variable se desvía significativamente de esta relación habitual, esto podría indicar la presencia de una anomalía.  

La correlación entre las variables Voltaje_FA y Voltaje_FC es fuerte (0.95), lo que indica que suelen moverse juntas. Un punto donde una de estas variables se desvía significativamente de esta tendencia podría indicar una anomalía. Por otro lado, la correlación moderada (0.64) entre la energía activa y la energía reactiva sugiere una relación positiva menos fuerte. Aun así, un punto donde la energía activa es alta pero la energía reactiva es baja (o viceversa) podría ser un indicador de anomalía (imagen 1). 

![Imagen 1](https://github.com/ggomez1803/ElectroDunas/assets/10146054/8439316a-b445-4839-ba6b-f3bd9000a405)<br>
Imagen 1. Matriz de correlación de variables Energía Activa – Reactiva y Voltaje FA y FC 
 
Para obtener una visión general de la distribución de los datos y tener alguna noción sobre las anomalías, se generaron gráficos de boxplot. A partir de este análisis, se concluye que hay una gran heterogeneidad y datos anómalos en los patrones de consumo de energía eléctrica. Además, se observan anomalías en los datos de voltaje, aunque estas son menos frecuentes en comparación con el par energético. 

 ![Imagen 2](https://github.com/ggomez1803/ElectroDunas/assets/10146054/190b1907-fb06-4a71-9bb8-5f598e702f1b)<br>
Imagen 2. Boxplots por cliente y sector económico 
Después de investigar y consultar expertos en la materia, experimentamos con dos conceptos que no solo definirían nuestro rumbo a seguir en la detección de anomalías en nuestro sistema, sino que también nos ayudarían a reducir la dimensionalidad a solo 2 variables, explicando las 4 dadas. El factor de potencia (FP), es una medida de eficiencia en la trasferencia de energía eléctrica, se define como la relación entre la energía activa y la potencia aparente. La energía activa, como sabemos, es la que se consume realmente al realizar algún trabajo útil, como encender una bombilla. La potencia aparente, un término nuevo para el experimento, se puede entender como la potencia total que fluye en un circuito incluyendo energía activa y reactiva. Esta la definiremos en la siguiente fórmula: 

$\ S = √{Pˆ2} + Qˆ2$
 
Donde: <br>
- S es la potencia aparente
- P es la energía activa.
- Q es la energía reactiva. 
 
Teniendo clara esta medición, el FP se calcula dividiendo la energía activa (P) por la potencia aparente (S). La definiremos en la siguiente fórmula: 

$\ FP = P/S$

Donde: <br>
- P es la energía activa.
- S es la potencia aparente. 
 
El factor de potencia (FP) debe ser un valor entre 0 y 1. Idealmente, cuando este valor se aproxima a 1, indica que la energía se está utilizando de manera eficiente. Esto nos lleva a un supuesto importante: un sistema eficiente debería tener un factor de potencia cercano a este valor. Si el factor de potencia se aleja significativamente de 1, podría indicar una anomalía. Esto se debe a que un factor de potencia bajo sugiere que una cantidad significativa de energía se está perdiendo durante el proceso de transferencia de energía. 

Por otro lado, cuando consideramos las dos variables Voltaje_FA y Voltaje_FC, podemos inferir que estamos tratando con un sistema trifásico (ST). Un ST es un sistema de producción, distribución y consumo de energía eléctrica que utiliza tres corrientes monofásicas. En un sistema trifásico equilibrado, los voltajes FA, FB y FC deberían tener magnitudes iguales y estar desfasados simétricamente. Si este equilibrio no se mantiene, podemos inferir que el sistema de tensiones está desequilibrado.1 

Considerando que sólo disponemos de los voltajes FA y FC, empleamos una fórmula que proporciona una medida normalizada del principio de desequilibrio. Esta fórmula consiste en dividir la diferencia absoluta entre los voltajes FA y FC por el voltaje más pequeño. De esta manera, obtenemos una medida de desequilibrio que es independiente de la magnitud de los voltajes. Este enfoque es especialmente útil para identificar anomalías dado que, en un sistema trifásico equilibrado, los tres voltajes deberían ser iguales. Por lo tanto, cualquier desviación significativa de esta igualdad podría indicar un problema o anomalía en el sistema. 

$\ 𝐷𝑉= (∣𝑉𝐹𝐴−𝑉𝐹𝐶∣)/min(𝑉𝐹𝐴,  𝑉𝐹𝐶)$

 
Donde: <br>
- DV es el desequilibrio de voltaje normalizado.
- 𝑉𝐹𝐴 es la variable Voltaje_FA.
- 𝑉𝐹𝐶 es la variable Voltaje_FC. 
 
La obtención del factor de potencia (FP) y el desequilibrio de voltaje (DV) nos proporciona dos variables normalizadas que nos permiten explicar tanto las energías como los voltajes en nuestro experimento de manera eficiente. 
 
En la imagen 3, se muestran las correlaciones obtenidas para las diferentes variables disponibles. Con relación a nuestras nuevas variables, observamos una correlación positiva entre el factor de potencia (FP) y la energía activa, lo que podría indicar que las anomalías están asociadas con una eficiencia energética reducida. De manera similar, las correlaciones negativas entre el desequilibrio de voltaje y los voltajes FA y FC podrían indicar que las anomalías están asociadas con un sistema desequilibrado. 

 ![Imagen 3](https://github.com/ggomez1803/ElectroDunas/assets/10146054/4d40c53a-7da9-4c91-8467-cbb246683813)<br>
Imagen 3. Matriz de correlación con las variables FP y DV. 

### Preprocesamiento: 
A cada uno de los dataframes (DF) pertenecientes a la lista creada previamente con la información de los clientes se agregaron las columnas de Factor Potencia (FP), Potencia Aparente (S) y Desequilibrio de voltaje (DV). De igual manera, se agregó la columna de fecha, se validó que no hubiera datos faltantes, que todos los DFs tuvieran el mismo número de columnas y por último que la fecha estuviera en el mismo formato. Al final se consolidó todo en una DF global. Ver imagen 4. 

 ![Imagen 4](https://github.com/ggomez1803/ElectroDunas/assets/10146054/cec90ae0-460f-4bbf-9594-69b64752c7d8)<br>
Imagen 4. Código preprocesamiento. 
 
Al evaluar el Factor de Potencia (FP) y el Desequilibrio de Voltaje (DV) en una distribución de frecuencias (imagen 6), observamos que los datos tienden a concentrarse en valores con FP = 1 y DV = 0. Sin embargo, en la gráfica del FP, se observan datos anómalos, como valores negativos, y en el DV, datos extremos que alcanzan hasta 60,000. Para el tratamiento de estos valores atípicos, los mejores resultados se obtuvieron a través del Rango Intercuartil, considerando como atípicas las observaciones que se encuentran por encima de 1.5+Q3 o debajo Q1-1.5 veces este valor (imagen 5). También se probó la métrica Z-Score para tratar outliers, pero no proporcionó los resultados esperados. Como se mencionó anteriormente, no era conveniente imputar esta información al principio debido a la naturaleza del experimento de encontrar datos anómalos; sin embargo, dados los resultados, se tomó la decisión de clasificar automáticamente como anomalías los outliers encontrados antes de proceder con los modelos de supervisados de clusterización. 

 ![Imagen 5](https://github.com/ggomez1803/ElectroDunas/assets/10146054/50783803-a71a-4fb0-9cf8-2e0274754221)<br>
Imagen 5. Código para tratar outliers usando IQR por sector. 


![Imagen 6](https://github.com/ggomez1803/ElectroDunas/assets/10146054/86d9bd3a-f538-49ac-b39b-e403bfef1729)<br>
Imagen 6. Distribución de frecuencias Factor de potencia y desequilibrio de voltaje de toda la muestra. 
 
El tratamiento de los outliers se llevó a cabo considerando el sector al que pertenece cada cliente. Esta consideración es relevante ya que puede proporcionar una medida significativa para identificar valores extremos dentro del entorno en el que opera cada cliente. Tras este tratamiento, la distribución de los datos mostró una notable mejora para estas variables, presentando magnitudes con un mayor sentido técnico. Los detalles se pueden observar en la siguiente imagen (Imagen 7): 

![Imagen 7](https://github.com/ggomez1803/ElectroDunas/assets/10146054/0f129ffa-d451-469f-ac95-6f2fca5ba390)<br>
Imagen 7. Distribución de frecuencias de FP y DV sin outliers. 

Para preparar los datos para un análisis de clustering subsiguiente, hemos seleccionado las columnas de interés específicas: el Factor de Potencia (FP) y el Desequilibrio de Voltaje (DV). Es importante recordar nuestra hipótesis de que los datos que se desvían significativamente de un FP igual a 1 y un DV igual a 0 tienen una mayor probabilidad de ser considerados anomalías. 
 
#### Entrenamiento de los modelos: 
El objetivo principal de esta etapa del proyecto es explorar y evaluar diversos algoritmos de clustering para segmentar los datos de consumo de energía de los clientes en dos grupos distintos: consumos normales y consumos atípicos. Dado que el proyecto se enfoca en el análisis no supervisado, no se busca una calibración específica de los modelos, sino más bien una evaluación exhaustiva de su desempeño utilizando métricas adecuadas. 
Inicialmente se consideraron varios algoritmos de clustering, entre ellos, K-Means, Birch y Spectral Clustering, cada uno con sus propias características y supuestos subyacentes sobre la estructura de los datos. Sin embargo, basándonos en el supuesto que un sistema eléctrico óptimo tiende a que el factor de potencia (FP) sea 1 y el desequilibrio de voltaje (DV) sea 0, decidimos recurrir a probar modelos donde pudiéramos definir desde un principio el centroide óptimo (1,0).  
Inicialmente, nos centramos en el algoritmo K-Means (KM). Este algoritmo presenta la ventaja de permitirnos definir nuestro propio centroide, además de ser fácil de implementar y eficiente en términos computacionales. No obstante, dada su naturaleza iterativa del proceso de minimización de distancias, no hay garantía que los centroides permanezcan en la posición óptima que buscamos. Es decir, los centroides inicializados en (1, 0) con KM pueden desplazarse durante la ejecución del algoritmo. Tras evaluar estas limitaciones, decidimos también explorar una estrategia alternativa basada en la clasificación por distancia o umbrales. 
En la metodología que empleamos basada en modelos con umbrales, calculamos la distancia euclidiana de cada punto al centroide (1, 0). Luego, clasificamos los puntos en dos grupos dependiendo de si su distancia es mayor o menor que la mediana de todas las distancias. Además, implementamos un enfoque complementario que utiliza la distancia de Mahalanobis. Este enfoque tiene en cuenta la correlación entre las variables y la variabilidad de cada una. Basándonos en un umbral derivado del cuantil de la distribución chi-cuadrado con un nivel de significancia del 0.01, clasificamos los puntos como anomalías o normales. Esto nos proporciona un 99% de confianza en la precisión de la clasificación. 
Durante el proceso de evaluación, utilizamos tres métricas de desempeño ampliamente reconocidas en el ámbito del clustering: Silhouette score, Davies Bouldin y Calinski Harabasz. Estas métricas proporcionan información valiosa sobre la calidad y la coherencia de los grupos generados por los algoritmos de clustering. Sin embargo, dada la naturaleza de nuestro experimento de encontrar anomalías, decidimos emplear métricas complementarias como la densidad, número de datos y varianza, los cuales se profundizarán en la sección de análisis de resultados. 
Por ejemplo, el Silhouette score, el índice de Davies-Bouldin y el índice de Calinski-Harabasz nos ayudan a medir la cohesión y separación de los clusters, así como la dispersión dentro y entre ellos. En cuanto a la detección de anomalías, consideramos la densidad de datos, el número de datos y la varianza dentro de un agrupamiento. Un cluster con una densidad de datos baja, un número de datos atípico o una alta varianza puede indicar la presencia de anomalías. 
Dado que el proyecto tiene como objetivo final la identificación de dos segmentos principales, es decir, consumos normales y consumos atípicos, se ha establecido un número de clusters igual a 2 en las pruebas iniciales. Esto simplifica la tarea de evaluación, ya que nos permite comparar directamente la capacidad de cada algoritmo para distinguir estos dos grupos fundamentales. 
 
De esta forma, filtramos el dataframe para incluir solo los valores que no son outliers y basamos el modelo en las columnas de interés: ‘Factor_Potencia_%’ y ‘Desequilibrio_Voltaje_%’. Recordemos que estas 2 variables ya están estandarizadas. Posteriormente, inicializamos el algoritmo K-Means con dos clusters y centroides específicos. Ajustamos el algoritmo K-Means al nuevo dataframe y agregamos las etiquetas de los clusters al dataframe original. En resumen, este código realiza una agrupación K-Means en un conjunto de datos, excluyendo los outliers (imagen 8). 
 
 ![Imagen 8](https://github.com/ggomez1803/ElectroDunas/assets/10146054/921394aa-ba3f-41df-8814-c49f6b7792bc)<br>
Imagen 8. Entrenamiento del modelo K-Means. 
 
 
Para el modelo basado en distancia o umbrales, primero filtramos el dataframe para incluir solo los valores que no son outliers, basándonos en las columnas ‘Anomalia_FP’ y ‘Anomalias_Voltaje’. Luego, calculamos la matriz de covarianza inversa de las columnas ‘Factor_Potencia_%’ y ‘Desequilibrio_Voltaje_%’. A continuación, calculamos la distancia de Mahalanobis de cada punto al centroide (1, 0) y la almacenamos en una nueva columna llamada ‘Distancia’. Posteriormente, calculamos el cuantil de la distribución chi cuadrado para un nivel de significancia de 0.01, que usamos como umbral para clasificar los puntos según su distancia de Mahalanobis. Finalmente, los puntos cuya distancia supera la raíz cuadrada del umbral se clasifican como anomalías pertenecientes al cluster 1, mientras que los demás se clasifican como pertenecientes al cluster 0 (imagen 9). 
 
 ![Imagen 9](https://github.com/ggomez1803/ElectroDunas/assets/10146054/5e60ae90-47c5-4582-8655-c710b9e3d187)<br>
Imagen 9. Entrenamiento del modelo basado en umbrales usando distancia de Mahalanobis. 
La distancia de Mahalanobis es preferible en situaciones donde las variables no son independientes o tienen diferentes variabilidades. A diferencia de la distancia euclidiana, que puede inflar las distancias en presencia de alta correlación entre variables, la distancia de Mahalanobis proporciona una medida más precisa al tener en cuenta estas correlaciones. Además, es invariante a las transformaciones lineales de los datos, lo que la hace robusta frente a diferencias en la escala de las variables. Este enfoque es especialmente útil para identificar outliers en conjuntos de datos multivariados, asegurando una detección más confiable de anomalías en el consumo de energía eléctrica. 
 
### Análisis de resultados: 
#### Métricas de desempeño de los modelos: 
Para evaluar los modelos de clustering, inicialmente realizamos una comparación entre el Silhouette Score, Davies Bouldin y Calinski Harabaz para los modelos k-Means (KM) y basados en umbrales, considerando cada cliente individualmente. Este tipo de clusterización nos permite definir un centroide óptimo, que en este caso corresponde a un factor de potencia de 1 y un desequilibrio de 0. Basados en estos resultados, el modelo KM superó a los modelos basados en umbrales, con la excepción del Silhouette Score, donde fue ligeramente inferior. 

| **Metric**              | **k-Means**        | **Clustering por umbrales**                     |
| ----------------------- | ------------------ | ----------------------------------------------- |
| Silhouette Score        |             0.5578 |                                          0.5625 |
| Davies-Bouldin Score    |             0.7273 |                                          1.3404 |
| Calinski-Harabasz Score |    400,465.67      |                                135,249.63       |

Tabla 1. Comparación métricas modelo K-Means y basado en umbrales. 
 
No obstante, dado que nuestro objetivo es identificar anomalías, decidimos evaluar también la densidad, el número de datos y la varianza de cada cluster en ambos modelos. Evaluamos la densidad para entender cuán dispersos o compactos son los puntos dentro de cada agrupamiento. El número de datos nos da una idea del tamaño del cluster. En condiciones normales, el conjunto de anomalías tiende a ser más pequeño, ya que las anomalías no son tan frecuentes. La varianza nos proporciona una medida de cuánto varían los puntos dentro de cada cluster. Dado que las anomalías suelen ser puntos que se apartan de la norma, esperaríamos que el agrupamiento de anomalías presente una mayor varianza. 

**Modelo K-Means**
| **métrica**  | **Normal**             | **Anomalía**                                       |
| ------------ | ---------------------- | -------------------------------------------------- |
| Densidad     |                   0.13 |                                               0.19 |
| Número datos |    327,418.00          |                                   63,911.00        |
| Varianza     |                   0.01 |                                               0.03 |

**Modelo Basado en Umbrales**
| **métrica**  | **Normal**             | **Anomalía**                                       |
| ------------ | ---------------------- | -------------------------------------------------- |
| Densidad     |                   0.14 |                                               0.37 |
| Número datos |    350,937.00          |                                   40,392.00        |
| Varianza     |                   0.01 |                                               0.08 |


Tablas 2 y 3. Comparación métricas modelo K-Means y basado en umbrales. 

Basados en los resultados de las anteriores tablas, observamos que el método basado en umbrales parece tener una mayor sensibilidad en la detección de anomalías. Este enfoque mostró el conjunto que está más disperso (mayor densidad y varianza) y tiene menor número de datos en comparación con k-Means. 

Esto sugiere que cuando los clusters tienen alta varianza, las métricas de Silhouette, Davies Bouldin y Calinski Harabaz podrían no ser suficientes para evaluar la calidad del clustering, ya que estas métricas se centran en la cohesión de los datos. Por lo tanto, es importante considerar también otras métricas que reflejen la dispersión de los datos al evaluar modelos de clustering para la detección de anomalías. 

Al visualizar la clusterización K-Means de la imagen 10 y comparar los clusters con el factor de potencia (FP) en el eje x y el desequilibrio de voltaje (DV) en el eje y, podemos validar nuestras hipótesis. Recordemos que nuestro punto óptimo, es tener una eficiencia de 1 en el FP y un desequilibrio 0 en el DV, es decir, los datos en condiciones ideales deberían estar concentrados en la zona inferior derecha de la imagen 10. En esta imagen, correspondiente al Cliente 22 con K-means, que lo escogimos de ejemplo por su gran variabilidad, se observa un cluster (amarillo) de anomalías claramente definido, donde se consideran anomalías los valores con un factor de potencia (FP) inferior a 0.65 aproximadamente. Sin embargo, este modelo parece no considerar adecuadamente una cantidad significativa de datos que presentan anomalías debido a un alto desequilibrio de voltaje (DV), los cuales se encuentran principalmente en la parte superior-derecha del gráfico. 

 
![Imagen 10](https://github.com/ggomez1803/ElectroDunas/assets/10146054/ee45605f-154b-4247-a53b-fe22838e6443)<br>
Imagen 10. Gráfico de dispersión modelo K-Means Cliente 22 

A diferencia del modelo k-means, el modelo basado en umbrales (imagen 11), que mantiene constante el centroide óptimo, nos proporciona una mejor visión de los datos que se alejan más de este centroide “ideal” y, por lo tanto, entre más alejados estén tienen una mayor probabilidad de ser anomalías. Este modelo utiliza la distancia de Mahalanobis como medida de distancia, la cual, a diferencia de la distancia euclidiana, tiene en cuenta la correlación entre las variables aleatorias. Por lo tanto, para nuestro modelo, fundamentados en los resultados, decidimos optar por los modelos de clusterización basado en umbrales, dado que consideramos identifican de una mejor manera las anomalías. 

 ![Imagen 11](https://github.com/ggomez1803/ElectroDunas/assets/10146054/78208824-7a00-4e54-bbc2-5fca37a46967)<br>
Imagen 11. Gráfico de dispersión modelo basado en umbrales Cliente 22 

### Plan de implementación del prototipo: 
Como plan de implementación del prototipo se propone la siguiente infraestructura: 

 ![Imagen 12](https://github.com/ggomez1803/ElectroDunas/assets/10146054/597d6864-b197-4af5-a0fc-60c750eccb18)<br>

A partir de un repositorio de SharePoint se podrán cargar los archivos de entrada con los consumos de los diferentes clientes, posteriormente desde un script de Python se leerán y procesarán los archivos para luego correr el modelo de segmentación para cada cliente, consolidar la información de los consumos y exportar los datos a otro archivo .csv. Este último archivo .csv será el insumo para poder realizar las gráficas de detección de anomalías por cliente. 

Ahora bien, para facilitar la operabilidad del reporte, se han creado varios scripts de Python que están interconectados entre ellos de la siguiente forma: 

 ![Imagen 13](https://github.com/ggomez1803/ElectroDunas/assets/10146054/56b1c53e-32bb-42a5-8574-e87185e54cd2)<br>

Imagen 13. Estructura de scripts de Python 

Donde en rutas.py se diligencian las rutas de lectura y de exportación de los archivos que se van a trabajar, mientras que en Funciones_Procesamiento.py y Funciones_Cluster.py se encuentran todas las acciones que se realizan a los datos de entrada y donde se cargan los modelos de cluster ya entrenados para poder predecir nuevos datos en el futuro. 
