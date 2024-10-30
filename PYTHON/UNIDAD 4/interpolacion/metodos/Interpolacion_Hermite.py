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

def duplicate_list(lista):
    nueva_lista = []
    for i in range(len(lista)):
        nueva_lista.append(lista[i])
        nueva_lista.append(lista[i])
    return nueva_lista


def calcular_valores_diferencias_divididas_Hermite(matrix):
    valores_diferencias_divididas = []
    valores_x = matrix[:,matrix.shape[1] - 3].tolist().copy()
    valores_y = matrix[:,matrix.shape[1] - 2].tolist().copy()
    valores_x = duplicate_list(valores_x)
    valores_y = duplicate_list(valores_y)
    valores_y_prime = matrix[:,matrix.shape[1] - 1].tolist()
    #Agregar el primer valor
    valores_diferencias_divididas.append(valores_y[0])
    n = matrix.shape[0]#número de filas
    lista1 = valores_y.copy()
    lista2 = []#Para los valores del numerador
    k = 0
    for i in range((2*n) - 1):#numero de veces q hay q iterar; n = 5
        k = (2*n) - i
        #Para la primer iteración
        if i == 0:
            m = n
            for j in range((2*n) - 1, 0, -1):#5, 3, 1
                if lista1[j] == lista1[j - 1]:
                    valor = valores_y_prime[j - m]
                    m -= 1
                else:
                    valor = valor_cifras_significativas((lista1[j] - lista1[j - 1]) / (valores_x[j] - valores_x[j - 1]), 4)
                lista2.append(valor)
        else:#k == 2
            for j in range((2*n) - 1 - i):#j empieza en 0, 
                #print("VALORES DE Y")
                #print(lista1[j])
                #print(lista1[j + 1])
                #print("VALORES DE LOS INDEX DE X")
                #print(k + i - 1)
                #print(k - 2)
                #print("VALORES DE X")
                #print(valores_x[k + i - 1])
                #print(valores_x[k - 2])
                valor = valor_cifras_significativas((lista1[j] - lista1[j + 1]) / (valores_x[k + i - 1] - valores_x[k - 2]), 4)
                lista2.append(valor)
                k -= 1
        valores_diferencias_divididas.append(lista2[-1])
        lista1 = lista2
        lista2 = []
    return valores_diferencias_divididas

def calcular_polinomio_Hermite(matrix, valores_diferencias_divididas):
    valores_x = matrix[:,matrix.shape[1] - 3].tolist().copy()
    valores_y = matrix[:,matrix.shape[1] - 2].tolist().copy()
    valores_x = duplicate_list(valores_x)
    valores_y = duplicate_list(valores_y)
    cad = ""
    n = matrix.shape[0]#número de filas
    grado = 2*(n) - 1
    for i in range(grado,-1, -1):
        if i == 0:
            if valores_diferencias_divididas[i] >= 0:
                cad += " + "
            cad += str(valores_diferencias_divididas[i]) + " "
        else:
            if valores_diferencias_divididas[i] >= 0 and i != grado:
                cad += " + "
            cad +=  str(valores_diferencias_divididas[i])
            j = 0
            while j < i:
                cad += "*"
                if valores_x[j] == valores_x[j + 1] and j != i - 1:#lo del cuadrado **2
                    cad += f"(x - {valores_x[j]})**2"
                    j += 1
                else: 
                    cad += f"(x - {valores_x[j]})"
                j += 1
    return cad
 

def ejecutar_metodo():
    matrix = np.empty((0,0))
    #Extraer datos del archivo csv
    #Esta ruta debe modificarse dependiendo de la computadora
    #import os
    #print(os.getcwd())  # Esto te muestra el directorio actual desde el que estás ejecutando Python
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 4\\interpolacion\\datos\\Datos_Interpolacion_Hermite.csv', delimiter=',')
    matrix = df.to_numpy()
    #Método de interpolacion de Hermite
    valores_diferencias_divididas = calcular_valores_diferencias_divididas_Hermite(matrix)
    polinomio = calcular_polinomio_Hermite(matrix, valores_diferencias_divididas)
    n = matrix.shape[0]#número de filas
    grado = 2*(n) - 1
    #Mostrar al usuario el polinomio calculado
    print("La función calculada es la siguiente: ")
    print(f"H_{grado}(x) = {polinomio.replace('**', '^')}")
    x = sp.symbols('x')
    function = sp.sympify(polinomio)
    derivada = sp.diff(function, x)
    #Mostrar la derivada de la función
    print("La derivada de la función calculada es la siguiente: ")
    print(f"H'_{grado}(x) = {str(derivada).replace('**', '^')}")
    #Preguntar si desea evaluar un valor de  x en la función
    while True:
        print("¿Desea evaluar un valor x?\n1. SI\n2. NO")
        ans = ask_for_int("una opción")
        if ans == 1:#un submenu
            
            while True:
                print("¿Desea sustituir el valor en la función o en su derivada?\n1. Función: H(x)\n2. Derivada: H'(x)\n3. Cancelar")
                ans2 = ask_for_int("una opción")
                if ans2 == 1:
                    value = ask_for_double("el valor de x que quiere evaluar")
                    resultado = function.subs(x, value)
                    print(f"H_{grado}({value}) = {round(resultado, 6)}")
                    break
                elif ans2 == 2:
                    value = ask_for_double("el valor de x que quiere evaluar")
                    resultado = derivada.subs(x, value)
                    print(f"H'_{grado}({value}) = {round(resultado, 6)}")
                    break
                elif ans2 == 3: break
                else: print("Se ingresó una opción inválida")
        elif ans == 2:
            break
        else:
            print("Se ingresó una opción inválida")    
                

    
        
def main():
    print("Bienvenid@ al método de interpolación de Hermite")
    print("El archivo que contiene los datos tiene el nombre de 'Datos_Interpolacion_Hermite.csv'")
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