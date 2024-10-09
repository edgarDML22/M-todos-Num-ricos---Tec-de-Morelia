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

def exportar_archivo_csv(matrix):
    np.savetxt("Valores_Metodo-Gauss-Seidel.csv", matrix, delimiter=",", fmt="%s")
    print("Se ha exportado el archivo csv!")
    print("Si desea ver los valores obtenidos durante el método abra el archivo matriz.csv con Excel")

def generar_matrix(numero_columnas): # debe ser un int >= 1
    matrix = np.array([3])
    if numero_columnas != 1:
        new_column = np.array([3])
        for i in range(numero_columnas - 1):
            matrix = np.hstack((matrix, new_column))
    return matrix    

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
    
def calcular_error_tolerable(n):
    return 0.5*(math.pow(10, 2-n))

def calcular_error_relativo(valor_anterior, valor_actual):
    return (abs(1 - (valor_anterior / valor_actual)))*100

def calcular_errores_relativos(x_i, x_j, n):
    errores = []
    for anterior, actual in zip(x_i, x_j):
        error = valor_cifras_significativas(calcular_error_relativo(anterior, actual), n)
        errores.append(error)
    return errores

def Gauss_Seidel_function(T, x_i, C, n):
    x_gauss_seidel = np.empty(x_i.size)
    for k in range(x_i.size):
        value = (vector_cifras_significativas(np.dot(T, x_i), n) + vector_cifras_significativas(C, n))[k]
        x_gauss_seidel[k] = value
        x_i[k] = value   
    x_gauss_seidel = vector_cifras_significativas(x_gauss_seidel, n)
    return x_gauss_seidel
    
def SOR_function(x_i, x_j, w, n):
    x_sor = np.empty(x_i.size)
    i = 0
    for sor_anterior,seidel in zip(x_i, x_j):
        value = w*(seidel) + (1-w)*(sor_anterior)
        x_sor[i] = value
        i += 1
    x_sor = vector_cifras_significativas(x_sor, n)
    return x_sor

def ejecutar_metodo_iterativo(n, w):
    soluciones = []
    matrix = np.empty((0,0))
    #Coeficientes de la matriz
    A = np.array([[3, -1, -1], 
              [-1, 3, 1], 
              [2, 1, 4]])
    B = np.array([1, 3, 7])#Términos independientes
    x_i = np.zeros(len(B))#Aquí se cambia el valor inicial para las variables
    D = np.diag(np.diag(A))
    D_inv = np.linalg.inv(D)
    Tx = D - A
    T = np.dot(D_inv, Tx)
    C = np.dot(D_inv, B)
    #Agregar valores inciales a la matriz
    row = 1
    error_tolerable = calcular_error_tolerable(n)

    while True:
        #Crear la fila para agregarla a la matriz de valores
        new_row = np.array([row])
        new_row = np.hstack((new_row, x_i))
        #Calcular nuevo valor para variables
        #Gauss-Seidel
        x_j = Gauss_Seidel_function(T, np.copy(x_i), C, n)
        #Aplicar SOR
        x_sor = SOR_function(x_i, x_j, w, n)
        #Meter los valores calculados a la nueva fila
        new_row = np.hstack((new_row, x_j))
        new_row = np.hstack((new_row, x_sor))
        #Calcular los errores
        if w == 1:
            errores_relativos = calcular_errores_relativos(x_i, x_j, n)
        else:
            errores_relativos = calcular_errores_relativos(x_j, x_sor, n)
        #Agregar los errores relativos a la fila
        new_row = np.hstack((new_row, errores_relativos))
        if matrix.size == 0:
            matrix = new_row
        else:
            matrix = np.vstack((matrix, new_row))
        #Verificar errores relativos
        if all(error < error_tolerable for error in errores_relativos):
            soluciones = x_j
            break
        if row > 500:
            print("No hubo convergencia, intente con otros valores")
            break
        x_i = x_sor
        row += 1
    return [matrix, soluciones]

def main():
    print("Bienvenid@ al método de Gauss-Seidel para la resolución de sistemas de ecuaciones lineales")
    while True:
        n = ask_for_int("el número de cifras significativas con el que desea trabajar")
        if n < 1:
            print("El número de mínimo de cifras significativas es 1, intente de nuevo")            
        else:                     
            break
    while True:
        w = ask_for_double("el coeficiente que desea utilizar para el SOR")
        if w < 0:
            print("El valor de w debe ser mayor a 0")
        elif w < 1:
            print("Se realizará una subrelajación")
            break
        elif w == 1:
            print("El valor de w es 1, no habrá cambio en los cálculos")
            break
        elif w < 2:
            print("Se realizará una sobrerelajación")
            break
        else:                     
            print("El valor de w es mayor o igual a 2, el sistema de ecuaciones divergerá rápidamente")

    array = ejecutar_metodo_iterativo(n , w)
    matrix = array[0]
    soluciones = array[1]
    if len(soluciones) != 0: 
        print(f"-------------------SOLUCIONES-------------------")
        for i in range(len(soluciones)):
            print(f"X_{i + 1}: {soluciones[i]}")
    exportar_archivo_csv(matrix)
    #mostrar_valores_registrados(matrix, n)
   
if __name__ == "__main__":
    main()
