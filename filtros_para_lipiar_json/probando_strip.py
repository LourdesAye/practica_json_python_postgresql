'''
En Python, strip() es un método de cadena que elimina los espacios en blanco 
(espacios, tabulaciones, saltos de línea) del principio y final de una cadena. 
Si se proporciona una cadena como argumento, strip() eliminará los caracteres de esa cadena 
tanto al principio como al final. 
No modifica la cadena original.

Ejemplo:
Si tienes la cadena " Hola, mundo! ", strip() la convertiría en "Hola, mundo!". 
Otros métodos relacionados:
lstrip(): Elimina espacios en blanco del principio de una cadena. 
rstrip(): Elimina espacios en blanco del final de una cadena. 
'''

string1 = "   Hola,mundo!   "
string2 = ",,,Python,,,,"

stripped_string1_sin_espacios_inicio_final = string1.strip()
stripped_string2_sin_espacios_inicio_final_y_sin_comas = string1.strip(",")

print("la cadena original con espacios al inicio y al final:",string1) # "   Hola,mundo!   "
print("la cadena sin espacios al inicio y al final:",stripped_string1_sin_espacios_inicio_final)  # "Hola,mundo!"

print()

print("la cadena original con comas al inicio y al final:",string2) #",,,Python,,,,"
print("la cadena sin comas al inicio y al final es:",string2.strip(","))  #  "Python"

print()

print("cadena sin espacio al incio:",string1.lstrip()) # "Hola, mundo!   "
print("cadena sin comas al final:",string2.rstrip(",")) # ",,,Python"