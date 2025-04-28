mi_lista = ["manzana", "banana", "cereza"]


for indice, fruta in enumerate(mi_lista): # el indice por defecto comienza en cero
    print(f"El índice es: {indice}, y el valor es: {fruta}")
   
'''
El índice es: 0, y el valor es: manzana
El índice es: 1, y el valor es: banana
El índice es: 2, y el valor es: cereza
'''
print()

for indice, fruta in enumerate(mi_lista, start=1): # el indice se fuerza a que empeice en uno 
    print(f"El índice es: {indice}, y el valor es: {fruta}")

'''
El índice es: 1, y el valor es: manzana
El índice es: 2, y el valor es: banana
El índice es: 3, y el valor es: cereza
'''

# función enumerate, recibe como parametro lista,tupla o cadena de caracteres
# la salida es un objeto que se puede iterar con un for
# En cada iteración del for, numerate devuelve una tupla (índice, valor).
# para acceder al contenido y posición de cada elemento en la secuencia

# Ventajas:
# Evita la necesidad de mantener un contador manualmente dentro del bucle.