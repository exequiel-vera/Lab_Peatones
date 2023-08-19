import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Rendimiento import get_resource_info
from scipy.spatial import KDTree
from scipy.optimize import curve_fit

encabezados = ["ID", "frame", "X", "Y", "Z"]

def lectura_datos():
    data = pd.read_csv('UNI_CORR_500_01.txt', sep= "\t" , skiprows=4, names=encabezados )

# Lectura del archivo txt y creación de DataFrame
df = pd.read_csv('UNI_CORR_500_01.txt', sep= "\t" , skiprows=4, names=encabezados )
df2 = pd.read_csv('UNI_CORR_500_05.txt', sep= "\t" , skiprows=4, names=encabezados )

df_1 = pd.read_csv('UNI_CORR_500_01.txt', sep= "\t" , skiprows=4, names=encabezados )
df_2 = pd.read_csv('UNI_CORR_500_05.txt', sep= "\t" , skiprows=4, names=encabezados )



#Analizis exploratorio de los datos
#print(df.info())
#columna_seleccionada = df["Y"]
#print(columna_seleccionada)

#a = int(input("agrege el ide de la persona: "))
#Filtrar y seleccionar columnas al mismo tiempo
#resultados_filtrados = df[df["ID"] == a][["frame","X", "Y"]]
#print(resultados_filtrados)


# Crear un histograma 2D utilizando las coordenadas X e Y
plt.subplot(2, 1, 1)
plt.hist2d(df['X'], df['Y'], bins=33, cmap='inferno')
plt.colorbar(label='Frecuencia')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.title("Histograma 2D \"UNI_CORR_500_01.txt\"")

plt.subplot(2, 1, 2)
plt.hist2d(df2['X'], df2['Y'], bins=33, cmap='inferno')
plt.title("Histograma 2D \"UNI_CORR_500_05.txt\"")
plt.colorbar(label='Frecuencia')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
#plt.tight_layout()
#plt.savefig("Comparacion hist 2d.pdf")

#plt.show()

#medicion tiempo que demora en cargar los datos
#get_resource_info(lectura_datos)

#................................funcion para calculo de pendientes......................................

def calcular_pendiente(ValorMetrico1, ValorPixel1, ValorMetrico2, ValorPixel2):
    m = (ValorPixel2 - ValorPixel1) / (ValorMetrico2 - ValorMetrico1)
    return m

#..........................uso de funcion para calculo de las pendientes......................................

Xm1, Xp1 = 0 , 320
Xm2, Xp2 = 9 , 640
Ym1, Yp1 = 0 , 480
Ym2, Yp2 = 5 , 0

Mx = calcular_pendiente(Xm1, Xp1, Xm2, Xp2)
#print("La pendiente de X (pixel/metro) es: ", Mx)
My = calcular_pendiente(Ym1, Yp1, Ym2, Yp2)
#print("La pendiente de y (pixel/metro) es: ", My)

#convercion a pixeles
df["Xpixel"]= df["X"]* Mx  + 320
df["Ypixel"]= df["Y"]* My  + 480
#print(df)

fps = 25

#descomposicion de los data frame por grupo
df_1['X'] = df_1.groupby('ID')['X'].diff()
df_1['Y'] = df_1.groupby('ID')['Y'].diff()
df_1['frame'] = df_1.groupby('ID')['frame'].diff()

df_2['X'] = df_2.groupby('ID')['X'].diff()
df_2['Y'] = df_2.groupby('ID')['Y'].diff()
df_2['frame'] = df_2.groupby('ID')['frame'].diff()



#funcion calculo velocidad
def velocidad(x, y, frame):
    vel_x = x/(frame/fps)
    vel_y = y/(frame/fps)
    return np.sqrt(vel_x**2 + vel_y**2)



df['velocidad_euclidiana'] = velocidad(df_1['X'], df_1['Y'], df_1['frame'])

df2['velocidad_euclidiana'] = velocidad(df_2['X'], df_2['Y'], df_2['frame'])


df = df.dropna()
df2 = df2.dropna()


df_peaton1 = df.groupby("ID").get_group(50)
df_peaton2 = df.groupby("ID").get_group(51)
df_peaton3 = df.groupby("ID").get_group(52)
df_peaton4 = df.groupby("ID").get_group(53)

df2_peaton1 = df2.groupby("ID").get_group(50)
df2_peaton2 = df2.groupby("ID").get_group(51)
df2_peaton3 = df2.groupby("ID").get_group(52)
df2_peaton4 = df2.groupby("ID").get_group(53)

