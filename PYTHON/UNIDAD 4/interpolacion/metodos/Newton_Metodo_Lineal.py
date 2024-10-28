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

def verificar_paso(valores_x):
    n = 0
    for i in range(len(valores_x) - 2):
        if i == 0:
            n = valores_x[i + 1] - valores_x[i]
        else: 
            if valores_x[i + 1] - valores_x[i] != n:
                return False
    return True

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

def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\interpolacion\\datos\\Datos_Newton_Metodo_Lineal.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_x = matrix[:,matrix.shape[1] - 2]
    #Pedir el valor de x
    valor_min = min(valores_x)
    valor_max = max(valores_x)
    while True:
        print("Proporcione el punto para evaluar la función")
        value = ask_for_int("el valor")
        if valor_min < value < valor_max:
            print("Valor adecuado para el método")
            break
        else:
            print("El valor proporcionado debe estar dentro del siguiente intervalo: ")
            print(f"{valor_min} < x < {valor_max}")
    #Método de Newton - Metodo Lineal
    valor_metodo_lineal = calcular_valor_metodo_lineal(matrix, value)#una lista
    #Mostrar al usuario la operación ejecutada
    print("La operación llevada a cabo fue la siguiente:")
    for operacion in valor_metodo_lineal:
        print(f"f({value}) = {operacion}")
    
    
    
def main():
    print("Bienvenid@ al método de Newton - Función Lineal")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Newton_Metodo_Lineal.csv'")
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