import numpy as np
import sympy as sp
import math

x, y, z = sp.symbols('x y z')
variables = {x: 0, y: 0}
funcion_str = "sqrt(10-x*y)" 
funcion_numerica = sp.sympify(funcion_str)
value = funcion_numerica.subs(variables)   
print(value)