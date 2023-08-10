#................Lectura archivo txt y creación lista de coordenadas..........................

import matplotlib.pyplot as plt
import numpy as np
from Rendimiento import get_resource_info
matriz = []
Coordenadas = []
Coordenadas_X = []
Coordenadas_Y = []
Coordenadas_Z = []

def lectura_datos():
    f = open('UNI_CORR_500_01.txt', 'r')
    for linea in f.readlines():
       separar = linea[0:29]
       aux = separar.split()
       matriz.append(aux)
    f.close()

lectura_datos()


#................Crear una matriz para las cordenadas X,Y,Z..................

for i in range(4, len(matriz)):
    lista = matriz[i]
    j = []
    X = []
    Y = []
    Z = []
    auxX, auxY, auxZ = lista[2], lista[3], lista[4]
    j.append(float(auxX))
    j.append(float(auxY))
    j.append(float(auxZ))
    Coordenadas.append(j)
    X.append(float(auxX))
    Y.append(float(auxY))
    Z.append(float(auxZ))
    Coordenadas_X.append(X)
    Coordenadas_Y.append(Y)
    Coordenadas_Z.append(Z)

    #print(auxX, auxY, auxZ, sep=' ')
#print(aux[2])
#k = int(input('Ingrese la linea de coordenadas que desea saber: '))
#print('Las coordenadas dela linea',k,': ', Coordenadas[k])

#......................................función para contar frecuencias........................................

def contar_frecuencias(coordenadas):
    frecuencias = {}
    for coordenada in coordenadas:
        if coordenada in frecuencias:
            frecuencias[coordenada] += 1
        else:
            frecuencias[coordenada] = 1
    return frecuencias

#..................................funcion para numero de repeticiones......................................

def encontrar_valor_mas_repetido(frecuencias):
    max_frecuencia = 0
    valor_mas_repetido = None
    for valor, frecuencia in frecuencias.items():
        if frecuencia > max_frecuencia:
            max_frecuencia = frecuencia
            valor_mas_repetido = valor
    return valor_mas_repetido, max_frecuencia

#............................uso de funcion para contar frecuencias...........................................

frecuencia_X = contar_frecuencias([coord for sublist in Coordenadas_X for coord in sublist])
frecuencia_Y = contar_frecuencias([coord for sublist in Coordenadas_Y for coord in sublist])
frecuencia_Z = contar_frecuencias([coord for sublist in Coordenadas_Z for coord in sublist])
frecuencia_XY = contar_frecuencias([(Coordenadas_X[i][j], Coordenadas_Y[i][j]) for i in range(len(Coordenadas_X)) for j in range(len(Coordenadas_X[i]))])

#..........................uso de funcion para contar nuemero de repeticiones......................

valor_x_mas_repetido, max_frecuencia_X = encontrar_valor_mas_repetido(frecuencia_X)
valor_y_mas_repetido, max_frecuencia_Y = encontrar_valor_mas_repetido(frecuencia_Y)
valor_z_mas_repetido, max_frecuencia_Z = encontrar_valor_mas_repetido(frecuencia_Z)
valor_xy_mas_repetido, max_frecuencia_XY = encontrar_valor_mas_repetido(frecuencia_XY)

#..........................................Resultados............................................................

#print(f"El valor de la coordenada de X que más se repite es {valor_x_mas_repetido} y aparece {max_frecuencia_X} veces.")
#print(f"El valor de la coordenada de Y que más se repite es {valor_y_mas_repetido} y aparece {max_frecuencia_Y} veces.")
#print(f"El valor de la coordenada de Z que más se repite es {valor_z_mas_repetido} y aparece {max_frecuencia_Z} veces.")
#print(f"La coordenada X,Y que más se repite es {valor_xy_mas_repetido} y aparece {max_frecuencia_XY} veces.")

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

#.....................conversion coordenada metro a pixel.................................

def Conversion(CoordenadaMetro):
    Xmetro, Ymetro = CoordenadaMetro
    Xpixel = int(Mx * Xmetro + 320)
    Ypixel = int(My * Ymetro + 480)
    return Xpixel , Ypixel

#.......................creacion de matrices y diccionario de posiciones...............................................

Matriz640x480 = np.zeros([640 , 480])
FrecCoordPixel = {(ValorX,ValorY): 0 for ValorX in range(641) for ValorY in range(481)}

#........................traspaso de coordenadas XY de metro a pixel.............................................

for coordenada, frecuencia in frecuencia_XY.items():
    CoordenadaPixel = Conversion(coordenada)
    #print(f'La coordenada metrica: {coordenada} pasa a pixel {CoordenadaPixel}' )
    FrecCoordPixel[CoordenadaPixel] = frecuencia

#............................funcion para convertir coordenadas X e Y de metro a píxeles........................
def ConversionXY(CoordenadaMetroX, CoordenadaMetroY):
    Xpixel = int(Mx * CoordenadaMetroX + 320)
    Ypixel = int(My * CoordenadaMetroY + 480)
    return Xpixel, Ypixel

#..............................conversion coordenadas X e Y de metro a píxeles y contar frecuencias............................

frecuencia_XY_pixel = {}
for coordenada, frecuencia in frecuencia_XY.items():
    CoordenadaPixelX, CoordenadaPixelY = ConversionXY(coordenada[0], coordenada[1])
    frecuencia_XY_pixel[(CoordenadaPixelX, CoordenadaPixelY)] = frecuencia


#........................calculo de Coordenada X,Y mas repetida en PIXEL...........................................

max_frecuenciaPixelXY = max(FrecCoordPixel.values())
XYPixel_mas_repetida = [CordXY for CordXY, frecuenciaXY in FrecCoordPixel.items() if frecuenciaXY == max_frecuenciaPixelXY]
#print(f"La(s) coordenadas X,Y que más se repite(n): {XYPixel_mas_repetida} con un recuento de {max_frecuenciaPixelXY} oportunidades")

#..............................creacion histograma 2D utilizando Matplotlib.......................................

coordenadas_xy_pixel = np.array(list(frecuencia_XY_pixel.keys()))
plt.figure(figsize=(10, 8))
plt.hist2d(coordenadas_xy_pixel[:, 0], coordenadas_xy_pixel[:, 1], bins=33, cmap='inferno')
plt.colorbar(label='Frecuencia')
plt.xlabel('Coordenada X (píxeles)')
plt.ylabel('Coordenada Y (píxeles)')
plt.title('Histograma 2D de Coordenadas X e Y en Píxeles')
plt.show()

get_resource_info(lectura_datos)

