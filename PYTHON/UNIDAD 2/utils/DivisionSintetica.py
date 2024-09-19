

def calcular_grado_funcion(cad):
    power = cad[cad.find("**") + 2]
    print(power)
    return int(power)

def obtener_coeficientes(cad):
    coeficientes = []
    grado = calcular_grado_funcion(cad)
    n = 0 #Posicion en la cadena
    while len(coeficientes) <= grado:
        index_asterisco = cad.find("*", n)
        valor = int(cad[n:index_asterisco].strip())
        print(f"VALOR: {valor}")
        coeficientes.append(valor)
        n = index_asterisco + 5
    return coeficientes    

def convertir_coeficientes_int(array):
    coeficientes = array
    n = 0
    while n < len(coeficientes):
        coeficientes[n] = int(coeficientes[n])
        n += 1
    return coeficientes 

def division_sintetica(function_str, solucion):
    #solucion = 2
    grado = calcular_grado_funcion(function_str)
    coeficientes = obtener_coeficientes(function_str)
    print(coeficientes)
    nuevos_coeficientes = []
    nuevos_coeficientes.append(coeficientes[0])
    #Obtener los coeficientes de la ecuación original
    index = 1
    while len(nuevos_coeficientes) <= (grado - 1):
        valor = coeficientes[index] + solucion*nuevos_coeficientes[index - 1] 
        nuevos_coeficientes.append(valor)
        index += 1
    print(nuevos_coeficientes)
    
    power = grado - 1
    index  = 0
    cad = ""
    while power >= 0:
        if nuevos_coeficientes[index] >= 0 and index > 0:#son positivos, ponerle el signo +
            cad += "+" 
        cad = cad + str(nuevos_coeficientes[index]) + "*x**" + str(power)
        print(f"CAD: {cad}")
        power -= 1
        index += 1
    return cad
    
        
def main():
    funcion_str = "1*x**4+0*x**3-13*x**2+0*x**1+36*x**0"
    "1*x**7 + 0*x**3 - 13*x**2 + 0*x**1 + 36*x**0"
    nueva_funcion = division_sintetica(funcion_str, 2) 
    print(nueva_funcion)  

if __name__ == "__main__":
    main()
    
