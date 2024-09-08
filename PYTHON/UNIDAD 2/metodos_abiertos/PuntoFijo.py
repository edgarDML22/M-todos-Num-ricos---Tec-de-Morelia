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

def function_f(x):
    return math.log(math.sin(x)) + math.exp(math.tan(x))
    #return 2*(math.exp(math.pow(x, 2))) - 5*x
    #return math.exp(x) - 4*x

def function_g(x):#probar lo de valor + function(f) avr si da lo mismo
    return x + function_f(x)
    #return 0.4*(math.exp(math.pow(x, 2)))
    #return 0.25*(math.exp(x))
    
    #return (0.25*(math.exp(valor)))

def ejecutar_metodo_iterativo(x, n):
    ##Devolver en una lista en 0: la matriz y en 1 el número de filas
    ##Puedes obtener el número de filas con la función shape
    matrix = np.array([-1, -1, -1, -1, -1])
    x_i = valor_cifras_significativas(x, n)
    F_xi = 0
    x_j = 0
    row = 0
    error_relativo = -1;
    error_tolerable = calcular_error_tolerable(n)
    while True:
        F_xi = valor_cifras_significativas(function_f(x_i), n)
        x_j = valor_cifras_significativas(function_g(x_i), n)
        #Calcular error relativo
        if row != 0:
            error_relativo = calcular_error_relativo(matrix[row-1][3], x_j)#Corregir
        #Meter los elementos al arreglo
        new_row = np.array([row, x_i, F_xi, x_j, error_relativo])
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
    return matrix
            
def mostrar_valores_registrados(matrix, n):
    ##Idea para romper el ciclo: cuando a y b sean 0 a la vez quiere decir que se llegó a una fila que no tiene elementos y que ahí se detenga la impresión
    print("f(x) = e^x - 4x")#Que se imprima con LaTeX
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

    last_row = matrix.shape[0] - 1
    print(f"Valor de la raíz: {matrix[last_row][1]}")

def main():
    print("Bienvenid@ al método de Punto Fijo")
    print("Valor recomnendado: x_i = 0")
    #Validar que la función exista en este punto
    x_i = -1
    while True:
        try:
            x_i = ask_for_double("un valor para x_i")
            r = function_f(x_i)
            print("Valor adecuado para el método")
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

# Potencias: math.pow(base, exponente)
# Exponencial e^x: math.expo(exponente)


