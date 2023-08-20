import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.spatial import KDTree
from PIL import Image
encabezados = ["ID", "frame", "X", "Y", "Z"]

def lectura_datos(archivo):
    data = pd.read_csv(archivo, sep="\t", skiprows=4, names=encabezados)
    return data

def main():
    col1, col2 = st.columns([2, 1])
    col1.markdown(" # Aplicación de gráficos ")
    col1.markdown(" Flujo de personas en espacios unidireccionales ")
    image_path = "geo_uni_corr_500.png"
    image = Image.open(image_path)
    col1.image(image, use_column_width=True) 
    datos1 = col2.file_uploader("Carga aquí el primer archivo UNI.txt", type='txt')
    datos2 = col2.file_uploader("Carga aquí el segundo archivo UNI.txt", type='txt')
    
    if datos1 is not None and datos2 is not None:
        df = lectura_datos(datos1)
        df2 = lectura_datos(datos2)
        df_1 = df.copy()
        df_2 = df2.copy()
        
        st.write("""
        ## Muestra de datos del primer archivo cargado
        """)
        st.table(df.head())
        
        st.write("""
        ## Muestra de datos del segundo archivo cargado
        """)
        st.table(df2.head())
 
        st.write("Opciones histograma 2d")  # slider
        div = st.slider('Número de bins:', 0, 130, 25)
        st.write("Bins=", div)

        fig1, ax1 = plt.subplots()
        hist1 = ax1.hist2d(df['X'], df['Y'], bins=div, cmap='inferno')
        plt.colorbar(hist1[3], ax=ax1, label='Frecuencia')
        ax1.set_xlabel('Coordenada X')
        ax1.set_ylabel('Coordenada Y')
        ax1.set_title(f"Histograma 2D \"{os.path.basename(datos1.name)}\"")

        st.pyplot(fig1)
        plt.close(fig1)

        fig2, ax2 = plt.subplots()
        hist2 = ax2.hist2d(df2['X'], df2['Y'], bins=div, cmap='inferno')
        plt.colorbar(hist2[3], ax=ax2, label='Frecuencia')
        ax2.set_title(f"Histograma 2D \"{os.path.basename(datos2.name)}\"")
        # ax2.set_title("Histograma 2D \"{datos2.name}\"")
        ax2.set_xlabel('Coordenada X')
        ax2.set_ylabel('Coordenada Y')

        st.pyplot(fig2)
        plt.close(fig2)

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

        st.write("""
        ## Gráficos de cajas y bigotes de la velocidad de 4 peatones
        """)

        def showboxplot():
            fig_1, ax1 = plt.subplots(figsize=(10, 6))
            ax1.boxplot([df_peaton1['velocidad_euclidiana'], df_peaton2['velocidad_euclidiana'],
                        df_peaton3['velocidad_euclidiana'], df_peaton4['velocidad_euclidiana']])
            ax1.set_xticks([1, 2, 3, 4])
            ax1.set_xticklabels(['Peatón 50', 'Peatón 51', 'Peatón 52', 'Peatón 53'])
            ax1.set_ylim(0, 2.8)
            ax1.set_ylabel('Velocidad Euclidiana (m/s)')
            ax1.set_title(f"Velocidad peatones - \"{os.path.basename(datos1.name)}\"")
            st.pyplot(fig_1)
            plt.close(fig_1)

            fig_2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.boxplot([df2_peaton1['velocidad_euclidiana'], df2_peaton2['velocidad_euclidiana'],
                        df2_peaton3['velocidad_euclidiana'], df2_peaton4['velocidad_euclidiana']])
            ax2.set_xticks([1, 2, 3, 4])
            ax2.set_xticklabels(['Peatón 50', 'Peatón 51', 'Peatón 52', 'Peatón 53'])
            ax2.set_ylim(0, 2.8)
            ax2.set_ylabel('Velocidad Euclidiana (m/s)')
            ax2.set_title(f"Velocidad peatones - \"{os.path.basename(datos2.name)}\"")
            st.pyplot(fig_2)
            plt.close(fig_2)
        showboxplot()

        st.write("""
        ## Histogramas de las velocidades euclidianas
        """)

        st.write("Opciones histogramas velocidades")  # slider
        div1 = st.slider('Número de bins:', 0, 70, 30)
        st.write("Bins=", div1)

        def showhistograma():
            fig11, ax1 = plt.subplots(figsize=(10, 6))
            ax1.hist(df['velocidad_euclidiana'], bins=div1, color= "plum", edgecolor="mediumorchid")
            ax1.set_xlabel('Velocidad Euclidiana (m/s)')
            ax1.set_ylabel("Frecuencia")
            ax1.set_xlim(0, 4)
            ax1.set_title(f"Histograma de velocidades - \"{os.path.basename(datos1.name)}\"")
            st.pyplot(fig11)
            plt.close(fig11)

            fig22, ax2 = plt.subplots(figsize=(10, 6))
            ax2.hist(df2['velocidad_euclidiana'], bins=div1, color= "plum", edgecolor="mediumorchid")
            ax2.set_xlabel('Velocidad Euclidiana (m/s)')
            ax2.set_ylabel("Frecuencia")
            ax2.set_xlim(0, 4)
            ax2.set_title(f"Histograma de velocidades - \"{os.path.basename(datos2.name)}\"")
            st.pyplot(fig22)
            plt.close(fig22)
        showhistograma()
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

        # def showscatter():
        #     figu, ax = plt.subplots(figsize=(10, 6))
        #     ax.scatter(sk["distancia"], velocity["velocidad"])
        #     ax.set_xlabel('SK')
        #     ax.set_ylabel("Velocidad")
        #     ax.set_title('SK v/s Velocidad')
        #     st.pyplot(figu)
        #     plt.close(figu)
        # showscatter()

        from scipy.optimize import curve_fit


        # Datos de SK y Velocidad
        x = sk["distancia"]
        y = velocity["velocidad"]

        # Definir una función polinómica cúbica para el ajuste
        def cubic_func(x, a, b, c, d):
            return a * x**3 + b * x**2 + c * x + d

        # Ajustar la curva utilizando curve_fit
        initial_guess = [1, 1, 1, 1]  # Estimación inicial de los parámetros (a, b, c, d)
        params, params_covariance = curve_fit(cubic_func, x, y, p0=initial_guess)
        a_fit, b_fit, c_fit, d_fit = params  # Desempaquetar los parámetros ajustados de la tupla 'params'

        y_fit = cubic_func(x, a_fit, b_fit, c_fit, d_fit)

        # Crear el gráfico
        figg, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, color='mediumturquoise', edgecolors="lightseagreen", linewidths=1.0, alpha=0.5, label='Datos')
        ax.plot(x, y_fit, color='red', label='Ajuste cúbico')  
        ax.set_ylabel('Velocidad')
        ax.set_title('Ajuste cúbico a scatter plot')
        ax.legend()

        # Mostrar el gráfico en Streamlit
        st.pyplot(figg)
        plt.close(figg)

if __name__ == "__main__":
    main()


