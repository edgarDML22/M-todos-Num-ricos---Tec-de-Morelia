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

def calcular_coeficientes_matrix_a(matrix, grado):
    coeficientes = np.empty(((grado + 1), (grado + 1)))
    #No considerar la columna i
    for i in range(grado + 1):
        valor = matrix[i, 1]
        for j in range(grado + 1):
            coeficientes[i,j] = math.pow(valor, j)
    return coeficientes

def obtener_polinomio(soluciones, grado):
    cad = ""
    for i in range(grado,-1, -1):
        if soluciones[i] >= 0 and i != grado:
            cad += "+ "
        cad +=  str(soluciones[i])
        if i != 0:
            cad += "*x**" + str(i) + " "
    return cad

def ejecutar_metodo_iterativo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\Datos_Metodo_Coeficientes_Interpolantes.csv', delimiter=',')
    matrix = df.to_numpy()
    #-----------------------Metodo de coeficientes interpolantes-----------------------
    #Se calcula el grado máximo del polinomio
    grado = calcular_grado_maximo_polinomio(matrix)
    #Calcular los coeficientes de la matrix a_o, a_i...
    A = calcular_coeficientes_matrix_a(matrix, grado)
    B = matrix[:, matrix.shape[1] - 1]#coeficientes del vector de terminos independientes
    solutions = lista_cifras_significativas(list(np.linalg.solve(A, B)), 4)
    #Formar el polinomio como str
    function_str = obtener_polinomio(solutions, grado)
    #--------------------------------------------------------------------------------------
    print("La función calculada con el método es la siguiente")
    print(f"f(x) = {function_str.replace('**', '^')}")
    #print(f"f(x) = {function_str.replace("**", "^")}")
    #Preguntar al usuario si desea obtener algún valor
    x = sp.symbols('x')
    function = sp.sympify(function_str)
    while True:
        print("¿Desea evaluar la función en algún punto?\n1. SI\n2. NO")
        ans = ask_for_int("una opción")
        if ans == 1:
            value = ask_for_double("el valor")
            result = function.subs({x:value})
            print(f"El valor para f({value}) es: {round(result, 4)}")
        else:
            break

        
    

def main():
    print("Bienvenid@ al método de Coeficientes Interpolantes para la resolución de sistemas de ecuaciones lineales")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Metodo_Coeficientes_Interpolantes.csv'")
    print("Si desea modificar algún dato, este es el momento de hacerlo")

    while True:
        print("¿Desea continuar con el método?\n 1. SI\n 2. NO")
        ans = ask_for_int("opción numérica")
        if ans == 1 or ans == 2: break
        else: print("Opción inválida, intente de nuevo")
    if ans == 1:
        print("Espere mientras se ejecuta el programa...")
        ejecutar_metodo_iterativo()
    else:
        print("Se detuvo la ejecución del programa")
    
   
if __name__ == "__main__":
    main()