def showboxplot():
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.boxplot([df_peaton1['velocidad_euclidiana'], df_peaton2['velocidad_euclidiana'],
                df_peaton3['velocidad_euclidiana'], df_peaton4['velocidad_euclidiana']])
    plt.xticks([1, 2, 3, 4], ['Peatón 50', 'Peatón 51', 'Peatón 52', 'Peatón 53'])
    plt.ylim(0,2.8)
    plt.ylabel('Velocidad Euclidiana (m/s)')
    plt.title('Velocidad peatones \"UNI_CORR_500_01\"')

    plt.subplot(2, 1, 2)
    plt.boxplot([df2_peaton1['velocidad_euclidiana'], df2_peaton2['velocidad_euclidiana'],
                df2_peaton3['velocidad_euclidiana'], df2_peaton4['velocidad_euclidiana']])
    plt.xticks([1, 2, 3, 4], ['Peatón 50', 'Peatón 51', 'Peatón 52', 'Peatón 53'])
    plt.ylabel('Velocidad Euclidiana (m/s)')
    plt.ylim(0,2.8)
    plt.title('Velocidad peatones \"UNI_CORR_500_05\"')
    plt.tight_layout()
    plt.show()


def showhistograma():
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.hist(df['velocidad_euclidiana'], bins = 50, color= "lightcoral")
    plt.xlabel('Velocidad Euclidiana (m/s)')
    plt.ylabel("Frecuencia")
    plt.xlim(0,4)
    plt.title('Velocidad peatones \"UNI_CORR_500_01\"')

    plt.subplot(2, 1, 2)
    plt.hist(df2['velocidad_euclidiana'], bins = 50, color= "lightcoral")
    plt.xlabel('Velocidad Euclidiana (m/s)')
    plt.ylabel("Frecuencia")
    plt.xlim(0,4)
    plt.title('Velocidad peatones \"UNI_CORR_500_05\"')
    plt.tight_layout()
    plt.show()

#get_resource_info(lambda: velocidad(df['X'], df['Y'], df['frame']))
#get_resource_info(lambda: velocidad(df2['X'], df2['Y'], df2['frame']))

radius = 3.0
frames_range = range(99, 1987)  # Frames desde 99 hasta 1986

# Crear listas para almacenar los resultados
peaton = []
vecino = []
distancia = []
frame_numero = []

for frame in frames_range:
    df_frame = df[df["frame"] == frame]
    cord = df_frame[["ID", "X", "Y"]]
    
    arbol = KDTree(cord[["X", "Y"]].values)
    
    # Obtener todas las coordenadas de los peatones en el frame
    all_coords = cord[["X", "Y"]].values
    
    for i, ID in enumerate(df_frame["ID"]):
        cord_int = cord[cord["ID"] == ID]
        
        # Encontrar los vecinos dentro del radio
        vecinos_indices = arbol.query_ball_point(cord_int[["X", "Y"]].values[0], radius)
        vecinos_indices = [index for index in vecinos_indices if cord.iloc[index]["ID"] != ID]
        
        if vecinos_indices:
            # Calcular distancias usando numpy broadcasting
            distances = np.linalg.norm(all_coords[vecinos_indices] - cord_int[["X", "Y"]].values[0], axis=1)
            
            # Agregar los resultados a las listas
            peaton.extend([ID] * len(vecinos_indices))
            vecino.extend(cord.iloc[vecinos_indices]["ID"].tolist())
            distancia.extend(distances.tolist())
            frame_numero.extend([frame] * len(vecinos_indices))
            


# Crear el DataFrame final
result_df = pd.DataFrame({
    "Peaton": peaton,
    "Vecino": vecino,
    "Distancia": distancia,
    "Frame": frame_numero
})


seleccion = ["Frame", "Peaton", "Distancia"]
aux = result_df[seleccion]
fusion = aux.merge(df, left_on=["Frame", "Peaton"], right_on=["frame", "ID"], how= 'inner')
velocity = fusion.groupby(["Frame", "Peaton"])["velocidad_euclidiana"].mean()
velocity = velocity.reset_index()
velocity = velocity.rename(columns={"velocidad_euclidiana": "velocidad"})


sk = result_df.groupby(["Frame", "Peaton"])["Distancia"].mean()
sk = sk.reset_index()
sk = sk.rename(columns={"Distancia": "distancia"})


def showscatter():
    plt.figure(figsize=(10, 6))
    plt.scatter(sk["distancia"], velocity["velocidad"])
    plt.xlabel('SK')
    plt.ylabel("Velocidad")
    plt.title('SK v/s Velocidad')
    plt.show()
showscatter()


# Datos de SK y Velocidad
x = sk["distancia"]
y = velocity["velocidad"]

# Definir una función logarítmica para el ajuste
def logarithmic_func(x, a, b):
    return a * np.log(x) + b

# Ajustar la curva utilizando curve_fit
initial_guess = [1, 0.1]  # Estimación inicial de los parámetros (a, b)
params, params_covariance = curve_fit(logarithmic_func, x, y, p0=initial_guess)

# Obtener los parámetros ajustados
a_fit, b_fit = params

# Calcular los valores ajustados
y_fit = logarithmic_func(x, a_fit, b_fit)

# Plot del scatter plot y la curva ajustada
plt.figure(figsize=(10, 6))
plt.scatter(x, y, label='Datos')
plt.plot(x, y_fit, color='red', label='Ajuste logarítmico')
plt.xlabel('SK')
plt.ylabel('Velocidad')
plt.title('Ajuste logarítmico a scatter plot')
plt.legend()
plt.show()

# Imprimir los parámetros ajustados
print("Parámetros ajustados:")
print("a:", a_fit)
print("b:", b_fit)












