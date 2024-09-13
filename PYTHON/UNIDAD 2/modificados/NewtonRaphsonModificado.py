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
    return math.pow(x, 3) - 5*math.pow(x, 2) + 7*x - 3

def derivative_function_f(x):
    return 3*math.pow(x, 2) - 10*x + 7

def second_derivative_function_f(x):
    return 6*x - 10

def calcular_valor_x_j(x_i, F_xi, Fp_xi, Fpp_xi):    
    return (x_i - ((F_xi*Fp_xi)/(math.pow(Fp_xi, 2) - (F_xi*Fpp_xi))))

def generar_matrix(numero_columnas): # debe ser un int >= 1
    matrix = np.array([3])
    if numero_columnas != 1:
        new_column = np.array([3])
        for i in range(numero_columnas - 1):
            matrix = np.hstack((matrix, new_column))
    return matrix


def ejecutar_metodo_iterativo(x, n):
    matrix = generar_matrix(7)
    x_i = valor_cifras_significativas(x, n)
    F_xi = 0
    x_j = 0
    row = 0
    error_relativo = -1;
    error_tolerable = calcular_error_tolerable(n)
    while True:
        F_xi = valor_cifras_significativas(function_f(x_i), n)
        Fp_xi = valor_cifras_significativas(derivative_function_f(x_i), n)
        Fpp_xi = valor_cifras_significativas(second_derivative_function_f(x_i), n)
        if F_xi != 0:
            #Calcular el valor de x_{i+1}
            x_j = valor_cifras_significativas(calcular_valor_x_j(x_i, F_xi, Fp_xi, Fpp_xi), n)
        #Calcular error relativo
        error_relativo = calcular_error_relativo(x_i, x_j)#Corregir
        #Meter los elementos al arreglo
        new_row = np.array([row, x_i, F_xi,Fp_xi, Fpp_xi, x_j, error_relativo])
        matrix = np.vstack((matrix, new_row))
        if (error_relativo < error_tolerable) and row > 1:
            break #Para romper el ciclo 
        else:
            x_i = x_j
            row += 1
    return matrix
            
def mostrar_valores_registrados(matrix, n):
    print("f(x) = x^2 - 7")
    print("    |    i      |    |    x_i    |    |  f(x_i)   |    |  f'(x_i)  |    |  f''(x_i) |    |  x_(i+1)  |    | Error relativo |")
    for i in range(matrix.shape[0]):
        if i != 0:
            fila = []
            for j in range(matrix.shape[1]):
                if j == 0:
                    fila.append(f"{int(matrix[i][j]):3}")
                elif j == matrix.shape[1] - 1:
                    fila.append(f"{valor_cifras_significativas(matrix[i, j], n)} %")
                else:
                    fila.append(f"{matrix[i][j]}")
            print("|".join(f"    | {valor:10}" for valor in fila) + "|")    

    print(f"Valor de la raíz: {matrix[matrix.shape[0] - 1][1]}")



def main():
    print("Bienvenid@ al método de Newton-Raphson")
    print("Valor recomnendado: x_i = 0")
    x_i = 0
    while True:
        try:
            x_i = ask_for_double("un valor para x_i")
            r = function_f(x_i)
            print("Valor adecuado para trabajar con el método")
            break
        except Exception as e:
            print("El valor ingresado no es válido para el tipo de función, intente con otro valor")
            print(f"Valor anterior: {x_i}")     
    while True:
        n = ask_for_int("el número de cifras significativas con el que desea trabajar")
        if n < 1:
            print("El número de mínimo de cifras significativas es 1, intente de nuevo")            
        else:                     
            break
    matrix = ejecutar_metodo_iterativo(x_i, n)
    mostrar_valores_registrados(matrix, n)
   
if __name__ == "__main__":
    main()