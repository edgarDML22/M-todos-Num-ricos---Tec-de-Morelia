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

def calcular_integral_Romberg(valores_x, valores_y):
    valor_integral = 0
    valores_trapecios = []
    n = m = len(valores_x) - 1#16
    h_max = valores_x[-1] - valores_x[0]
    h_min = valores_x[1] - valores_x[0]
    h_actual = h_max
    #se calculan los primeros valores con los trapecios
    while h_actual >= h_min:
        new_list = []
        i = 0
        while i <= m:
            new_list.append(valores_y[i])
            i = int(i + n)
        valores_trapecios.append((h_actual / 2)*(calcular_suma_valores_y_Trapecio(new_list)))
        h_actual /= 2
        n /= 2
    #aplicar la fórmula de 4^k - 1
    actual_values = valores_trapecios
    for k in range(2, len(valores_trapecios) + 1):
        coeficiente = math.pow(4, k-1)
        next_values = []
        for j in range(len(actual_values) - 1):
            next_values.append((coeficiente*actual_values[j + 1] - actual_values[j])/(coeficiente - 1))
        actual_values = next_values
    #devolver el resultado
    return actual_values[0]

#con la funciión
# def ejecutar_metodo_5k_segmentos(function_str, n, a, b):
#     valores = calcular_valores_xy_tabla(function_str, n, a, b)
#     valores_x = valores[0]
#     valores_y = valores[1]
#     resultado = calcular_integral_5k_segmentos(valores_x, valores_y)
#     print("El valor de la integral es:")
#     print(f"I = {valor_cifras_significativas(resultado, 6) }")

#con tabla de valores
def ejecutar_metodo_integracion_Romberg():
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 5\\Integrales\\datos\\Datos_Integracion_Romberg.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    #Verificar que h sea constante h
    #se calcula el valor de la Integral
    resultado = calcular_integral_Romberg(valores_x, valores_y)
    print("El valor de la integral es:")
    print(f"I = {valor_cifras_significativas(resultado, 6) }")

    
#2.8374
def main():
    print("Bienvenid@ al método de segmentos desiguales calcular integrales")
    ejecutar_metodo_integracion_Romberg()

if __name__ == "__main__":
    main()