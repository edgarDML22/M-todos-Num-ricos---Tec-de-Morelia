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

def derivative_function_f(x):
    return 2*x

def calcular_valor_x_j(x_i, F_xi, Fp_xi):
    return (x_i - (F_xi / Fp_xi))

def generar_matrix(numero_columnas): # debe ser un int >= 1
    matrix = np.array([3])
    if numero_columnas != 1:
        new_column = np.array([3])
        for i in range(numero_columnas - 1):
            matrix = np.hstack((matrix, new_column))
    return matrix


def ejecutar_metodo_iterativo(x, n):
    matrix = generar_matrix(6)
    x_i = valor_cifras_significativas(x, n)
    flag = True
    F_xi = 0
    x_j = 0
    row = 0
    error_relativo = -1;
    error_tolerable = calcular_error_tolerable(n)
    while True:
        F_xi = valor_cifras_significativas(function_f(x_i), n)
        Fp_xi = valor_cifras_significativas(derivative_function_f(x_i), n)
        #Verificar que la derivada no sea 0
        if Fp_xi == 0:
            flag = False
            break
        #Calcular el valor de x_{i+1}
        x_j = valor_cifras_significativas(calcular_valor_x_j(x_i, F_xi, Fp_xi), n)
        #Calcular error relativo
        error_relativo = calcular_error_relativo(x_i, x_j)#Corregir
        #Meter los elementos al arreglo
        new_row = np.array([row, x_i, F_xi,Fp_xi, x_j, error_relativo])
        matrix = np.vstack((matrix, new_row))
        #Método Punto Fijo
        if F_xi == 0:
            break #Para romper el ciclo
        else:
            if (error_relativo < error_tolerable) and row > 1:
                break #Para romper el ciclo 
            else:
                x_i = x_j
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
    print(f"Valor de la raíz: {matrix[matrix.shape[0] - 1][1]}")



def main():
    print("Bienvenid@ al método de Newton-Raphson")
    print("Valor recomnendado: x_i = 0")
    x_i = 0
    while True:
        while True: #Validar que la función exista en este punto
            try:
                x_i = ask_for_double("un valor para x_i")
                r = function_f(x_i)
            except Exception as e:
                print("El valor ingresado no es válido para el tipo de función, intente con otro valor")
                print(f"Valor anterior: {x_i}")
            if derivative_function_f(x_i) == 0:
                print("El valor de x_i hace valer 0 la derivada de la función, proponga un nuevo valor")
            else:
                print("Valor adecuado para trabajar con el método")
                break
        while True:
            n = ask_for_int("el número de cifras significativas con el que desea trabajar")
            if n < 1:
                print("El número de mínimo de cifras significativas es 1, intente de nuevo")            
            else:                     
                break
        array = ejecutar_metodo_iterativo(x_i, n)
        if array[0] == False:
            print("Con el valor dado de x_i, la derivada en alguna iteración tuvo un valor de 0")
            print("Proponga un nuevo valor para x_i")
        else:
            mostrar_valores_registrados(array[1], n)
            break
   
if __name__ == "__main__":
    main()