import math
from math import exp
import numpy as np


def ask_for_double(nombre_valor):
    while True:
        try:
            return float(input(f"Ingrese {nombre_valor}: "))
        except Exception as e:
            print("Se ingresó un valor inválido, intente de nuevo")

def ask_for_int(nombre_valor):
    while True:
        try:
            return int(input(f"Ingrese {nombre_valor}: "))
        except Exception as e:
            print("Se ingresó un valor inválido, intente de nuevo")

def valor_cifras_significativas(numero, n):
    if numero == 0:
        return 0
    else:
        factor = n - (int(f"{numero:e}".split('e')[1]) + 1)
        return round(numero, factor)
    
def calcular_error_tolerable(n):
    return 0.5*(math.pow(10, 2-n))

def calcular_error_relativo(valor_anterior, valor_actual):
    return (abs(1 - (valor_anterior / valor_actual)))*100

def function_f(x):
    return math.pow(x, 2) - 7

def calcular_valor_x_k(x_i, x_j, F_xi, F_xj):
    return (x_j - F_xj*((x_j - x_i)/(F_xj - F_xi)))

def generar_matrix(numero_columnas): # debe ser un int >= 1
    matrix = np.array([3])
    if numero_columnas != 1:
        new_column = np.array([3])
        for i in range(numero_columnas - 1):
            matrix = np.hstack((matrix, new_column))
    return matrix


def ejecutar_metodo_iterativo(x_0, x_1, n):
    matrix = generar_matrix(7)
    flag = True
    x_i = valor_cifras_significativas(x_0, n)
    x_j = valor_cifras_significativas(x_1, n)
    F_xi = 0
    F_xj = 0
    row = 0
    error_relativo = -1;
    error_tolerable = calcular_error_tolerable(n)
    while True:
        F_xi = valor_cifras_significativas(function_f(x_i), n)
        F_xj = valor_cifras_significativas(function_f(x_j), n)
        #Calcular el valor de x_{i+2}
        x_k = valor_cifras_significativas(calcular_valor_x_k(x_i, x_j, F_xi, F_xj), n)
        #Calcular error relativo
        error_relativo = calcular_error_relativo(x_j, x_k)
        #Meter los elementos al arreglo
        new_row = np.array([row, x_i, x_j, F_xi, F_xj, x_k, error_relativo])
        matrix = np.vstack((matrix, new_row))
        #Método Punto Fijo
        if F_xi == 0 or F_xj == 0:
            break #Para romper el ciclo
        elif (error_relativo < error_tolerable) and row > 1:
            break
        elif error_relativo > 300 and row > 10:
            flag = False
            break
        else:
            x_i = x_j
            x_j = x_k                
            row += 1
    return [flag, matrix]
            
def mostrar_valores_registrados(matrix, n):
    print("f(x) = x^2 - 7")
    print("|   i  |\t|   x_i  |\t|  f(x_i) |\t| x_(i+1) |\t|   Error relativo  |")
    for i in range(matrix.shape[0]):
        if i != 0:
            for j in range(matrix.shape[1]):
                if j == 0:
                    print(f"| {round(matrix[i][j], 0)} |\t", end="")
                elif j == matrix.shape[1] - 1:
                    print(f"| {round(matrix[i][j], n)} % |\t", end="")
                else: 
                    print(f"| {matrix[i][j]} |\t", end="")
            print("")    

    #last_row = matrix.shape[0] - 1
    print(f"Valor de la raíz: {matrix[matrix.shape[0] - 1][5]}")



def main():
    print("Bienvenid@ al método de la secante")
    print("Valores recomnendados: x_0 = 0, x_1 = 1")
    x_0 = 0
    x_1 = 0
    while True: #Validar que la función exista en este punto
        try:
            x_0 = ask_for_double("un valor para x_0")
            r = function_f(x_0) * function_f(x_1) 
            x_1 = ask_for_double("un valor para x_1")             
            print("Valores adecuados para trabajar con el método")
            break
        except Exception as e:
            print("EL último valor ingresado no es válido para el tipo de función, intente con otro valor")

    while True:
        n = ask_for_int("el número de cifras significativas con el que desea trabajar")
        if n < 1:
            print("El número de mínimo de cifras significativas es 1, intente de nuevo")            
        else:                     
            break
    array = ejecutar_metodo_iterativo(x_0, x_1, n)
    mostrar_valores_registrados(array[1], n)
    if array[0] == False:
        print("El valor no convergió a un resultado en concreto")
            
   
if __name__ == "__main__":
    main()