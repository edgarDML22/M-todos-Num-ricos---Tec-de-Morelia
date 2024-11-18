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

def calcular_primera_derivada(matrix, value):
    first_derivatives = []
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    h = valores_x[1] - valores_x[0]
    n = len(valores_x)
    for i in range(n - 1):
            if valores_x[i] <= value <= valores_x[i + 1]:#derivada de orden 1 con Taylor
                first_derivatives.append((valores_y[i + 1] - valores_y[i])/(h))
                #derivada de orden 2 con Taylor
                if i == 0:
                    first_derivatives.append((-valores_y[2] + 4*valores_y[1] - 3)/(2*h))
                elif i == n - 2:
                    first_derivatives.append((3*valores_y[i + 1] - 4*valores_y[i] + valores_y[i - 1])/(2*h))
                else:
                    first_derivatives.append((-valores_y[i + 2] + 8*valores_y[i + 1] - 8*valores_y[i] + valores_y[i - 1])/(12*h))
                break
    return first_derivatives

def calcular_segunda_derivada(matrix, value):
    second_derivatives = []
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    h = valores_x[1] - valores_x[0]
    n = len(valores_x)
    for i in range(n - 1):
            if valores_x[i] <= value <= valores_x[i + 1]:#segunda derivada de orden 1 con Taylor
                if i == 0:
                    second_derivatives.append((valores_y[i + 2] - 2*valores_y[i + 1] + valores_y[i])/(math.pow(h, 2)))
                    second_derivatives.append((-valores_y[i + 3] + 4*valores_y[i + 2] - 5*valores_y[i + 1] + 2*valores_y[i])/(math.pow(h, 2)))
                elif i == n - 2:
                    second_derivatives.append((valores_y[i + 1] - 2*valores_y[i] + valores_y[i - 1])/(math.pow(h, 2)))
                    second_derivatives.append((2*valores_y[i + 1] - 5*valores_y[i] + 4*valores_y[i - 1] - valores_y[i - 2])/(math.pow(h, 2)))
                else:
                    if valores_x[i + 1] == value:
                        second_derivatives.append((valores_y[i + 2] - 2*valores_y[i + 1] + valores_y[i])/(math.pow(h, 2)))
                        second_derivatives.append((-valores_y[i + 3] + 16*valores_y[i + 2] - 30*valores_y[i + 1] + 16*valores_y[i])/(12*(math.pow(h, 2))))
                break
    return second_derivatives


def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    #valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 5\\Derivadas\\datos\\Datos_Metodo_PRC.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    #Pedir el valor de x
    #Asegurar que esté en el rango de valores
    while True:
        x_value = ask_for_double("el valor para calcular la derivada")
        if valores_x[0] <= x_value <= valores_x[-1]:
            print("Valor adecuado para el método")
            #Método para calcular las derivadas de distinto orden
            #se guardan como una lista [] para luego presentarse
            first_derivatives = calcular_primera_derivada(matrix, x_value)
            second_derivatives = calcular_segunda_derivada(matrix, x_value)
            print("Los valores calculados fueron los siguientes")
            #mostrar primera derivada
            print("-------------------PRIMERA DERIVADA-------------------")
            print("**************** ORDEN 1 ******************")
            print(f"f'({x_value}) = {valor_cifras_significativas(first_derivatives[0], 4)}")
            print("**************** ORDEN 2 ******************")
            print(f"f'({x_value}) = {valor_cifras_significativas(first_derivatives[1], 4)}")
            #mostrar segunda derivada
            if len(second_derivatives) == 0:
                print("No se pudo calcular la segunda derivada para el valor solicitado")
            else:
                print("-------------------SEGUNDA DERIVADA-------------------")
                print("**************** ORDEN 1 ******************")
                print(f"f''({x_value}) = {valor_cifras_significativas(second_derivatives[0], 4)}")
                print("**************** ORDEN 2 ******************")
                print(f"f''({x_value}) = {valor_cifras_significativas(second_derivatives[1], 4)}")
            #Preguntar por otro valor
            print("¿Desea calcular la derivada para otro valor?\n1. SI\n2. NO")
            ans = ask_for_int("una opción")
            if ans != 1: break
        else:
            print("El valor no está dentro del rango de valores")
        
def main():
    print("Bienvenid@ al método de Progresivo, Regresivo y Central para calcular derivadas")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Metodo_PRC.csv'")
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