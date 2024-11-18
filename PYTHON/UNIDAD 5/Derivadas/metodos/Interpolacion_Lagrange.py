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

def buscar_valores_x(matrix, x_value):
    index_list = []
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    n = len(valores_x)
    for i in range(n - 1):
        if valores_x[i] <= x_value <= valores_x[i + 1]:
            index_list = [i, i + 1]
            break
    #partirlo en 3 casos
    #si da el primer valor[0, 1]
    if 0 in index_list:
        index_list.append(2)
    #si da el último
    elif n - 1 in index_list:
        index_list.append(n - 2)
    else:
        index_list.append(index_list[0] - 1)
    #ordenar la lista
    index_list = sort_list(index_list.copy())
    index_list = [int(index) for index in index_list]
    return index_list

def calcular_derivadas_interpolacion_Lagrange(matrix, index_list, x_value):
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    nuevos_valores_y = []
    nuevos_valores_x = []
    j = 0
    #generar la nueva tabla
    for i in range(len(valores_x)):
        if i == index_list[j]:
            nuevos_valores_y.append(valores_y[i])
            nuevos_valores_x.append(valores_x[i])
            j += 1
        if j == 3: break
    derivatives = []
    primera = 0
    for i in range(len(nuevos_valores_y)):
        numerador = 2*x_value
        denominador = 1
        for j in range(len(nuevos_valores_x)):
            if j != i:
                numerador -= valores_x[j] #numerador
                denominador *= (nuevos_valores_x[i] - nuevos_valores_x[j])#denominador
        primera += nuevos_valores_y[i]*(numerador/denominador)
    derivatives.append(primera)
    segunda = 0
    for i in range(len(nuevos_valores_y)):
        denominador = 1
        for j in range(len(nuevos_valores_x)):
            if j != i:
                denominador *= (nuevos_valores_x[i] - nuevos_valores_x[j])#denominador
        segunda += nuevos_valores_y[i]*(2/denominador)
    derivatives.append(segunda)
    return derivatives


def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    #valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 5\\Derivadas\\datos\\Datos_Interpolacion_Lagrange.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    #Pedir el valor de x
    #Asegurar que esté en el rango de valores
    while True:
        x_value = ask_for_double("el valor para calcular la derivada")
        if valores_x[0] <= x_value <= valores_x[-1]:
            print("Valor dentro del intervalo")#está dentro del rango de valores
            #Verificar que exista una posible equidistancia
            index_list = buscar_valores_x(matrix, x_value)
            if(len(index_list) != 2):
                print("Valor adecuado para el método")
                #hacer las operaciones
                derivatives = calcular_derivadas_interpolacion_Lagrange(matrix, index_list, x_value)
                #mostrar los resultados
                print("Estas fueron las derivadas calculadas con el método")
                print(f"f'({x_value}) = {valor_cifras_significativas(derivatives[0], 6)}")
                print(f"f''({x_value}) = {valor_cifras_significativas(derivatives[1], 6)}")
                #preguntar por otro valor
                print("¿Desea calcular la derivada para otro valor?\n1. SI\n2. NO")
                ans = ask_for_int("una opción")
                if ans != 1: break
            else:
                print("Sin embargo, no existe equidistancia con los valores adyacentes")
        else:
            print("El valor no está dentro del rango de valores")
        
def main():
    print("Bienvenid@ al método de interpolación de Lagrange para calcular derivadas")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Interpolacion_Lagrange.csv'")
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