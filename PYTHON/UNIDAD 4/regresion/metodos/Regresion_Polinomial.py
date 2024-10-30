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

def ask_for_grado_polinomio():
    while True:
        n = ask_for_int("el grado del polinomio que desea calcular")
        if n < 1:
            print("El grado mínimo del polinomio es 1")            
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

def calcular_lista_sumatorias_potencias_x(valores_x, grado, m):
    lista_potencias_x = []
    for pow in range(1, 2*grado + 1):
        lista_potencias_x.append(valor_cifras_significativas(np.sum(valores_x ** pow), m))
    return lista_potencias_x

def calcular_suma_x_times_y(valores_x, valores_y, m):
    suma_x_y = 0
    for x, y in zip(valores_x, valores_y):
        suma_x_y += valor_cifras_significativas(x*y, m)
    return suma_x_y

def calcular_lista_sumatorias_x_times_y(valores_x, valores_y, grado, m):
    lista_x_times_y = []
    for pow in range(grado + 1):
        lista_x_times_y.append(calcular_suma_x_times_y(valores_x ** pow, valores_y, m))
    return lista_x_times_y

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

def generar_sistema_ecuaciones(coeficientes_ecuaciones, lista_sumatorias_potencias_x, grado):
    #rellenar la matriz del sistema de ecuaciones
    k = 0
    for i in range(grado + 1):
        if i == 0:
            for j in range(1, grado + 1):
                coeficientes_ecuaciones[i, j] = lista_sumatorias_potencias_x[j - 1]
        else:#segunda fila en adelante, i=1
            k = i - 1
            for j in range(grado + 1):
                coeficientes_ecuaciones[i, j] = lista_sumatorias_potencias_x[k]
                k += 1
            
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

def calcular_valor_e(matrix, polinomio, m):
    valores_x = matrix[:,0]
    valores_y = matrix[:,1]
    e = 0
    x = sp.symbols('x')
    function = sp.sympify(polinomio)
    for i in range(len(valores_x)):
        y_ecuacion = valor_cifras_significativas(function.subs(x, valores_x[i]), m)
        y_tabla = valores_y[i]
        e += valor_cifras_significativas(math.pow(y_tabla - y_ecuacion, 2), m)
    return e

def calcular_sistema_ecuaciones(matrix, coeficientes_ecuaciones, terminos_independientes, grado,  m):
    valores_x = matrix[:,0]
    valores_y = matrix[:,1]
    n = len(valores_x)
    coeficientes_ecuaciones[0,0] = n
    lista_sumatorias_potencias_x = calcular_lista_sumatorias_potencias_x(valores_x, grado, m)
    lista_sumatorias_x_times_y = calcular_lista_sumatorias_x_times_y(valores_x, valores_y, grado, m)
    #rellenar la matriz del sistema de ecuaciones
    generar_sistema_ecuaciones(coeficientes_ecuaciones, lista_sumatorias_potencias_x, grado)
    #rellenar el vector de terminos independientes
    terminos_independientes[:] = lista_sumatorias_x_times_y

def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\regresion\\datos\\Datos_Regresion_Polinomial.csv', delimiter=',')
    matrix = df.to_numpy()
    #Regresión Polinomial
    m = ask_for_cifras_significativas()
    grado = ask_for_grado_polinomio()
    coeficientes_ecuaciones = np.zeros((grado + 1, grado + 1))
    terminos_independientes = np.zeros(grado + 1)
    print(coeficientes_ecuaciones)
    print(terminos_independientes)
    #Se plantea el sistema de ecuaciones
    calcular_sistema_ecuaciones(matrix, coeficientes_ecuaciones, terminos_independientes,grado, m)
    #Se resuelve el sistema y se obtiene un polinomio
    soluciones = np.linalg.solve(coeficientes_ecuaciones, terminos_independientes)
    soluciones = lista_cifras_significativas(soluciones, m)
    polinomio = obtener_polinomio(soluciones, grado)
    #Se calcula el valor del error
    e = calcular_valor_e(matrix, polinomio, m)
    #Se muestra el polinomio obtenido al usuario
    print(f"f(x) = {polinomio.replace('**', '^')} +- {e}")
    #Coeficiente de Pearson
    r = calcular_coeficiente_correlacion_Pearson(matrix, m)
    print("Coeficiente de correlación de Pearson")
    print(f"r = {valor_cifras_significativas(r, m)}")
    print("Nivel de confianza")
    print(f"r^2 = {valor_cifras_significativas(100*math.pow(r, 2), m)}%")
    
    
def main():
    print("Bienvenid@ al método de Regresión Polinomial")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Regresion_Polinomial.csv'")
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