import pandas as pd
import numpy as np
import sympy as sp
import math


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

def ask_for_cifras_significativas():
    while True:
        n = ask_for_int("el número de cifras significativas con el que desea trabajar")
        if n < 1:
            print("El número de mínimo de cifras significativas es 1, intente de nuevo")            
        else: return n                  
            
def exportar_archivo_csv(matrix):
    np.savetxt("Valores_Metodo-Gauss-Seidel.csv", matrix, delimiter=",", fmt="%s")
    print("Se ha exportado el archivo csv!")
    print("Si desea ver los valores obtenidos durante el método abra el archivo matriz.csv con Excel")

def valor_cifras_significativas(numero, n):
    if numero == 0:
        return 0
    else:
        numero_float = float(numero) 
        factor = n - (int(f"{numero_float:e}".split('e')[1]) + 1)
        return round(numero_float, factor)
    
def vector_cifras_significativas(vector, n):
    new_vector = np.empty(vector.size)
    for i in range(vector.size):
        new_vector[i] = valor_cifras_significativas(vector[i], n)
    return new_vector

def lista_cifras_significativas(lista, n):
    new_list = []
    for i in range(len(lista)):
        new_list.append(valor_cifras_significativas(lista[i], n))
    return new_list

def sort_list(lista):
    flag = False
    while not flag:
        flag = True
        for i in range(len(lista) - 1):
            if lista[i] > lista[i + 1]:
                aux = lista[i]
                lista[i] = lista[i + 1]
                lista[i + 1] = aux
                flag = False
    return [float(valor) for valor in lista]

def calcular_valor_integral_Rectangulos(function_str, n, a, b):
    x = sp.symbols('x')
    function = sp.sympify(function_str)
    h = (b - a)/n
    #para los valores de x
    valores_x = []
    i = a
    while i <= b:
        valores_x.append(i)
        i += h
    #para las medias
    medias_x = []
    for i in range(len(valores_x) - 1):
        medias_x.append((valores_x[i] + valores_x[i + 1]) / 2)
    #sustituirlos en la función y sumarlos
    suma = 0
    for value in medias_x:
        suma += valor_cifras_significativas(function.subs(x, value), 6)
    resultado = h*suma
    return resultado

def ejecutar_metodo(function_str, n, a, b):
    resultado = calcular_valor_integral_Rectangulos(function_str, n, a, b)
    print("El valor de la integral es:")
    print(f"I = {valor_cifras_significativas(resultado, 6) }")

def main():
    print("Bienvenid@ al método del rectángulo para calcular integrales")
    print("La función es la siguiente:")
    function_str = "exp(x**4)"#aqui se cambia la función como un String
    print(f"f(x) = {function_str}")
    #numero de rectangulos
    while True:
        print("Ingrese el número de rectángulos con el que desea trabajar")
        n = ask_for_int("valor de n")
        if n >= 1: break
        else: print("El número de rectángulos mínimo es 1")
    #límites de integración
    print("Ingrese los límites de integración")
    a = ask_for_double("el valor de a")
    b = ask_for_double("el valor de b")
    #calcular y mostrar el valor de la integral
    ejecutar_metodo(function_str, n, a, b)
    #print("El archivo que contiene los datos tiene el nombre de 'Datos_Interpolacion_Lagrange.csv'")
    #print("Si desea modificar algún dato, este es el momento de hacerlo")

    # while True:
    #     print("¿Desea continuar con el método?\n 1. SI\n 2. NO")
    #     ans = ask_for_int("opción numérica")
    #     if ans == 1 or ans == 2: break
    #     else: print("Opción inválida, intente de nuevo")
    # if ans == 1:
    #     print("Espere mientras se ejecuta el programa...")
    #     ejecutar_metodo()
    # else:
    #     print("Se detuvo la ejecución del programa")
    
   
if __name__ == "__main__":
    main()