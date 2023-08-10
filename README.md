![Logo UCN](images/60x60-ucn-negro.png)
# Laboratorio 02: Visualizar mapas de calor (Histogramas 2D)


## 1. Introducción 

El estudio del flujo de personas en espacios unidireccionales podría tratarse de un tema fundamental para la planificación urbana y la gestión de multitudes ya que entender cómo se mueven las personas podría garantizar la seguridad, eficiencia y comodidad en diversos escenarios. En este informe, se presenta la primera parte del desarrollo para abordar el dicho problema, con los datos recopilados, los cuales contienen las coordenadas en metros que describen la ruta seguida por las personas, las cuales serán transformadas posteriormente a píxeles, lo que permitirá calcular una matriz de frecuencia que represente la ruta seguida por las personas en términos de píxeles. Para posteriormente graficar los datos a través de un histograma en 2D.

### 1.1 Justificación 

En situaciones como evacuaciones de emergencia, eventos deportivos o festivales musicales se requieren de una planificación cuidadosa que garantice la seguridad de las personas. La transformación de las coordenadas (X, Y) a píxeles es esencial para cuantificar y analizar de manera más precisa el recorrido de estas ya que con ello se puede construir una matriz de frecuencia con la cual se pueden implementar mapas de calor y así visualizar los patrones de densidad, dado que cada píxel representa una unidad de área y su intensidad de color se correlaciona con la magnitud de los datos en esa ubicación por lo que se mostraran aquellas áreas más transitadas, facilitando la identificación de áreas críticas que requieran intervenciones específicas.

### 1.3 Objetivos 

**Objetivo general**

Creación de un histograma en 2D con la libreía "Matplotlib" de la ruta que siguen las personas en un pasillo unidireccional y compararla con otro data set.

 

**Objetivos específicos**

1. Cargar los datos de las coordenadas (x, y) utilizando la librería "Pandas".
2. Utilizar distintos data sets que varíen el ancho de las puertas de entrada y salida
3. Comparar el rendimiento del código anterior y el Código utilizando librerías.


## 2. Marco teórico 

Python: Es un lenguaje de programación de alto nivel. Presenta una sintaxis clara y legible. Es un lenguaje versátil que se utiliza en una amplia variedad de aplicaciones.

Visual Studio Code (VSCode): Editor de código fuente desarrollado por Microsoft.  Admite una variedad de lenguajes de programación, incluido Python, y proporciona funciones útiles como resaltado de sintaxis, autocompletado y depuración integrada.

NumPy: Es una biblioteca de Python ampliamente utilizada para realizar cálculos numéricos y operaciones con matrices y matrices multidimensionales. Introduce un objeto de matriz multidimensional llamado numpy.array, que permite realizar operaciones eficientes en grandes conjuntos de datos.

Matplotlib: Biblioteca de visualización de datos en Python que proporciona una amplia variedad de herramientas para crear gráficos estáticos, interactivos y animaciones.

Pandas: biblioteca de análisis de datos en Python que proporciona estructuras de datos flexibles y herramientas para manipular y analizar datos de manera eficiente.


## 3. Materiales y métodos

Los Data Sets utilizados en el laboratorio son archivos de texto descargados de “Pedestrian Dynamics Data Archive”, que contienen datos de coordenadas (x, y, z) que describen la ruta seguida por las personas en el corredor unidireccional. Cada línea del archivo representa una ruta individual con sus respectivas coordenadas.

El tamaño del Data Set dependerá de la cantidad de rutas registradas en el archivo y corresponderá al número de líneas presentes en el archivo, para el caso se utilizaron dos data sets, los cuales son UNI_CORR_500_01 y UNI_CORR_500_05, el primero cuenta con 25.536 datos. Mientras que el segundo tiene un total de 363.064 datos.

Descripción del Experimento:

El experimento consiste en analizar el flujo de personas en un pasillo unidireccional mediante el análisis de datos de coordenadas (x, y) proporcionados por los archivos de texto. Durante el proceso del laboratorio, se llevan a cabo diferentes operaciones como la lectura de los archivos, la exploración de los datos y la creación de los histogramas. 

Secuencia de Pasos:

Se inicia importando las librerías necesarias, en este caso Pandas, Matplotlib y NumPy (Lab 1), luego se cargan los documentos en un data frame utilizando Pandas, se le asigna un encabezado que sea representativo a cada columna de datos que contiene el TXT.  Con ello se utilizaron distintas funciones integradas en la librería para la exploración de los datos y tener un mejor entendimiento de estos. Una vez realizado esto con ayuda del data frame creado y la librería Matplotlib se generaron dos histogramas 2D con la frecuencia de las coordenadas X e Y para distintas medidas de los anchos de las puertas.


