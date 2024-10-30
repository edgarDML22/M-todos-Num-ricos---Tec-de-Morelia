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

def obtener_polinomio_multivariable(soluciones, variables, ans):
    print(variables)
    x, y, z = sp.symbols(', '.join(variables))
    dependiente = variables[ans]
    cad = f"{dependiente}({', '.join(elemento for elemento in variables if elemento != dependiente)}) = "
    print(cad)
    #termino independiente
    cad += str(soluciones[0])
    print("************************")
    i = 0
    k = 1
    while i < len(soluciones) - 1:
        if variables[i] != dependiente:
            if soluciones[k] >= 0:
                cad += "+ "
            cad += f"{soluciones[k]}*{variables[i]} "
            k += 1
        i += 1
    return cad

def calcular_suma_x_times_y(valores_x, valores_y, m):
    suma_x_y = 0
    for x, y in zip(valores_x, valores_y):
        suma_x_y += valor_cifras_significativas(x*y, m)
    return suma_x_y


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

def calcular_matrix_variables_indpendientes(valores_variables_independientes, m):
    n = len(valores_variables_independientes)
    matrix = np.zeros((n + 1, n + 1), dtype=object)
    matrix[0,0] = len(valores_variables_independientes[0])
    #rellenar el borde de la matriz con las listas de valores
    for i in range(1, n + 1):
        matrix[0, i] = valores_variables_independientes[i - 1]#la primer fila
        matrix[i, 0] = valores_variables_independientes[i - 1]#la primer columna
    #Ahora si invente Roman invente, rellenar la matriz con las sumas y los productos
    for i in range(1, n + 1):#n + 1 es 3
        for j in range(1, n + 1):
            matrix[i,j] = calcular_suma_x_times_y(matrix[i, 0], matrix[0, j], m)
    #sacar las sumas de las orillas manualmente al final
    #calcular las sumas de los bordes
    for i in range(1, n + 1):
        matrix[0, i] = valor_cifras_significativas(np.sum(matrix[0 , i]), m)
        matrix[i, 0] = valor_cifras_significativas(np.sum(matrix[i , 0]), m)
    # Convertir la matriz existente a tipo float
    matrix = matrix.astype(float)
    print("Matriz al final del metodo")
    print(matrix)
    return matrix

def calcular_lista_sumatorias_independientes_times_dependiente(valores_variables_independientes, valores_variable_dependiente, m):
    n = len(valores_variables_independientes) + 1
    array_sumas_x1_times_xn = np.zeros(n)
    array_sumas_x1_times_xn[0] = np.sum(valores_variable_dependiente)
    for variable_independiente in range(n - 1):
        array_sumas_x1_times_xn[variable_independiente + 1] = calcular_suma_x_times_y(valores_variables_independientes[variable_independiente],valores_variable_dependiente, m)
    print(array_sumas_x1_times_xn)
    return array_sumas_x1_times_xn

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
          
def calcular_sistema_ecuaciones(matrix, coeficientes_ecuaciones, terminos_independientes, index, m):
    valores_variables_independientes = []#una lista de arrays
    k = matrix.shape[1]#numero de variables
    for i in range(k):
        if i != index:
            valores_variables_independientes.append(matrix[:,i])
    valores_variable_dependiente = matrix[:,index]
    #valores_x = matrix[:,0]
    #valores_y = matrix[:,1]
    #cambiarlo para generar directamente el sistema aquí
    coeficientes_ecuaciones = calcular_matrix_variables_indpendientes(valores_variables_independientes, m)
    #un arreglo con [z, xz, yz] - las sumatorias
    print("matriz de coeficientes")
    print(coeficientes_ecuaciones)
    terminos_independientes = calcular_lista_sumatorias_independientes_times_dependiente(valores_variables_independientes, valores_variable_dependiente, m)
    print("terminos independientes")
    print(terminos_independientes)
    soluciones = np.linalg.solve(coeficientes_ecuaciones, terminos_independientes)
    soluciones = lista_cifras_significativas(soluciones, m)
    return soluciones

def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\regresion\\datos\\Datos_Regresion_Multivariable.csv', delimiter=',', header=None)
    matrix = df.to_numpy()
    variables = matrix[0]
    #Regresión Multivariable
    #Preguntar cual es la variable independiente
    while True:
        print("Se tienen las siguientes variables")
        for i in range(len(variables)):
            print(f"{i + 1}. {variables[i]}")
        print("Elija la variable dependiente")
        ans = ask_for_int("una opción")
        if  1 <= ans <= len(variables):
            print(f"La variable dependiente será: {variables[ans - 1]}")
            ans -= 1
            break
        else:
            print("Opción inválida, intente de nuevo")
    #ans es el índice de la coumna de la variable dependiente
    matrix = matrix[1:].astype(float)
    m = ask_for_cifras_significativas()
    coeficientes_ecuaciones = np.zeros((len(variables), len(variables)))
    terminos_independientes = np.zeros(len(variables))
    #Se plantea el sistema de ecuaciones y se resuelve
    soluciones = calcular_sistema_ecuaciones(matrix, coeficientes_ecuaciones, terminos_independientes, ans, m)
    print(soluciones)
    #Se calcula el polinomio multivariable
    polinomio = obtener_polinomio_multivariable(soluciones, variables, ans)
    #Se calcula el valor del error
    print("Función obtenida con el método")
    print(polinomio)
    
    
def main():
    print("Bienvenid@ al método de Regresión Multivariable")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Regresion_Multivariable.csv'")
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