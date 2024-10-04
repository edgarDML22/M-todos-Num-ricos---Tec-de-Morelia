import numpy as np
import sympy as sp
import math

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

def evaluar_matrix_Jacobiana(jacobiana, valores):#valores como collection
    matrix = np.empty((jacobiana.shape[0], jacobiana.shape[0]))
    #valores como una collection
    for i in range(jacobiana.shape[0]):
        for j in range(jacobiana.shape[1]):
            expresion = sp.sympify(jacobiana[i, j])
            matrix[i, j] = expresion.subs(valores)
    return matrix

def calcular_minus_f(A, B, valores):#valores como collection
    minus_f = np.empty(B.shape[0])
    for i in range(B.shape[0]):
        expresion = sp.sympify(A[i])
        minus_f[i] = B[i] - expresion.subs(valores)[0]
    return minus_f

def Newton_Raphson_Method(A, B, A_jacobiana, x_i):
    #x_i es una collection{x: 1, y: 2, z: 3}
    h_values = []#Aquí se van a guardar los valores de h
    x_j = []#Aquí se devolverán los siguientes valores del método
    #[C]{h_i} = [D] - Para crear el sistema de ecuaciones
    C = evaluar_matrix_Jacobiana(A_jacobiana, x_i)#Ya funciona
    D = calcular_minus_f(A, B, x_i)
    #Se resuelve el sistema de ecuaciones lineales
    h_values = np.linalg.solve(C, D).tolist()
    for x_actual, h in zip(x_i.values(), h_values):
        x_j.append(x_actual + h)
    return [h_values, x_j]


def main():
    x, y, z = sp.symbols('x y z')
    A = np.array([["x**3+y**3-z**3"], 
              ["x**2+y**2-z**2"], 
              ["x+y-z"]])
    B = np.array([129, 9.75, 9.49])#Términos independientes
    A_jacobiana = calcular_matrix_Jacobiana(A)
    #Valores como un collection{}
    x_i = {x: 1, y: 2, z: 3} #Aquí se cambia el valor inicial para las variables
    array = Newton_Raphson_Method(A, B, A_jacobiana, x_i)
    h_values = array[0]
    x_j = array[1]


if __name__ == "__main__":
    main()