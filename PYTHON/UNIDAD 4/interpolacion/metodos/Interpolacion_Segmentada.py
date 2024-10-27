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

def obtener_polinomios_cuadraticos(soluciones):
    lista_polinomios = []
    grado = 2
    k = 0#es para el numero de polinomios
    i = 0#para la posicion en el vector solucion
    print(len(soluciones))
    while k < (len(soluciones) + 1) / 3:#numero de polinomios
        cad = ""
        if k == 0:#el primer polinomio es una recta
            for j in range(grado - 1,-1, -1):
                print(f"VALOR DE i: {i}")
                if soluciones[i] >= 0 and j != grado - 1:
                    cad += "+ "
                cad +=  str(soluciones[i])
                if j == 1:
                    cad += "*x" + " "
                i += 1
        else:#Para los demás polinomios cuadraticos
            for j in range(grado,-1, -1):
                if soluciones[i] >= 0 and j != grado:
                    cad += "+ "
                cad +=  str(soluciones[i])
                if j == 1:
                    cad += "*x" + " "
                elif j != 0:
                    cad += "*x**" + str(j) + " "
                i += 1
        lista_polinomios.append(cad)
        k += 1 
        print(lista_polinomios)
    return lista_polinomios

def calcular_valores_regla1(matrix, coeficientes_ecuaciones, terminos_independientes, n):
    valores_x = matrix[:,matrix.shape[1] - 2]
    valores_y = matrix[:, matrix.shape[1] - 1]
    #k es el número de filas
    k = matrix.shape[0]
    #Te tienen que salir 4*((k / 2) - 1) ecuaciones en este método
    #Ya de paso no incluyas los de a_0 pq es siempre 0
    #i son las posiciones del vector
    #n es el número de ecuaciones
    #k es el número de pares ordenados o filas de la tabla
    #4*((k / 2) - 1) es el número de ecuaciones que van a salir en este método
    #j es el iterador para saber cuantas ecuaciones llevamos
    j = 0
    i = 0
    m = 4*((k / 2) - 1)
    while j < m:
        new_vector = np.zeros(n)#poner sólo n términos(no poner el de a_o)
        if j == 0:#El primero
            valor_x = valores_x[1]
            #a_1 = 0, no se pone nada
            new_vector[0] = valor_x#b_1
            new_vector[1] = 1#c_1
            valor_y = valores_y[1]
            coeficientes_ecuaciones[0] = new_vector
            terminos_independientes[0] = valor_y
            i += 2
        elif j == (m - 1):#De la ultima ecuacion
            print("*********************ULTIMA*****************")
            valor_x = valores_x[k - 2]
            new_vector[n - 3] = math.pow(valor_x, 2)
            new_vector[n - 2] = valor_x#b_3
            new_vector[n - 1] = 1#c_3
            valor_y = valores_y[k - 2]
            coeficientes_ecuaciones[j] = new_vector
            terminos_independientes[j] = valor_y
        else: 
            #j = 1
            new_vector1 = np.zeros(n)
            new_vector2 = np.zeros(n)
            valor_x1 = valores_x[j]
            valor_x2 = valores_x[j + 1]
            #Para vector 1
            new_vector1[i] = math.pow(valor_x1, 2)#a_2
            new_vector1[i + 1] = valor_x1#b_2
            new_vector1[i + 2] = 1#c_2
            valor_y1 = valores_y[j]
            coeficientes_ecuaciones[j] = new_vector1
            terminos_independientes[j] = valor_y1
            #Para vector 2
            new_vector2[i] = math.pow(valor_x2, 2)#a_2
            new_vector2[i + 1] = valor_x2#b_2
            new_vector2[i + 2] = 1#c_2
            valor_y2 = valores_y[j + 1]
            coeficientes_ecuaciones[j + 1] = new_vector2
            terminos_independientes[j + 1] = valor_y2
            j += 1
            i += 3
        j += 1
    print(coeficientes_ecuaciones)
    print(terminos_independientes)

