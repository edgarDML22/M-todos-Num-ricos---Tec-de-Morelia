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

def sort_list(lista):
    flag = False
    while not flag:
        flag = True
        for i in range(len(lista) - 1):
            if lista[i] > lista[i + 1]:
                aux = lista[i]
                lista[i] = lista[i + 1]
                lista[i + 1] = aux
                flag = False
    return [float(valor) for valor in lista]

def calcular_valores_y_Simpson_Un_Tercio(function_str, n, a, b):
    x = sp.symbols('x')
    function = sp.sympify(function_str)
    h = (b - a)/n
    #para los valores de x
    valores_x = []
    i = a
    while i <= b:
        valores_x.append(i)
        i += h
    #sustituirlos en la función y sumarlos
    valores_y = []
    for value in valores_x:
        valores_y.append(valor_cifras_significativas(function.subs(x, value), 6))
        #print(f"{valor_cifras_significativas(value, 6)}, {valor_cifras_significativas(function.subs(x, value), 6)}") #Para obtener como un csv en la consola
    return valores_y

def calcular_suma_valores_y_Simpson_Un_Tercio(valores_y):
    suma_valores_y = valores_y[0] + valores_y[-1]
    suma_parcial = 0
    #se suman los demás y se multiplican por 2
    for i in range(1, len(valores_y) - 1):
        if i % 2 == 0:
            suma_parcial += 2*valores_y[i]
        else:
            suma_parcial += 4*valores_y[i]
    suma_valores_y += suma_parcial
    return suma_valores_y

#con la funciión
def ejecutar_metodo_Simpson_Un_Tercio(function_str, n, a, b):
    valores_y = calcular_valores_y_Simpson_Un_Tercio(function_str, n, a, b)
    suma_valores_y = calcular_suma_valores_y_Simpson_Un_Tercio(valores_y)
    h = (b - a)/n
    resultado = (h/3)*(suma_valores_y)
    print("El valor de la integral es:")
    print(f"I = {valor_cifras_significativas(resultado, 6) }")

#con tabla de valores
def ejecutar_metodo_Simpson_Un_Tercio_tabla():
    df = pd.read_csv('C:\\Users\\EDGAR\\Desktop\\EDGAR\\SCHOOL\\TEC DE MORELIA\\TERCER SEMESTRE\\MÉTODOS NUMÉRICOS\\PYTHON\\UNIDAD 5\\Integrales\\datos\\Datos_Regla_Simpson_Un_Tercio.csv', delimiter=',')
    matrix = df.to_numpy()
    valores_y = matrix[:,matrix.shape[1] - 1].tolist()
    valores_x = matrix[:,matrix.shape[1] - 2].tolist()
    #se cacula el valor de h
    a = valores_x[0]
    b = valores_x[-1]
    n = len(valores_x) - 1
    h = (b - a)/n
    #se calcula la suma de los valores de y
    suma_valores_y = calcular_suma_valores_y_Simpson_Un_Tercio(valores_y)
    #se calcula el valor de la Integral
    resultado = (h/3)*(suma_valores_y)
    print("El valor de la integral es:")
    print(f"I = {valor_cifras_significativas(resultado, 6) }")


def main():
    print("Bienvenid@ al método de Simpson 1/3 para calcular integrales")
    while True:
        print("Indique que tipo de datos se están proporcionando")
        print("1. La función\n2. Tabla de valores x y y")
        ans = ask_for_int("una opción")
        if ans == 1 or ans == 2: break
        else: print("Se ingresó una opción inválida")
    if ans == 1:
        print("La función es la siguiente:")
        function_str = "exp(x**4)"#aqui se cambia la función como un String
        print(f"f(x) = {function_str}")
        while True:
            print("Ingrese el número de rectángulos con el que desea trabajar")
            print("Para este método el número de segmentos DEBE SER PAR")
            n = ask_for_int("valor de n")
            if n >= 1:
                if n % 2 == 0:
                    break
                else:
                    print("El número de segmentos ingresados no es par") 
            else: print("El número de rectángulos mínimo es 1")
            #límites de integración
        print("Ingrese los límites de integración")
        a = ask_for_double("el valor de a")
        b = ask_for_double("el valor de b")
        #calcular y mostrar el valor de la integral
        ejecutar_metodo_Simpson_Un_Tercio(function_str, n, a, b)

    else:
        print("El archivo que contiene los datos tiene el nombre de 'Datos_Regla_Simpson_Un_Tercio.csv'")
        print("Si desea modificar algún dato, este es el momento de hacerlo")
        while True:
            print("¿Desea continuar con el método?\n 1. SI\n 2. NO")
            ans2 = ask_for_int("opción numérica")
            if ans2 == 1 or ans2 == 2: break
            else: print("Opción inválida, intente de nuevo")
        if ans2 == 1:
            print("Espere mientras se ejecuta el programa...")
            ejecutar_metodo_Simpson_Un_Tercio_tabla()
        else:
            print("Se detuvo la ejecución del programa")

if __name__ == "__main__":
    main()