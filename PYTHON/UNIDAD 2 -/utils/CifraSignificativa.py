import numpy as np

def valor_cifras_significativas(numero, n):
    if numero == 0:
        return 0
    else:
        # f"{numero:e}", te da el número en notación científica(String)
        #.split() separa la cadena en una lista y en la segunda posición[1] queda el exponente del 10^x
        # se convierte en un entero con int()
        factor = n - (int(f"{numero:e}".split('e')[1]) + 1)
        return round(numero, factor)

# Ejemplos de uso
print(valor_cifras_significativas(1.234567, 4))  # 1.235
print(valor_cifras_significativas(12.34567, 4))  # 12.35
print(valor_cifras_significativas(123.4567, 4))  # 123.5

#a = 120003.456
#b = f"{a:e}"
#print(b)

print(f"{0.0004567:e}".split('e'))
print(valor_cifras_significativas(0.0004567, 1) + 10)

matrix = np.zeros((3,3))

#>>>>>>>>Comandos para la terminal<<<<<<<<<<<
#pip install numpy
#pip install sympy

