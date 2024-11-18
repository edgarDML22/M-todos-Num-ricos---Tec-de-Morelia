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

def verificar_equidistancia(valores_x):
    h = valores_x[1] - valores_x[0]
    error_tolerable = 1/(math.pow(10, 4))
    for i in range(1, len(valores_x) - 1):
        new_h = valores_x[i + 1] - valores_x[i]
        if abs(new_h - h) > error_tolerable: 
            return False
    return True


def calcular_valores_xy_tabla(function_str, h, a, b):
    x = sp.symbols('x')
    function = sp.sympify(function_str)
    #para los valores de x
    valores_x = []
    i = a
    while i <= b:
        valores_x.append(i)
        i += h
    #sustituirlos en la función y sumarlos
    valores_y = []
    for value in valores_x:
        valores_y.append(valor_cifras_significativas(function.subs(x, value), 6))
        print(f"{valor_cifras_significativas(value, 6)}, {valor_cifras_significativas(function.subs(x, value), 6)}") #Para obtener como un csv en la consola
    return [valores_x, valores_y]

def calcular_integral_Newton_Cotes(valores_x, valores_y, a, b):
    valor_integral = 0
    #Eliminar de la lista el límite que si se encuentra
    index = 0
    if valores_x[-1] == b:    
        index = -1
    valores_x.pop(index)
    valores_y.pop(index)
    n = len(valores_x)
    c = b-a
    if n == 1:
        valor_integral = (c)*valores_y[0]
    elif n == 2:
        valor_integral = (c/2)*(valores_y[0] + valores_y[1])
    elif n == 3:
        valor_integral = (c/3)*(2*valores_y[0] + valores_y[1] + 2*valores_y[2])
    elif n == 4:
        valor_integral = (c/24)*(11*valores_y[0] + valores_y[1] + valores_y[2] + 11*valores_y[3])
    else:
        valor_integral = (c/20)*(11*valores_y[0] + 14*valores_y[1] + 26*valores_y[2] + 14*valores_y[3] + 11*valores_y[4])
    return valor_integral

#con la funciión
# def ejecutar_metodo_5k_segmentos(function_str, n, a, b):
#     valores = calcular_valores_xy_tabla(function_str, n, a, b)
#     valores_x = valores[0]
#     valores_y = valores[1]
#     resultado = calcular_integral_5k_segmentos(valores_x, valores_y)
#     print("El valor de la integral es:")
#     print(f"I = {valor_cifras_significativas(resultado, 6) }")

#con tabla de valores
def ejecutar_metodo_Newton_Cotes():
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 5\\Integrales\\datos\\Datos_Newton_Cotes.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    a_tabla = valores_x[0]
    b_tabla = valores_x[-1]

    #obtener los límites de integración
    while True:
        if len(valores_x) > 5:
            print("La tabla cuenta con más de 5 pares de valores")
            break
        print("Ingrese los límites de integración")
        a = ask_for_double("el valor de a")
        b = ask_for_double("el valor de b")
        if a != a_tabla or b != b_tabla:
                #cumple las condiciones
                #ahora hay que ver si hay que quitar el valor de a o de b de la tabla de valores
                resultado = calcular_integral_Newton_Cotes(valores_x, valores_y, a, b)
                print("El valor de la integral es:")
                print(f"I = {valor_cifras_significativas(resultado, 6) }")
                break
        else:
            print("Los límites de integración proporcionados se encuentran en la tabla de valores")
            print("Este método sólo debe utilizarse cuando no se encuentra uno de los límites de integración")
        print("¿Desea ingresar nuevamente los límites de integración?\n1. SI\n2. NO")
        ans = ask_for_int("Ingrese una opción")
        if ans != 1: break

    
def main():
    print("Bienvenid@ al método de Newton-Cotes calcular integrales")
    ejecutar_metodo_Newton_Cotes()

if __name__ == "__main__":
    main()