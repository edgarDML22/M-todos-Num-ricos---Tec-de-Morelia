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

def calcular_suma_valores_y_Trapecio(valores_y):
    suma_valores_y = valores_y[0] + valores_y[-1]
    suma_parcial = 0
    #se suman los demás y se multiplican por 2
    for i in range(1, len(valores_y) - 1):
        suma_parcial += valores_y[i]
    suma_valores_y += 2*suma_parcial
    return suma_valores_y

def calcular_valor_Integracion_Multiple(valores_T, valores_x, valores_y):
    valor_integral = 0
    #Eliminar de la lista el límite que si se encuentra
    d = 0
    x_0 = valores_x[0]
    for i in range(1, len(valores_x)):
        if valores_x[i] == x_0:
            if d == 0:
                d = i
                break
    #suma de los trapecios con las T
    valores_trapecios = []
    k = 0
    while k < len(valores_T):
        bloque_k = []
        h = 0
        for j in range(k, k + d):
            if h == 0:
                h = valores_x[j + 1] - valores_x[j]
            bloque_k.append(valores_T[j])
        valores_trapecios.append((h/2)*(calcular_suma_valores_y_Trapecio(bloque_k))) 
        k += d
    #el paso entre las y
    y_0 = valores_y[0] 
    h_y = 0
    for y_actual in valores_y:
        if y_0 != y_actual:
            h_y = y_actual - y_0
            break
    #resultado final
    valor_integral = (h_y / 2)*(calcular_suma_valores_y_Trapecio(valores_trapecios))
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
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 5\\Integrales\\datos\\Datos_Integracion_Multiple.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_T = matrix[:,matrix.shape[1] - 3].tolist()
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    resultado = calcular_valor_Integracion_Multiple(valores_T, valores_x, valores_y)
    print("El valor de la integral es:")
    print(f"I = {valor_cifras_significativas(resultado, 6) }")


    
def main():
    print("Bienvenid@ al método de Integaración Múltiple")
    ejecutar_metodo_Newton_Cotes()

if __name__ == "__main__":
    main()