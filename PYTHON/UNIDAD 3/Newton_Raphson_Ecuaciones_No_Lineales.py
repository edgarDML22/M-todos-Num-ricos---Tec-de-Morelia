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
    np.savetxt("Valores_Metodo_Newton_Raphson_No_Lineal.csv", matrix, delimiter=",", fmt="%s")
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
    new_vector = np.empty(vector.shape[0])
    for i in range(vector.shape[0]):
        new_vector[i] = valor_cifras_significativas(vector[i], n)
    return new_vector

def lista_cifras_significativas(lista, n):
    new_list = []
    for i in range(len(lista)):
        new_list.append(valor_cifras_significativas(lista[i], n))
    return new_list
    
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

def calcular_errores_relativos_Edgar(new_row):
    errores = []
    n = int((new_row.size - 1) / 2) #numero de incognitas
    k = 1
    while True:
        if (k + n) >= new_row.size: break
        errores.append(calcular_error_relativo(new_row[k], new_row[k + n]))
        k += 1
    return errores

def calcular_matrix_Jacobiana(A):#valores como collection
    x, y, z = sp.symbols('x y z')
    variables = [x, y, z]
    jacobiana = np.empty((A.shape[0], A.shape[0]), dtype= object)
    for i in range(A.shape[0]):
         # Convertir la ecuación a una expresión simbólica
        expr = sp.sympify(A[i, 0])
        # Calcular la derivada parcial respecto a cada variable
        for j in range(len(variables)):
            derivada = sp.diff(expr, variables[j])
            jacobiana[i, j] = derivada
    return jacobiana

def evaluar_matrix_Jacobiana(jacobiana, valores, n):#valores como collection
    matrix = np.empty((jacobiana.shape[0], jacobiana.shape[0]))
    #valores como una collection
    for i in range(jacobiana.shape[0]):
        for j in range(jacobiana.shape[1]):
            expresion = sp.sympify(jacobiana[i, j])
            matrix[i, j] = valor_cifras_significativas(expresion.subs(valores), n)
    return matrix

def calcular_minus_f(A, B, valores, n):#valores como collection
    minus_f = np.empty(B.shape[0])
    for i in range(B.shape[0]):
        expresion = sp.sympify(A[i])
        minus_f[i] = B[i] - expresion.subs(valores)[0]
        minus_f[i] = valor_cifras_significativas(minus_f[i], n)
    return minus_f

def Newton_Raphson_Method(A, B, A_jacobiana, x_i, n):
    #x_i es una collection{x: 1, y: 2, z: 3}
    h_values = []#Aquí se van a guardar los valores de h
    x_j = []#Aquí se devolverán los siguientes valores del método
    #[C]{h_i} = [D] - Para crear el sistema de ecuaciones
    C = evaluar_matrix_Jacobiana(A_jacobiana, x_i, n)#Ya funciona
    D = calcular_minus_f(A, B, x_i, n)
    #Se resuelve el sistema de ecuaciones lineales
    h_values = np.linalg.solve(C, D).tolist()
    h_values = lista_cifras_significativas(h_values, n)
    for x_actual, h in zip(x_i.values(), h_values):
        x_j.append(valor_cifras_significativas((x_actual + h), n))
    return [h_values, x_j]


def ejecutar_metodo_iterativo(n):
    x, y, z = sp.symbols('x y z')  
    soluciones = []
    matrix = np.empty((0,0))
    #Coeficientes de la matriz
    A = np.array([["x**3+y**3-z**3"], 
              ["x**2+y**2-z**2"], 
              ["x+y-z"]])
    B = np.array([129, 9.75, 9.49])#Términos independientes
    A_jacobiana = calcular_matrix_Jacobiana(A)
    #Valores como un collection{}
    x_i = {x: 1, y: 2, z: 3} #Aquí se cambia el valor inicial para las variables
    row = 1
    error_tolerable = calcular_error_tolerable(n)

    while True:
        keys = [x, y, z]
        #Crear la fila para agregarla a la matriz de valores
        new_row = np.array([row])
        new_row = np.hstack((new_row, list(x_i.values())))
        #Calcular nuevo valor para variables
        array = Newton_Raphson_Method(A, B, A_jacobiana, x_i, n)
        h_values = array[0]#Lista
        x_j = array[1]#Lista
        x_j = lista_cifras_significativas(x_j, n)
        #Meter los valores calculados a la nueva fila
        new_row = np.hstack((new_row, h_values))
        new_row = np.hstack((new_row, x_j))
        #Calcular los errores 
        errores_relativos = calcular_errores_relativos(x_i.values(), x_j, n)
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
        x_i = dict(zip(keys, x_j))
        row += 1
    return [matrix, soluciones]

def main():
    print("Bienvenid@ al método de Jacobi para la resolución de sistemas de ecuaciones lineales")
    while True:
        n = ask_for_int("el número de cifras significativas con el que desea trabajar")
        if n < 1:
            print("El número de mínimo de cifras significativas es 1, intente de nuevo")            
        else:                     
            break
    array = ejecutar_metodo_iterativo(n)
    matrix = array[0]
    soluciones = array[1]
    if len(soluciones) != 0:
        print(f"-------------------SOLUCIONES-------------------")
        for i in range(len(soluciones)):
            print(f"X_{i + 1}: {soluciones[i]}")
        exportar_archivo_csv(matrix)
   
if __name__ == "__main__":
    main()
