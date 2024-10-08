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
    np.savetxt("Valores_Metodo_Punto_Fijo_No_Lineal.csv", matrix, delimiter=",", fmt="%s")
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

def calcular_error_absoluto(x_i, x_j, n):
    suma = 0
    for anterior, actual in zip(x_i, x_j):
        suma += math.pow(actual - anterior, 2)
    return valor_cifras_significativas(math.sqrt(suma), n)

def Punto_Fijo_Method(G, x_i, n): #Hecho con Gauss-Seidel
    x, y, z = sp.symbols('x, y, z')
    keys = [x, y]
    valores = list(x_i.values()) #[0, 1]
    nuevos_valores = []
    #x_i es una collection {x: 0, y: 0}
    #Calcula los nuevos valores con Gauss-Seidel
    for i in range(len(x_i)):
        expresion = sp.sympify(G[i, 0])
        value = valor_cifras_significativas(expresion.subs(dict(zip(keys, valores))), n)#el argumento debe ser una collection
        nuevos_valores.append(value)
        valores[i] = value
    return nuevos_valores

def calcular_funciones(F, x_j, n):#x_j es una lista
    funciones = []
    for i in range(len(x_j)):
        expresion = sp.sympify(F[i, 0])
        value = valor_cifras_significativas(expresion.subs(x_j), n)
        funciones.append(value)
    return funciones


def ejecutar_metodo_iterativo(n):
    x, y, z = sp.symbols('x y z')  
    soluciones = []
    matrix = np.empty((0,0))
    #Funciones originales (f_i)
    F = np.array([["x**2+y*x-10"], ["y + 3*x*y**2 - 57"]])
    #Funciones despejadas (g_i)
    G = np.array([["sqrt((10-x*y))"], ["sqrt((57-y)/(3*x))"]])
    #Valores como un collection{}
    x_i = {x: 0, y: 0} #Aquí se cambia el valor inicial para las variables
    row = 1
    error_tolerable = calcular_error_tolerable(n)

    while True:
        keys = [x, y]
        #Crear la fila para agregarla a la matriz de valores
        new_row = np.array([row])
        new_row = np.hstack((new_row, list(x_i.values())))
        #Calcular nuevo valor para variables
        x_j = Punto_Fijo_Method(G, x_i, n) #Lista
        x_j = lista_cifras_significativas(x_j, n)
        #Calcular el valor de las funciones
        functions = calcular_funciones(F, dict(zip(keys, x_j)), n)
        functions = lista_cifras_significativas(functions, n)
        #Meter los valores calculados a la nueva fila
        new_row = np.hstack((new_row, x_j))
        new_row = np.hstack((new_row, functions))
        #Calcular error absoluto
        error_absoluto = calcular_error_absoluto(x_i.values(), x_j, n)
        new_row = np.hstack((new_row, error_absoluto))
        #Calcular los errores relativos
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
    print("Bienvenid@ al método de Punto FIjo para la resolución de sistemas de ecuaciones no lineales")
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
