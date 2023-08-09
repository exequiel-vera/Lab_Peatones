import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
encabezados = ["ID", "frame", "X", "Y", "Z"]
# Lectura del archivo txt y creación de DataFrame
data = pd.read_csv('Pea.txt', sep= "\t" , skiprows=4, names=encabezados )


#entrega las priemras 5 filas del documento 
print(data.head())
# Seleccionar una columna específica
#columna_seleccionada = data["Y"]
#print(columna_seleccionada)

#a = int(input("agrege el ide de la persona: "))
#Filtrar y seleccionar columnas al mismo tiempo
#resultados_filtrados = data[data["ID"] == a][["frame","X", "Y"]]
#print(resultados_filtrados)

#falta pasar a pixel

# Crear un histograma 2D utilizando las coordenadas X e Y
plt.figure(figsize=(10, 6))
plt.hist2d(data['X'], data['Y'], bins=33, cmap='inferno')
plt.colorbar(label='Frecuencia')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.title('Histograma 2D de Coordenadas X e Y')
plt.show()