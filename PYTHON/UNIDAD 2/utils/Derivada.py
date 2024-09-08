import sympy as sp
import numpy as np

from sympy import cos, sin, log

x = sp.symbols('x')
expresion = sin(x)
print(expresion)
derivative = sp.diff(expresion,x)
print(derivative)


def derivative_function(derivative, valor):
    derivative_function = sp.lambdify(x, derivative)
    return derivative_function(valor)


valor = np.pi
print(f"Valor de x={valor} en la derivada: {derivative_function(derivative, valor)}")

