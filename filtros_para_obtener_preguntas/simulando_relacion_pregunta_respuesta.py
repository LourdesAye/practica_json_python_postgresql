import pandas as pd
from datetime import datetime, timedelta

# Creamos un DataFrame simulado con 3 mensajes
datos = [
    {"id": "1", "author": "lourdes", "content": "¿Qué hay que entregar el viernes?", "timestamp": "2024-04-20T10:00:00Z"},
    {"id": "2", "author": "juan", "content": "Tenés que subir el informe al campus.", "timestamp": "2024-04-20T10:30:00Z"},
    {"id": "3", "author": "carla", "content": "Perfecto, gracias", "timestamp": "2024-04-20T11:00:00Z"},
]

df = pd.DataFrame(datos)

# Se convierte timestamp a tipo datetime de pandas
df["timestamp"] = pd.to_datetime(df["timestamp"])
# Se ordena por fecha 
df = df.sort_values('timestamp').reset_index(drop=True)
# Índices quedan desordenados porque se cambia a orden por fecha, 
# entonces reset_index es para reinicia los índices y que se adapten a esa nueva forma de orden

# Función simple para detectar si un mensaje es pregunta
def es_pregunta(texto):
    return texto.strip().endswith("?") or texto.lower().startswith("¿")
    #strip() es para sacar espacios al inicio y al final de los mensajes
    #endswith("?") es para obtener los mensajes que terminan con signo ?
    #startswith("¿") es para obtener los mensajes que empiezan con ¿

# Creamos una nueva columna en el DataFrame para marcar si el mensaje es pregunta o no.
# Toma cada fila de la columna 'content'. Le aplica la función es_pregunta(texto).
# Guarda True o False en la nueva columna 'es_pregunta'.
df['es_pregunta'] = df['content'].apply(es_pregunta)

# Lógica para asociar respuestas a la última pregunta válida
relaciones = [] # lista
indice_pregunta_actual = None #no hay pregunta en este momento
tiempo_limite = timedelta(hours=48) #limite de tiempo 48 hs

for i in range(len(df)): # for recorre cada índices i de la secuencia generada por range que es 0,1, hasta len(df)-1 
    fila = df.iloc[i] # recorre la fila i del datagrama
    # Ejemplo: df tiene 3 filas
    # for i in range(len(df)):   # i será 0, luego 1, luego 2
    # fila = df.iloc[i]      # fila = fila 0, luego fila 1, luego fila 2

    print(f"\n📝 Analizando mensaje {i}:")
    print(f"Contenido: {fila['content']}")
    
    if fila['es_pregunta']: # se evalua si el mensaje es pregunta a partir de la columna es_pregunta que es True or False
        print("👉 Es una PREGUNTA. Guardamos como pregunta activa.")
        indice_pregunta_actual = i 
        # si es pregunta se guarda como pregunta activa, como la pregunta actual, para ver si le sigue respúesta u otra pregunta

    else: # no es pregunta, entonces es respuesta
        print("💬 Es una RESPUESTA.")
        if indice_pregunta_actual is not None: # si el indice de pregunta actual no esta vacio, hay una pregunta actual
            fila_pregunta = df.iloc[indice_pregunta_actual]  # se toma esa pregunta en una variable
            diferencia = fila['timestamp'] - fila_pregunta['timestamp'] # para poder hacer diferencia de tiempo entre fila actual que puede ser una respuesta y la fila de la pregunta que se evalñua en este momento
            print(f"⏱️ Diferencia con la última pregunta: {diferencia}")

            if diferencia <= tiempo_limite: # se evalua si la respuesta esta dentro de las 48 hs
                print(f"✅ Asociamos con la pregunta: {fila_pregunta['content']}")
                relaciones.append({
                    "pregunta_id": fila_pregunta["id"],
                    "pregunta": fila_pregunta["content"],
                    "respuesta_id": fila["id"],
                    "respuesta": fila["content"],
                    "autor_respuesta": fila["author"],
                    "timestamp_respuesta": fila["timestamp"]
                }) # lista de diccionarios que contiene la pregunta y la respuesta asociada
            else:
                print("⛔ Muy tarde para asociarla. Se descarta como respuesta.")

# Se Convierte las relaciones preguntas y respuestas en un nuevo DataFrame
df_relaciones = pd.DataFrame(relaciones)
print("\n🎯 Relaciones encontradas:")
print(df_relaciones)

# Guardar como CSV, opcionalmente 
df_relaciones.to_csv("relaciones_preguntas_respuestas.csv", index=False)