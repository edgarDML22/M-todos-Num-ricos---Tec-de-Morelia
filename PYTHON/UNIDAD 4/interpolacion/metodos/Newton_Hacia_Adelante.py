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

def calcular_valores_delta(matrix):
    valores_delta = []
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_delta.append(valores_y[0])
    n = calcular_grado_maximo_polinomio(matrix)
    lista1 = valores_y.copy()
    lista1.reverse()
    lista2 = []
    
    for i in range(n):#numero de valores q hay q calcular
        for j in range(n - i):
            lista2.append(lista1[j] - lista1[j + 1])
        valores_delta.append(lista2[-1])
        lista1 = lista2
        lista2 = []
    return valores_delta

def calcular_valores_combinaciones(matrix, value, h):
    valores_combinaciones = [1]
    valores_x = matrix[:,matrix.shape[1] - 2].tolist().copy()
    n = calcular_grado_maximo_polinomio(matrix)
    k = float((value - valores_x[0]) / h)
    for i in range(1, n + 1):
        j = k
        m = 1
        L = (k-(i - 1)) #calcular el límite y meterlo en el otro ciclo
        while j >= L:
            m *= j
            j -= 1
        valores_combinaciones.append((m)/(math.factorial(i)))
    return lista_cifras_significativas(valores_combinaciones, 4)

def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\interpolacion\\datos\\Datos_Newton_Hacia_Adelante.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_x = matrix[:,matrix.shape[1] - 2]
    #Verificar que los valores tengan el mismo paso
    if verificar_paso(valores_x) == True:
        h = valores_x[1] - valores_x[0]
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
        #Método de Newton - Hacia adelante
        valores_delta = calcular_valores_delta(matrix)
        valores_combinaciones = calcular_valores_combinaciones(matrix, value, h)
        #Mostrar al usuario la operación ejecutada
        cad = f"Y_{calcular_grado_maximo_polinomio(matrix)}({value}) = "
        for i in range(len(valores_delta)):
            if valores_delta[i] >= 0 and i != 0:
                cad += "+ "
            cad += f"{valores_delta[i]}*({valores_combinaciones[i]}) "
        print("Función calculada con el método")
        print(cad)
        #Calcular el resultado
        result = 0
        for i in range(len(valores_delta)):
            result += valores_delta[i]*valores_combinaciones[i]
        print(f"Y_{calcular_grado_maximo_polinomio(matrix)}({value}) = {result}")
    else:
        print("Los valores de la tabla no tienen el mismo paso, por lo que no es posible llevar este método a cabo")
    
    
    

    
def main():
    print("Bienvenid@ al método de Newton - Hacia Adelante")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Newton_Hacia_Adelante.csv'")
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