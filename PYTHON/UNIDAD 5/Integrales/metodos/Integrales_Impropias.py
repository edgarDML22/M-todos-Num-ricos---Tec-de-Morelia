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

def is_number(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False

def is_infinity(cad):
    if cad == '+inf' or cad == '-inf':
        return True
    return False

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


#con la funciión
# def ejecutar_metodo_5k_segmentos(function_str, n, a, b):
#     valores = calcular_valores_xy_tabla(function_str, n, a, b)
#     valores_x = valores[0]
#     valores_y = valores[1]
#     resultado = calcular_integral_5k_segmentos(valores_x, valores_y)
#     print("El valor de la integral es:")
#     print(f"I = {valor_cifras_significativas(resultado, 6) }")

#METODO DEL TRAPECIO
def calcular_valores_y_Trapecio(function_str, n, a, b):
    x = sp.symbols('x')
    function = sp.sympify(function_str)
    h = (b - a)/n
    print(f"VALOR DE H:{h}")
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
        #print(f"{valor_cifras_significativas(value, 6)}, {valor_cifras_significativas(function.subs(x, value), 6)}") #Para obtener como un csv en la consola
    return valores_y

def calcular_suma_valores_y_Trapecio(valores_y):
    suma_valores_y = valores_y[0] + valores_y[-1]
    suma_parcial = 0
    #se suman los demás y se multiplican por 2
    for i in range(1, len(valores_y) - 1):
        suma_parcial += valores_y[i]
    suma_valores_y += 2*suma_parcial
    return suma_valores_y

def ejecutar_metodo_Trapecio(function_str, n, a, b):
    valores_y = calcular_valores_y_Trapecio(function_str, n, a, b)
    suma_valores_y = calcular_suma_valores_y_Trapecio(valores_y)
    h = (b - a)/n
    return (h/2)*(suma_valores_y)

#METODO DEL RECTANGULO
def calcular_valor_integral_Rectangulos(function_str, n, a, b):
    t = sp.symbols('t')
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
        suma += valor_cifras_significativas(function.subs(t, value), 6)
    resultado = h*suma
    return resultado

def ejecutar_metodo_Rectangulos(function_str, n, a, b):
    resultado = calcular_valor_integral_Rectangulos(function_str, n, a, b)
    return resultado

#con tabla de valores
def ejecutar_metodo_integrales_impropias(function_str, a, b):
    print(f"VALOR DE A: {a}")
    print(f"VALOR DE B: {b}")
    valor_integral = 0
    x, t = sp.symbols('x t')
    #function = sp.sympify(function_str)
    #3 casos, "[(1/sqrt(2*pi))*exp(-(x**2)/2)]"
    #se aplica el cambio de variable de x=1/t
    function_original = function_str
    if 'exp' in function_str:
        function_str = function_str.replace('exp', 'key_word')
        function_str = function_str = function_str.replace('x', '(1/t)')
        function_str = function_str.replace('key_word', 'exp')
    else:
        function_str = function_str.replace('x', '(1/t)')
    function_str += '*(-1/t**2)'
    #a y b son infinitos
    #sustituir x = 1/t y multiplicar por (-1/t**2)
    #obtener los nuevos límites de integración
    t_values = []
    if is_infinity(a) == True and is_infinity(b) == True:
        t_values = [0, -1, 1, 0]
    else:
        if is_infinity(a) == True:#a es -inf y b es numerico
            b = float(b)
            new_b = -2
            if b == new_b: new_b = -2
            t_values = [0, 1/new_b, 1/b]
        else:#b es +inf y a es numérico
            a = float(a)
            new_a = 1
            if b == new_a: new_b = 2
            t_values = [1/a, new_b, b]
    #calcular las integrales
    #n = 100
    for i in range(len(t_values) - 1):
        #usar rectángulo o usar trapecio
        t_i = t_values[i]
        t_j = t_values[i + 1]
        if t_i != 0 and t_j != 0:#usar regla del trapecio
            n = ask_for_int("el número de segmentos para el método el trapecio")
            r = ejecutar_metodo_Trapecio(function_original, n, 1/t_i, 1/t_j)
            print(f"Valor calculado con trapecio: {r}")
            valor_integral += r
        else:
            n = ask_for_int("el número de segmentos para el método del rectángulo")
            r = ejecutar_metodo_Rectangulos(f"-{function_str}", n, t_j, t_i)
            print(f"Valor calculado con rectángulos: {r}")
            valor_integral += r

    print("El valor de la integral es:")
    print(f"I = {valor_cifras_significativas(valor_integral, 6) }")
  


#2.8374
def main():
    print("Bienvenid@ al método para calcular integrales impropias")
    print("La función es la siguiente:")
    function_str = "((1/sqrt(2*pi))*exp(-(x**2)/2))"#aqui se cambia la función como un String
    print(f"f(x) = {function_str}")
    #límites de integración
    while True:
        print("Ingrese los límites de integración")
        print("Si desea agregar un infinito siga la siguiente nomenclatura")
        print("Para infinito escriba: +inf")
        print("Para menos infinito escriba: -inf")
        a = input("Ingrese el valor de a: ")
        b = input("Ingrese el valor de b: ")
        #Checar primero el de a y luego el de b
        flag = True
        if is_number(a) and is_number(b):
            print("Los límites de integración no son los de una integral impropia")
        else:
            if is_number(a) == False:
                if is_infinity(a) == False:
                    print("Valor de a no válido")
                    flag = False
            if is_number(b) == False:
                if is_infinity(b) == False:
                    print("Valor de b no válido")
        if flag == True:
            print("Valores adecuados para el método")
            ejecutar_metodo_integrales_impropias(function_str, a, b)
            break
        else:
            print("¿Desea intentar con otros límites de integración?")

if __name__ == "__main__":
    main()