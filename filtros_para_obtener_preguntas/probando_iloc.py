import pandas as pd

#diccionario {clave1:valor1,clave2:valor2,...}
data = {'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]}
#convertir diccionario a DataFrame (usando pandas)
df = pd.DataFrame(data, index=['a', 'b', 'c'])
#para viusalizar el Dataframe
print(df)

'''
   col1  col2  col3
a     1     4     7
b     2     5     8
c     3     6     9

'''

# Ejemplos de uso de iloc ( de Pandas en Python)
# método para acceder a filas y columnas de un DataFrame 
# utilizando la indexación basada en posiciones enteras, comenzando desde 0. 
# no usa las etiquetas de las filas y columnas, se usa su posición numérica para seleccionar datos.

# df.iloc[fila] devuelve una serie con los elementos de la fila indicada.
# df.iloc[:, columna] devuelve una columna del DataFrame.
# df.iloc[fila, columna] devuelve el valor en la intersección de la fila y la columna.
# df.iloc[fila1:fila2, columna1:columna2] devuelve una submatriz del DataFrame 
# con las filas desde fila1 hasta fila2 (excluyendo fila2) 
# y las columnas desde columna1 hasta columna2 (excluyendo columna2).

#Se puede pasar una lista de índices para seleccionar varias filas o columnas.
#Se pueden usar rangos de índices para seleccionar un intervalo de filas o columnas.

# Se pueden usar índices negativos para acceder a elementos desde el final del DataFrame.
# df.iloc[-1] selecciona la última fila.
# df.iloc[[-1,-2]] selecciona la última y penúltima fila. 



# Seleccionar la primera fila
print("Seleccionar la primera fila",df.iloc[0]) # fila del Dataframe

'''
Seleccionar la primera fila col1    1
col2    4
col3    7
Name: a, dtype: int64
'''

# Seleccionar la columna 'col2'
print("Seleccionar la columna 'col2'",df.iloc[:, 1]) #df.iloc[:, columna]

'''
Seleccionar la columna 'col2' a    4
b    5
c    6
Name: col2, dtype: int64
'''

# Seleccionar el valor en la intersección de la fila 'a' y la columna 'col2'
print("seleccionar el valor en la intersección de la fila 'a' y la columna 'col2'",df.iloc[0, 1]) # df.iloc[fila, columna]

'''
seleccionar el valor en la intersección de la fila 'a' y la columna 'col2' 4
'''

# Seleccionar las filas 1 y 2
print("Seleccionar las filas 1 y 2 ",df.iloc[1:3])  # df.iloc[fila1:fila2, columna1:columna2]
'''
Seleccionar las filas 1 y 2     col1  col2  col3
b     2     5     8
c     3     6     9
'''

# Seleccionar las filas 1 y 2 y las columnas 0 y 1
print(" Seleccionar las filas 1 y 2 y las columnas 0 y 1 ",df.iloc[1:3, 0:2]) # df.iloc[fila1:fila2, columna1:columna2]

'''
 Seleccionar las filas 1 y 2 y las columnas 0 y 1     col1  col2
b     2     5
c     3     6
'''
