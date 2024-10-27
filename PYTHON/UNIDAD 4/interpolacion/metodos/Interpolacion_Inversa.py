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

def calcular_coeficientes_matrix_a(matrix, index_lista, grado):
    coeficientes = np.empty(((grado + 1), (grado + 1)))
    #No considerar la columna de i
    i = 0
    for index in index_lista:
        valor = matrix[index, 1]
        for j in range(grado + 1):
            coeficientes[i,j] = math.pow(valor, j)
        i += 1
    return coeficientes

def obtener_terminos_independientes(valores_y, index_list):
    terminos_independientes = []
    for i in range(len(valores_y)):
       if i in index_list:
           terminos_independientes.append(valores_y[i])
    return terminos_independientes

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

def calcular_index_list(matrix, value):
    lista_index = []
    valores_x = matrix[:, matrix.shape[1] - 2]
    valores_y = matrix[:, matrix.shape[1] - 1]
        #Para los primeros 2 valores
    for i in range(len(valores_y) - 1):
        if valores_y[i] <= value <= valores_y[i + 1]:#lista creciente
            lista_index = [i, i + 1]
            break
        if valores_y[i] >= value >= valores_y[i + 1]:
            lista_index = [i, i + 1]
            break
    #Para el tercer valor
    if 0 in lista_index:
        lista_index.append(2)
    elif (len(valores_y) - 1) in lista_index:
        lista_index.append(len(valores_y) - 3)
    else:
        #Primero ver si hay un valor de x más cercano
        posibles_index = [lista_index[0] - 1, lista_index[1] + 1]
        if valores_x[posibles_index[0]] <= valores_x[posibles_index[1]]:
            lista_index.append(posibles_index[0])
        else:
            lista_index.append(posibles_index[1])
    #ordenar la lista
    lista_index = sort_list(lista_index.copy())
    lista_index = [int(index) for index in lista_index]
    return lista_index

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

def solve_cuadratic_equation(a_solutions, value):
    a = a_solutions[2]
    b = a_solutions[1]
    c = a_solutions[0] - value
    d = math.pow(b, 2) - (4*a*c)
    if d < 0:
        return []
    else: 
        x1 = (-b + math.sqrt(d)) / (2*a)
        x2 =  (-b - math.sqrt(d)) / (2*a)
        return [x1, x2]


def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\interpolacion\\datos\\Datos_Interpolacion_Inversa.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_x = matrix[:,matrix.shape[1] - 2]
    valores_y = matrix[:, matrix.shape[1] - 1]
    #---------------Pedir el valor de f(x)------------------------
    sorted_values_y = sort_list(valores_y.copy())
    while True:
        value = ask_for_double("el valor de f(x)")
        if value <= sorted_values_y[0] or value >= sorted_values_y[len(valores_y) - 1]:
            print("El valor proporcionado no se encuentra dentro de los datos proporcionados en la tabla")
            print("Ingrese un valor válido para continuar con el método")
        if value in valores_y:
            print("El valor ingresado ya está contenido en la tabla")
            index = valores_y.index(value)
            print(f"El valor de x correspondiente es: {matrix[index, 1]}")
        else:
            print("Valor adecuado para el método")
            break
    #------------------Elegir los 3 pares de valores para el método-----------------
    index_list = calcular_index_list(matrix, value)
    #-----------------------Metodo de coeficientes interpolantes-----------------------
    grado = 2
    #Calcular los coeficientes de la matrix a_o, a_1 y a_2
    A = calcular_coeficientes_matrix_a(matrix, index_list, grado)
    B = obtener_terminos_independientes(valores_y, index_list)#coeficientes del vector de terminos independientes de las filas
    a_solutions = lista_cifras_significativas(list(np.linalg.solve(A, B)), 4)
    function_str = obtener_polinomio(a_solutions, grado)
    #Mostrar el polinomio obtenido
    print("La función calculada con el método es la siguiente")
    print(f"f(x) = {function_str.replace('**', '^')}")
    #--------------------------------------------------------------------------------------
    #Obtener soluciones de la ecuación cuadrática
    solutions = solve_cuadratic_equation(a_solutions, value)
    if len(solutions) == 0:
        print("La ecuación calculada con el método no tiene solución en los números reales")
    else:
        #Decidir que valor de x tomar
        print("Las soluciones calculadas son las siguientes: ")
        print(f"X1 = {solutions[0]}")
        print(f"X2 = {solutions[1]}")
        print("Sin embargo, el valor que cumple con el intervalo de valores es: ")
        if  valores_x[index_list[0]] <= solutions[0] <= valores_x[index_list[2]]:
            print(f"X1 = {solutions[0]}")
        else:
            print(f"X2 = {solutions[1]}")

def main():
    print("Bienvenid@ al método de Interpolación Inversa")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Interpolacion_Inversa.csv'")
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