import pandas as pd
import numpy as np
import sympy as sp
import math
import os

matrix = np.empty((0,0))
    #Extraer datos del archivo csv
#matrix = np.loadtxt('Datos_Metodo_Coeficientes_Interpolantes.csv', delimiter=',', skiprows=1)
df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\datos\\Datos_Metodo_Coeficientes_Interpolantes.csv', delimiter=',')
matrix = df.to_numpy()
print()

print(np.sum(matrix))


# Mostrar los primeros registros
print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
