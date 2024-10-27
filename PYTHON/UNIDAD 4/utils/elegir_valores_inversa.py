import numpy as np
import sympy as sp
import math

#El valor ya está dentro de los valores de y
value = 0.3
valores_x = [1, 2, 3, 4, 5]
valores_y = [0.2, 0.25, 0.33, 0.5, 1]
#lista = [0.2, 0.25, 0.33, 0.5, 1]
lista_index = []


#Para los primeros 2 valores
for i in range(len(valores_y) - 1):
        if valores_y[i] <= value <= valores_y[i + 1]:#lista creciente
            lista_index =  [i, i + 1]
        if valores_y[i] >= value >= valores_y[i + 1]:
            lista_index = [i, i + 1]
#Para el tercer valor
if 0 in lista_index:
     lista_index.append(2)
elif (len(valores_y) - 1) in lista_index:
     lista_index.append(len(valores_y) - 3)
else:
    #Primero ver si hay un valor de x más cercano
    posibles_index = [lista_index[0] - 1, lista_index[1] + 1]
    if valores_x[posibles_index[0]] <= valores_x[posibles_index[1]]:
         lista_index.append(posibles_index[0])
    else:
        lista_index.append(posibles_index[1])
    
#ordenar la lista
flag = False
while not flag:
    flag = True
    for i in range(len(lista_index) - 1):
        if lista_index[i] > lista_index[i + 1]:
             aux = lista_index[i]
             lista_index[i] = lista_index[i + 1]
             lista_index[i + 1] = aux
             flag = False

print(lista_index)





