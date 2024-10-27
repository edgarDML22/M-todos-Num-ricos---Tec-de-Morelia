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


def calcular_valores_L_i(matrix):
    valores_L_i = []
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    n = calcular_grado_maximo_polinomio(matrix)
    for i in range(n + 1):#numero de iteraciones
        L_i = ""
        contador = 0
        for j in range(n + 1):
            if i != j:
                numerador = f"(x - {valores_x[j]})"
                denominador = f"({valores_x[i]} - {valores_x[j]})"#ya despues lo compactas para que sólo se haga la resta si quieres
                L_i += f"({numerador}/{denominador})"
                if contador != n - 1:
                    L_i += "*"
                contador += 1
        valores_L_i.append(L_i)
    return valores_L_i

def calcular_polinomio_Lagrange(valores_L_i, valores_y):
    cad = ""
    m = len(valores_L_i)
    for i in range(m):
        if valores_y[i] >= 0 and i != 0:
            cad += " + "
        cad += str(valores_y[i]) + "*"
        cad += valores_L_i[i]
    return cad

def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\interpolacion\\datos\\Datos_Polinomio_Lagrange.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_y = valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    #Método de polinomio de Lagrange
    valores_L_i = calcular_valores_L_i(matrix)
    polinomio = calcular_polinomio_Lagrange(valores_L_i, valores_y)
    #Mostrar al usuario el polinomio obtenido
    print("Polinomio calculado con el método")
    print(f"f_{calcular_grado_maximo_polinomio(matrix)}(x) = {polinomio}")
    #Preguntar si desea evaluar un valor de x
    x = sp.symbols('x')
    while True:
        print("¿Desea evaluar un valor x en el polinomio?\n1. SI\n2. NO")
        ans = ask_for_int("una opción")
        if ans == 1:
            value = ask_for_double("el valor de x que quiere evaluar en la función")
            function = sp.sympify(polinomio)
            resultado = function.subs(x, value)
            print(f"Y_{calcular_grado_maximo_polinomio(matrix)}({value}) = {round(resultado, 6)}")
        elif ans == 2:
            break
        else:
            print("Se ingresó una opción inválida")

def main():
    print("Bienvenid@ al método de Newton - Polinomio de interpolación de Lagrange")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Polinomio_Lagrange.csv'")
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