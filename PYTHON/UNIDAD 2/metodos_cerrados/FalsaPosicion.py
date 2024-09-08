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
        # f"{numero:e}", te da el número en notación científica(String)
        #.split() separa la cadena en una lista y en la segunda posición[1] queda el exponente del 10^x
        # se convierte en un entero con int()
        factor = n - (int(f"{numero:e}".split('e')[1]) + 1)
        return round(numero, factor)
    
def calcular_error_tolerable(n):
    return 0.5*(math.pow(10, 2-n))

def calcular_error_relativo(valor_anterior, valor_actual):
    return (abs(1 - (valor_anterior / valor_actual)))*100

def function(valor):
    return (math.exp(2*valor)-3)

def calcular_valor_C(a, b, F_a, F_b):
    return ((a * F_b) - (b * F_a)) / (F_b - F_a)

##def calcular_valor_con_n_cifras_significativas(n):


def ejecutar_metodo_iterativo(A, B, n):
    ##Devolver en una lista en 0: la matriz y en 1 el número de filas
    ##Puedes obtener el número de filas con la función shape
    matrix = np.zeros((50, 7))
    a = valor_cifras_significativas(A, n)
    b = valor_cifras_significativas(B, n)
    F_a = valor_cifras_significativas(function(a), n)
    F_b = valor_cifras_significativas(function(b), n)
    c = 0
    row = 0
    flag_row = 0
    error_relativo = -1;
    error_tolerable = calcular_error_tolerable(n)
    while True:
        if row == matrix.shape[0]:
            break
        c = valor_cifras_significativas(calcular_valor_C(a, b, F_a, F_b), n)
        F_c = valor_cifras_significativas(function(c), n)
        #Calcular error relativo
        if row != 0:
            error_relativo = calcular_error_relativo(matrix[row-1, 4], c)
            #print(f"Valor de c anterior: {matrix[row-1, 4]}")
            #print(f"Valor de c actual: {c}")
            #print(f"Nuevo error relativo: {error_relativo}")
        #Para romper el ciclo
        if error_relativo < error_tolerable and row != 0:
            flag_row = row + 1
        #Meter los elementos al arreglo
        matrix[row] = [a, b, F_a, F_b, c, F_c, error_relativo]
        row += 1
        if row == flag_row:
            break
        #Método Falsa Posición
        R = F_c * F_a
        if R > 0:
            a = valor_cifras_significativas(c, n)
            F_a = valor_cifras_significativas(function(a), n)
        elif R == 0:
            print("Se obtuvo una raíz exacta")
        else:
            b = valor_cifras_significativas(c, n)
            F_b = valor_cifras_significativas(function(b), n)
    return matrix
            


def mostrar_valores_registrados(matrix, n):
    ##Idea para romper el ciclo: cuando a y b sean 0 a la vez quiere decir que se llegó a una fila que no tiene elementos y que ahí se detenga la impresión
    print("f(x) = e^(2*x) - 3")#Que se imprima con LaTeX
    print("|    a   |\t|    b   |\t|   f(a)  |\t|  f(b)  |\t|    c   |\t|   f(c)  |\t| Error relativo |")
    last_row = 0
    #print(matrix)
    for i in range(matrix.shape[0]):
        if matrix[i, 0] == 0 and matrix[i, 1] == 0:
                last_row = i - 1
                break
        for j in range(matrix.shape[1]):
            if j == matrix.shape[1] - 1:
                print(f"| {round(matrix[i, j], n)} % |\t", end="")
            else: 
                print(f"| {matrix[i, j]} |\t", end="")
        print("")    

    print(f"Valor de la raíz: {matrix[last_row, 4]}")


def main():
    print("Bienvenid@ al método de Falsa Posición")
    print("Valores recomnendados: \na = 0\nb = 1")
    a = ask_for_double("el valor de a")
    b = ask_for_double("el valor de b")
    F_a = function(a)
    F_b = function(b)

    while True:
        R = F_a*F_b
        if R > 0:
            print("Proponga nuevos valores")
            a = ask_for_double("el valor de a")
            b = ask_for_double("el valor de b")
            F_a = function(a)
            F_b = function(b)
        elif R == 0:
            print("Uno de los valores ingresados corresponde a la raíz de la función")#Arreglarle lo de las cifras significativas
            print(f"Valor de a: {a:.2f}, Valor de f(a) = {F_a:.2f}")
            print(f"Valor de b: {b:.2f}, Valor de f(b) = {F_b:.2f}")
            break
        else: 
            print("Valores adecuados para el método")
            while True:
                n = ask_for_int("el número de cifras significativas con el que desea trabajar")
                if n < 1:
                    print("El número de mínimo de cifras significativas es 1, intente de nuevo")
                else: 
                    break
            matrix = ejecutar_metodo_iterativo(a, b, n)
            mostrar_valores_registrados(matrix, n)
            break

if __name__ == "__main__":
    main()

# Potencias: math.pow(base, exponente)
# Exponencial e^x: math.expo(exponente)


