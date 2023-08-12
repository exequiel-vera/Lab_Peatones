import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Rendimiento import get_resource_info


encabezados = ["ID", "frame", "X", "Y", "Z"]

def lectura_datos():
    data = pd.read_csv('UNI_CORR_500_01.txt', sep= "\t" , skiprows=4, names=encabezados )

# Lectura del archivo txt y creación de DataFrame
df = pd.read_csv('UNI_CORR_500_01.txt', sep= "\t" , skiprows=4, names=encabezados )
df2 = pd.read_csv('UNI_CORR_500_05.txt', sep= "\t" , skiprows=4, names=encabezados )

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
plt.tight_layout()
plt.savefig("Comparacion hist 2d.pdf")

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
df['X'] = df.groupby('ID')['X'].diff()
df['Y'] = df.groupby('ID')['Y'].diff()
df['frame'] = df.groupby('ID')['frame'].diff()

df2['X'] = df2.groupby('ID')['X'].diff()
df2['Y'] = df2.groupby('ID')['Y'].diff()
df2['frame'] = df2.groupby('ID')['frame'].diff()


#funcion calculo velocidad
def velocidad(x, y, frame):
    vel_x = x/(frame/fps)
    vel_y = y/(frame/fps)
    return np.sqrt(vel_x**2 + vel_y**2)



df['velocidad_euclidiana'] = velocidad(df['X'], df['Y'], df['frame'])
df2['velocidad_euclidiana'] = velocidad(df2['X'], df2['Y'], df2['frame'])

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


plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.boxplot([df_peaton1['velocidad_euclidiana'], df_peaton2['velocidad_euclidiana'],
             df_peaton3['velocidad_euclidiana'], df_peaton4['velocidad_euclidiana']])
plt.xticks([1, 2, 3, 4], ['Peatón 1', 'Peatón 2', 'Peatón 3', 'Peatón 4'])
plt.ylim(0,2.8)
plt.ylabel('Velocidad Euclidiana (m/s)')
plt.title('Velocidad peatones \"UNI_CORR_500_01\"')

plt.subplot(2, 1, 2)
plt.boxplot([df2_peaton1['velocidad_euclidiana'], df2_peaton2['velocidad_euclidiana'],
             df2_peaton3['velocidad_euclidiana'], df2_peaton4['velocidad_euclidiana']])
plt.xticks([1, 2, 3, 4], ['Peatón 1', 'Peatón 2', 'Peatón 3', 'Peatón 4'])
plt.ylabel('Velocidad Euclidiana (m/s)')
plt.ylim(0,2.8)
plt.title('Velocidad peatones \"UNI_CORR_500_05\"')
plt.tight_layout()
plt.show()


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