## 4. Resultados obtenidos


|       Tipo de Experimento      | Tiempo de ejecucion (seg) |  Memoria utilizada (Mb) |
|--------------------------------|---------------------------|-------------------------|
| Lectura Uno (Codigo_Lab.py)    | 0.020186185836791992 seg  | 155.3828125 MB          |
| Lectura Dos (Codigo_Pandas.py) | 0.01766800880432129 seg   | 151.609375 MB           |
Tabla 1: Comparación eficiencia computacional

Con respecto a la eficiencia computacional, se evaluó la lectura del mismo archivo de texto (UNI_CORR_500_01) utilizando ciclos “FOR” en una primera instancia y luego se procedió con el mismo proceso, pero esta vez con la librería pandas. Se nota una clara eficiencia a la hora de escribir el Código debido a su extensión y legibilidad, siendo claramente mas legible con la librería pandas, además como se muestra en la tabla 1 los números respaldan esto, ya que este Código ocupa menos memoria y además se demora 0,03 segundos menos que el primer Código.

<img src="images/comparacion.png" width="600">
Imagen 1: Comparación HeatMaps


Para el estudio de flujo de personas en pasillos unidireccionales con diferentes tamaños de las puertas de entrada y de salida, se generaron dos histogramas 2D que muestran la distribución del flujo de personas en función de las coordenadas X e Y en el pasillo. Estos histogramas proporcionan la información sobre cómo las variaciones en el diseño del pasillo afectan el comportamiento de las personas y como circulan a lo largo del mismo.

En el primer histograma que contiene los datos del archivo con una puerta de entrada de 1 metro y una puerta de salida de 5 metros, se observa que el flujo de personas tiende a ser mayor en el centro del pasillo. Esto podría indicar que los individuos tienden a agruparse en el centro debido a la ubicación de las puertas de entrada y salida, lo que podría estar relacionado con la distribución asimétrica de las puertas. Además, se observa un punto en el inicio del pasillo, justo en el centro que está completamente negro, es decir, no está pasando nadie por ahí. Este punto parece ser el resultado de una obstrucción causada por una persona que se quedó parada en ese lugar, bloqueando el paso de los demás.

Para el segundo histograma se utilizaron los datos del archivo con una puerta de entrada de 5 metros y una puerta de salida de 5 metros, se observa que la distribución del flujo de personas es diferente en comparación con el primer histograma. Aquí, los colores fríos predominan, lo que indica que las personas se distribuyen más uniformemente a lo largo del pasillo. Esto podría sugerir que el diseño de las puertas de entrada y salida más amplias permite un flujo más fluido y sin obstrucciones. Aunque esta distribución uniforme es favorable en términos de un tránsito más ágil y eficiente, también podría significar un mayor uso de recursos y gastos debido a la necesidad de un espacio más amplio.

La elección del tamaño de las puertas debe ser el óptimo, que busque el equilibrio entre un flujo eficiente y los factores económicos y logísticos, ya que, si bien una distribución uniforme podría ser más eficiente desde el punto de vista del tránsito, podría requerir inversiones adicionales en espacio y recursos.


## 5. Conclusiones

En este laboratorio es posible analizar y reconocer la importancia del estudio del comportamiento y flujo de las personas en diferentes espacios, analizando de manera detallada y visual (a través de los mapas de calor) los patrones de densidad en diferentes diseños de puertas de entrada y salida, los cuales revelaron puntos importantes en cuanto a dicho comportamiento de las personas. El primer histograma resaltó la influencia de la distribución asimétrica de las puertas en la concentración de flujo en el centro del pasillo, así como la posibilidad de obstrucciones puntuales. Por otro lado, el segundo histograma demostró que puertas más amplias favorecen una distribución más uniforme del flujo, aunque podrían requerir una inversión mayor en espacio y recursos.

La utilización de herramientas como Python, Pandas, Matplotlib y NumPy demostró su eficacia en el procesamiento y análisis de datos, mostrando cómo las librerías pueden mejorar la eficiencia y legibilidad del código. Estos resultados sugieren que la combinación de tecnologías de análisis de datos y visualización puede desempeñar un papel crucial en la toma de decisiones de planificación y en la creación de espacios seguros y eficientes para la circulación de personas en diferentes eventos y situaciones.




