import sympy as sp
import numpy as np

# Definir el símbolo
x = sp.symbols('x')

# Leer la expresión desde una cadena de texto
expresion_str = "exp(x)"  # Aquí iría la cadena escrita en la consola
expresion_simb = sp.sympify(expresion_str)  # Convertir cadena a expresión simbólica

# Mostrar la expresión simbólica
print(f"Expresión simbólica: {expresion_simb}")

# Derivar la expresión simbólica
derivada_simb = sp.diff(expresion_simb, x)

# Mostrar la derivada simbólica
print(f"Derivada simbólica: {derivada_simb}")

# Convertir la derivada en una función evaluable numéricamente
derivada_func = sp.lambdify(x, derivada_simb)

# Evaluar la derivada en un valor numérico
valor = 1
resultado = derivada_func(valor)

print(f"Valor de la derivada en x={valor}: {resultado}")

