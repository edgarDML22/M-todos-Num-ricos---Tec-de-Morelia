import math
from math import exp
import numpy as np

matrix = np.array([-1, -1, -1, -1, -1])
new_row_prueba = np.array([3, 5, 3, 3, 3])
matrix = np.vstack((matrix, new_row_prueba))
print(matrix[1][1])