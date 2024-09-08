import math
from math import exp
import numpy as np

matrix = np.array([-1, -1, -1, -1, -1])
new_row_prueba = np.array([3, 5, 3, 3, 3])
matrix = np.vstack((matrix, new_row_prueba))
print(matrix[1][1])

def generar_matrix(numero_columnas): # debe ser un int >= 1
    matrix = np.array([3])
    if numero_columnas != 1:
        new_column = np.array([3])
        for i in range(numero_columnas - 1):
            matrix = np.hstack((matrix, new_column))
    return matrix