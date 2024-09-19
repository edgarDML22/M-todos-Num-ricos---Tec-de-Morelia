import math
from math import exp
import numpy as np
import sympy as sp

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

def function_f(function_str, value):
    x = sp.symbols('x')
    function = sp.sympify(function_str)
    return function.subs(x, value) # Para evaluar

def calcular_grado_funcion(cad):
    power = cad.find("**") + 2
    return int(power)

def division_sintetica(function_str, solucion):
    "x**4 + 0*x**3 - 13*x**2 + 0*x**1 + 36*x**0"
    #solucion = 2
    grado = calcular_grado_funcion(function_str)
    
    
    
    
    

def calcular_valor_lambda(f_x0, f_x1, h_0):
    return ((f_x1 - f_x0) / h_0)

def calcular_valor_a(lambda_0, lambda_1, h_0, h_1):
    return ((lambda_1 - lambda_0)/(h_1 + h_0))

def calcular_valor_xm1(x_k, a, b, c):
    return (x_k + ((-2*c)/(b + math.sqrt(math.pow(b, 2) - 4*a*c))))

def calcular_valor_xm2(x_k, a, b, c):
    return (x_k + ((-2*c)/(b - math.sqrt(math.pow(b, 2) - 4*a*c))))

def elegir_valor_x_m(function_str, x_m1, x_m2):
    Fx_1 = function_f(function_str, abs(x_m1))
    Fx_2 = function_f(function_str, abs(x_m2))
    if Fx_1 < Fx_2:
        return x_m1
    else:
        return x_m2

def generar_matrix(numero_columnas): # debe ser un int >= 1
    matrix = np.array([3])
    if numero_columnas != 1:
        new_column = np.array([3])
        for i in range(numero_columnas - 1):
            matrix = np.hstack((matrix, new_column))
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

def exportar_archivo_csv(matrix):
    np.savetxt("matriz.csv", matrix, delimiter=",")


def ejecutar_metodo_iterativo(x_0, x_1, x_2, n):
    function_str = "x**4 + 0*x**3 - 13*x**2 + 0*x**1 + 36*x**0" #Aquí va la primera función del programa
    grado_funcion = int(calcular_grado_funcion(function_str))
    soluciones = []
    matrix = generar_matrix(16)
    x_i = valor_cifras_significativas(x_0, n)
    x_j = valor_cifras_significativas(x_1, n)
    x_k = valor_cifras_significativas(x_2, n)
    x_m = 0
    F_xi = 0
    F_xj = 0
    F_xk = 0
    h_0 = 0
    h_1 = 0
    lambda_0 = 0
    lambda_1 = 0
    a = 0
    b = 0
    c = 0
    x_m1 = 0
    x_m2 = 0
    row = 0
    error_relativo = -1;
    error_tolerable = calcular_error_tolerable(n)
    contador_soluciones = 0
    #Calcular el grado del polinomio y en base a eso ir metiendo las soluciones en una lista
    while len(soluciones) < grado_funcion:
        #Evaluar las funciones
        F_xi = valor_cifras_significativas(function_f(function_str, x_i), n)
        F_xj = valor_cifras_significativas(function_f(function_str, x_j), n)
        F_xk = valor_cifras_significativas(function_f(function_str, x_k), n)

        if F_xi == 0 or F_xj == 0 or F_xk == 0:
            #Encontrar la raíz y agregarla a la lista soluciones[]
            if F_xi == 0:
                soluciones.append(x_i)
            elif F_xj == 0:
                soluciones.append(x_j)
            else:
                soluciones.append(x_k)
            #Reducir un grado a la función
            function_str = division_sintetica(function_str, soluciones.get(contador_soluciones))
            contador_soluciones += 1
            #No se registran los valores después de h_1
            new_row = np.array([row, x_i, x_j, x_k, F_xi, F_xj, F_xk, h_0, h_1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
            matrix = np.vstack((matrix, new_row))
        else:
        #Valores de apoyo
            h_0 = valor_cifras_significativas((x_j - x_i), n)
            h_1 = valor_cifras_significativas((x_k - x_j), n)
            lambda_0 = valor_cifras_significativas(calcular_valor_lambda(F_xi, F_xj, h_0), n)
            lambda_1 = valor_cifras_significativas(calcular_valor_lambda(F_xj, F_xk, h_1), n)
            a = valor_cifras_significativas(calcular_valor_a(lambda_0, lambda_1, h_0, h_1), n)
            b = valor_cifras_significativas((a*h_1 + lambda_1), n)
            c = F_xk
            #Calcular los valores de x_m1+ y x_m2-
            x_m1 = valor_cifras_significativas(calcular_valor_xm1(x_k, a, b, c), n)
            x_m2 = valor_cifras_significativas(calcular_valor_xm1(x_k, a, b, c), n)
            #Comparar el valor y elegir la máx próxima a 0 al evaluar la función
            x_m = elegir_valor_x_m(function_str, x_m1, x_m2)
            #Calcular error relativo
            error_relativo = calcular_error_relativo(x_k, x_m)
            #Meter los elementos a la matriz
            new_row = np.array([row, x_i, x_j, x_k, F_xi, F_xj, F_xk, h_0, h_1, lambda_0, lambda_1, a, b, c, x_m1, x_m2, x_m, error_relativo])
            matrix = np.vstack((matrix, new_row))
            #Algoritmo de valores
            x_i = x_j
            x_j = x_k
            x_k = x_m
        row += 1
    return matrix


def main():
    print("Bienvenid@ al método de Müller")
    print("Valor recomnendado: x_i = 0")
    x_i = ask_for_double("un valor para x_0")
    x_j = ask_for_double("un valor para x_1")
    x_k = ask_for_double("un valor para x_2")

    while True:
        n = ask_for_int("el número de cifras significativas con el que desea trabajar")
        if n < 1:
            print("El número de mínimo de cifras significativas es 1, intente de nuevo")            
        else:                     
            break
    matrix = ejecutar_metodo_iterativo(x_i, x_j, x_k, n)
    #exportar_archivo_csv()
    mostrar_valores_registrados(matrix, n)
   
if __name__ == "__main__":
    main()