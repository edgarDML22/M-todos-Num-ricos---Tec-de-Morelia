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

def calcular_grado_maximo_polinomio(matrix):
    return int(matrix[matrix.shape[0] - 1, 0])

def obtener_polinomio(soluciones, grado):
    cad = ""
    for i in range(grado,-1, -1):
        if soluciones[i] >= 0 and i != grado:
            cad += "+ "
        cad +=  str(soluciones[i])
        if i == 1:
            cad += "*x" + " "
        elif i != 0:
            cad += "*x**" + str(i) + " "
    return cad


def calcular_valor_metodo_lineal(matrix, value):
    valor_metodo_lineal = []
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    for i in range(len(valores_x) - 1):
        if valores_x[i] <= value <= valores_x[i + 1]:
            valor_metodo_lineal.append(f"f({valores_x[i]}) + ((f({valores_x[i + 1]}) - f({valores_x[i]}))/(({valores_x[i + 1]}) - {valores_x[i]}))")
            valor_metodo_lineal.append(f"{valores_y[i]} + (({valores_y[i + 1]} - {valores_y[i]})/(({valores_x[i + 1]}) - {valores_x[i]}))")
            valor_metodo_lineal.append(valores_y[i] + ((valores_y[i + 1] - valores_y[i])/((valores_x[i + 1]) - valores_x[i])))
            break
    return valor_metodo_lineal

def calcular_suma_x_times_y(valores_x, valores_y, m):
    suma_x_y = 0
    for x, y in zip(valores_x, valores_y):
        suma_x_y += valor_cifras_significativas(x*y, m)
    return suma_x_y

def calcular_coeficiente_correlacion_Pearson(matrix, m):
    valores_x = matrix[:,0]
    valores_y = matrix[:,1]
    n = len(valores_x)
    suma_x = np.sum(valores_x)
    suma_y = np.sum(valores_y)
    suma_x_y = calcular_suma_x_times_y(valores_x, valores_y , m)
    suma_cuadrados_x = valor_cifras_significativas(np.sum(valores_x ** 2), m)
    suma_x_al_cuadrado = valor_cifras_significativas(math.pow(suma_x, 2), m)
    suma_cuadrados_y = valor_cifras_significativas(np.sum(valores_y ** 2), m)
    suma_y_al_cuadrado = valor_cifras_significativas(math.pow(suma_y, 2), m)
    r = ((n*suma_x_y - suma_x*suma_y)/(math.sqrt(n*suma_cuadrados_x - suma_x_al_cuadrado) * math.sqrt(n*suma_cuadrados_y - suma_y_al_cuadrado)))
    return r

def calcular_valor_a_1(matrix, m):
    valores_x = matrix[:,0]
    valores_y = matrix[:,1]
    n = len(valores_x)
    suma_x = np.sum(valores_x)
    suma_y = np.sum(valores_y)
    suma_x_y = calcular_suma_x_times_y(valores_x, valores_y , m)
    suma_cuadrados_x = valor_cifras_significativas(np.sum(valores_x ** 2), m)
    suma_x_al_cuadrado = valor_cifras_significativas(math.pow(suma_x, 2), m)
    a_1 = valor_cifras_significativas(((n*suma_x_y - suma_x*suma_y)/(n*suma_cuadrados_x - suma_x_al_cuadrado)), m)
    return a_1

    
def calcular_valor_a_0(matrix, a_1, m):
    valores_x = matrix[:,0]
    valores_y = matrix[:,1]
    n = len(valores_x)
    suma_x = np.sum(valores_x)
    suma_y = np.sum(valores_y)
    media_x = valor_cifras_significativas(suma_x/ n, m)
    media_y = valor_cifras_significativas(suma_y/ n, m)
    a_0 = valor_cifras_significativas(media_y - (a_1*media_x), m)
    return a_0

def calcular_valor_e(matrix, a_0, a_1, m):
    e = 0
    valores_x = matrix[:,0]
    valores_y = matrix[:,1]
    for x, y in zip(valores_x, valores_y):
        e += valor_cifras_significativas(math.pow(y - a_0 - a_1*x, 2), m)
    print(e)
    return e

def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\regresion\\datos\\Datos_Regresion_Lineal.csv', delimiter=',')
    matrix = df.to_numpy()
    #Método de Newton - Metodo Lineal
    m = ask_for_cifras_significativas()
    a_1 = calcular_valor_a_1(matrix, m)
    a_0 = calcular_valor_a_0(matrix, a_1, m)
    e = calcular_valor_e(matrix, a_0, a_1, m)
    print("La ecuación de regresión calculada fue la siguiente:")
    print(f"y = {a_0} + {a_1}x +- {e}")
    r = calcular_coeficiente_correlacion_Pearson(matrix, m)
    print("Coeficiente de correlación de Pearson")
    print(f"r = {valor_cifras_significativas(r, m)}")
    print("Nivel de confianza")
    print(f"r^2 = {valor_cifras_significativas(100*math.pow(r, 2), m)}%")
    
    
    
def main():
    print("Bienvenid@ al método de Regresión Lineal")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Regresion_Lineal.csv'")
    print("Si desea modificar algún dato, este es el momento de hacerlo")

    while True:
        print("¿Desea continuar con el método?\n 1. SI\n 2. NO")
        ans = ask_for_int("opción numérica")
        if ans == 1 or ans == 2: break
        else: print("Opción inválida, intente de nuevo")
    if ans == 1:
        print("Espere mientras se ejecuta el programa...")
        ejecutar_metodo()
    else:
        print("Se detuvo la ejecución del programa")
    
   
if __name__ == "__main__":
    main()