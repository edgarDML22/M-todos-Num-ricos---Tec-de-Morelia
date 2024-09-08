import math
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

def function(x):
    return (math.exp(2*x)-3)

def ask_for_a_and_b():
    print("Valores recomnendados: \na = 0\nb = 1")
    array = []
    array.append(ask_for_double("el valor de a"))
    array.append(ask_for_double("el valor de b"))
    return array

def valid_values_for_function(a, b):
    try:
        r = function(a) * function(b)
        return True
    except Exception as e:
        return False

def calcular_valor_C(a, b, F_a, F_b):
    return ((a * F_b) - (b * F_a)) / (F_b - F_a)

def generar_matrix(numero_columnas): # debe ser un int >= 1
    matrix = np.array([3])
    if numero_columnas != 1:
        new_column = np.array([3])
        for i in range(numero_columnas - 1):
            matrix = np.hstack((matrix, new_column))
    return matrix

def ejecutar_metodo_iterativo(A, B, n):
    matrix = generar_matrix(7)
    a = valor_cifras_significativas(A, n)
    b = valor_cifras_significativas(B, n)
    F_a = valor_cifras_significativas(function(a), n)
    F_b = valor_cifras_significativas(function(b), n)
    c = 0
    row = 0
    error_relativo = -1;
    error_tolerable = calcular_error_tolerable(n)
    while True:
        #Calcular valor de C
        c = valor_cifras_significativas(calcular_valor_C(a, b, F_a, F_b), n)
        F_c = valor_cifras_significativas(function(c), n)
        #Calcular error relativo
        if row != 0:
            error_relativo = calcular_error_relativo(matrix[row-1][4], c)
        #Meter los elementos al arreglo
        new_row = np.array([a, b, F_a, F_b, c, F_c, error_relativo])
        matrix = np.vstack((matrix, new_row))
        #Método de Falsa Posición
        if (error_relativo < error_tolerable) and row > 1:
            break
        else:
            R = F_c * F_a
            if R > 0:
                a = valor_cifras_significativas(c, n)
                F_a = valor_cifras_significativas(function(a), n)
            elif R == 0:
                break
            else:                
                b = valor_cifras_significativas(c, n)
                F_b = valor_cifras_significativas(function(b), n)
        row += 1
    return matrix
            
def mostrar_valores_registrados(matrix, n):
    print("f(x) = e^(2*x) - 3")
    print("|    a   |\t|    b   |\t|   f(a)  |\t|  f(b)  |\t|    c   |\t|   f(c)  |\t| Error relativo |")

    for i in range(matrix.shape[0]):
        if i != 0:
            for j in range(matrix.shape[1]):
                if j == matrix.shape[1] - 1:
                    print(f"| {round(matrix[i, j], n)} % |\t", end="")
                else: 
                    print(f"| {matrix[i, j]} |\t", end="")
            print("")    
    print(f"Valor de la raíz: {matrix[matrix.shape[0] - 1][4]}")

def main():
    print("Bienvenid@ al método de Falsa Posición")
    while True:
        array = ask_for_a_and_b()
        valid_values = valid_values_for_function(array[0], array[1])
        if valid_values == True:
            a = array[0]
            b = array[1]
            F_a = function(a)
            F_b = function(b)
            R = F_a*F_b
            if R > 0:
                print("No hubo un cambio de signo, proponga nuevos valores")
            elif R == 0:
                print("Uno de los valores ingresados corresponde a la raíz de la función")
                print(f"Valor de a: {a:.4f}, Valor de f(a) = {F_a:.4f}")
                print(f"Valor de b: {b:.4f}, Valor de f(b) = {F_b:.4f}")
                break
            else: 
                print("Valores adecuados para el método")
                while True:
                    n = ask_for_int("el número de cifras significativas con el que desea trabajar")
                    if n < 1:
                        print("El número de mínimo de cifras significativas debe ser mayor a 0, intente de nuevo")
                    else: 
                        break
                matrix = ejecutar_metodo_iterativo(a, b, n)
                mostrar_valores_registrados(matrix, n)
                break
        else:
            print("En alguno de los valores ingresados no está definida la función")
            print("Proponga nuevos valores")
        
if __name__ == "__main__":
    main()