def calcular_valores_regla2(matrix, coeficientes_ecuaciones, terminos_independientes, n):
    valores_x = matrix[:,matrix.shape[1] - 2]
    valores_y = matrix[:, matrix.shape[1] - 1]
    k = matrix.shape[0]
    vector_0 = np.zeros(n)#el primero
    vector_n = np.zeros(n)#el ultimo
    #Para el vector 1
    vector_0[0] = valores_x[0]
    vector_0[1] = 1
    #Para el vector n
    vector_n[n - 3] = math.pow(valores_x[k - 1], 2)
    vector_n[n - 2] = valores_x[k - 1]
    vector_n[n - 1] = 1
    #Calcular cuantas ecuaciones ya van para después de eso agregar las que calculaste en la regla 2
    m = int(4*((k / 2) - 1))
    coeficientes_ecuaciones[m] = vector_0
    terminos_independientes[m] = valores_y[0]
    coeficientes_ecuaciones[m + 1] = vector_n
    terminos_independientes[m + 1] = valores_y[k - 1]
    #Comprobación
    print(coeficientes_ecuaciones)
    print(terminos_independientes)

def calcular_valores_regla3(matrix, coeficientes_ecuaciones, terminos_independientes, n):
    valores_x = matrix[:,matrix.shape[1] - 2]
    k = matrix.shape[0]
    #m es el valor de ecuaciones de la regla 1, más 2 de la segunda regla
    m = int(4*((k / 2) - 1)) + 2 #en este caso ya van 6 ecuaciones
    j = 0
    i = 0#posicion en el vector
    while j < (n - m + 1):
        if j != 0:
            vector = np.zeros(n)
            if j == 1:
                #a_1
                vector[i] = 1#b_1
                vector[i + 2] = -2*(valores_x[j])#a_2
                vector[i + 3] = -1#b_2
                i += 2
            else:
                #j = 2
                #i = 2
                print(f"VALOR DE J: {j}")
                vector[i] = 2*valores_x[j]
                vector[i + 1] = 1
                vector[i + 3] = -2*valores_x[j]
                vector[i + 4] = -1
                i += 3
            coeficientes_ecuaciones[m + j - 1] = vector
            terminos_independientes[m + j - 1] = 0#esta sobra pero mejor la pongo XD
        j+=1
    #Comprobación
    print(coeficientes_ecuaciones)
    print(terminos_independientes)
            
def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\interpolacion\\datos\\Datos_Interpolacion_Segmentada.csv', delimiter=',')
    matrix = df.to_numpy()
    print(matrix)
    if matrix.shape[0] % 2 != 0:
        print("Para trabajar este método debe proporcionarse un número par de pares de valores(x, y)")
    #numero de ecuaciones
    n = 3*(matrix.shape[0])-4
    coeficientes_ecuaciones = np.zeros((n,n))
    terminos_independientes = np.zeros(n)
    #-----------------------Metodo de interpolación segmentada cuadrática-----------------------
    #REGLA 1
    #Tomar los valores intermedios, no tomar i = 0, i = n
    calcular_valores_regla1(matrix, coeficientes_ecuaciones, terminos_independientes, n)
    #REGLA 2
    calcular_valores_regla2(matrix, coeficientes_ecuaciones, terminos_independientes, n)
    #REGLA 3
    calcular_valores_regla3(matrix, coeficientes_ecuaciones, terminos_independientes, n)
    #Resolver el sistema de ecuaciones
    A = coeficientes_ecuaciones
    B = terminos_independientes
    solutions = lista_cifras_significativas(list(np.linalg.solve(A, B)), 4)
    #Formar el polinomio como str
    lista_polinomios = obtener_polinomios_cuadraticos(solutions)
    #--------------------------------------------------------------------------------------
    print("Las funciones calculadas con el método son las siguientes")
    for i in range(len(lista_polinomios)):
        print(f"f_{i + 1}(x) = {lista_polinomios[i].replace('**', '^')}")
    
    
def main():
    print("Bienvenid@ al método de Interpolación Segementada")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Interpolacion_Segmentada.csv'")
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