# range()
# genera una secuencia de números enteros. 
# se utiliza con bucles for para iterar sobre un rango específico de números. 
# Por defecto, range() comienza en 0, incrementa en 1 y termina antes de un número específico. 

# Argumentos: range(start,stop,step)
# stop: Número entero que indica el final del rango (no se incluye).
# start: (Opcional) Número entero que indica el inicio del rango (por defecto es 0).
# step: (Opcional) Número entero que indica el incremento entre cada número en la secuencia (por defecto es 1). 

#Características: range() genera un iterador, no una lista directamente. 
# range() es útil para crear bucles iterativos, 
# especialmente cuando necesitas contar hasta un determinado número 
# o generar una secuencia de números. 

for i in range(5): # range(stop): Genera la secuencia 0, 1, 2, 3, 4.
    print(i)

for i in range(2,8): # range(2, 8): range(start,stop) : Genera la secuencia 2, 3, 4, 5, 6, 7.
    print(i)

for i in range(0,10,2): # range(0, 10, 2): range(start,stop,step): Genera la secuencia 0, 2, 4, 6, 8.
    print(i)

for i in range(10,0,-1): # range(10, 0, -1): range(start,stop,step): Genera la secuencia 10, 9, 8, 7, 6, 5, 4, 3, 2, 1.
    print(i)
