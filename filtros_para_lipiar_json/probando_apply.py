import pandas as pd

# creación de un diccionario en python diccionario={clave1:valor1,clave2:valor2,...}
data = {'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]}
# Convertir diccionario en DataFrame
df = pd.DataFrame(data)

# Se define una función 
def sumar_columnas(col):
  return col.sum()

# Aplicar una función a cada columna (axis=0, default)
resultados_columnas = df.apply(sumar_columnas)
print(resultados_columnas)

# Se define una función 
def sumar_filas(fila):
  return fila.sum()

# Aplicar una función a cada fila (axis=1)
resultados_filas = df.apply(sumar_filas, axis=1)
print(resultados_filas)


def multiplicar_por_2(col):
  return col * 2

# Aplicar una función lambda a cada columna
df['col4'] = df.apply(multiplicar_por_2, axis=1)
print(df)

# El método .apply() en Pandas permite aplicar una función a cada fila o columna de un DataFrame. 
# Si se utiliza sin el parámetro axis, se aplica a cada columna. Si se usa axis=1, se aplica a cada fila. 
