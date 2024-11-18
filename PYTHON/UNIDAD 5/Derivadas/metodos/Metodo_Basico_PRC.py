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

def calcular_derivada_PRC(matrix, value):
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    for i in range(len(valores_x) - 1):
            if valores_x[i] <= value <= valores_x[i + 1]:
                return ((valores_y[i + 1] - valores_y[i])/(valores_x[i + 1] - valores_x[i]))
        

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
            #Método para calcular la pendiente
            derivative = calcular_derivada_PRC(matrix, x_value)
            print("El valor calculado es el siguiente:")
            print(f"f'({x_value}) = {valor_cifras_significativas(derivative, 4)}")
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