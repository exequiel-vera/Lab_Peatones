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

plt.show()

#medicion tiempo que demora en cargar los datos
get_resource_info(lectura_datos)













