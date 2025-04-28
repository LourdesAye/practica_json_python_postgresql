import json
import pandas as pd
import re
import os
from datetime import datetime, timedelta

import sys

# Redireccionar todos los print() a un archivo
sys.stdout = open("logs_procesamiento.txt", "w", encoding="utf-8")

# Todos los filtros para limpiar json:
  # mensajes con frases irrelevantes : solo gracias, muchas garcias,...
  # mensaje con emojis, stickers, tenor/giphy 
  # mensajes que sea solo numeros o con algun signo como +1

# Palabras que están en respuestas irrelevenates

# palabras_irrelevantes = {
#     "gracias", "profe", "perfecto", "exacto", "dale", "ok", "oka", "hola",
#     "buenas", "tarde", "mañana", "ahh", "sí", "no", "entiendo","joya","genial", "resuelto","claro","buenisimo"
# }


# usuarios docentes
usuarios_docentes = ["ezequieloescobar", "aylenmsandoval", "lucassaclier"]

# Frases comunes para detectar preguntas explícitas o implícitas
frases_clave_preguntas = [
    "cómo", "cuándo", "qué", "cuál", "dónde", "por qué", "para qué",
    "qué pasa si", "tengo una consulta", "tengo una duda", "tengo una pregunta",
    "mi duda es", "mi consulta es", "quisiera consultar", 
    "quería saber si", "me surgió la duda", "necesito saber si", "me pregunto si",
    "alguien sabe", "una duda", "una consulta","necesito ayuda", "es posible"
]

frases_validacion_docente ={"perfecto", "exacto","buenísimo"}
frases_cierre_alumnos = {"gracias","perfecto","buenísimo","genial","muchas","joya"}

# filtrar palabras irrelevantes
# eliminar mensajes con 10 palabras o menos, y que contienen al menos una palabra irrelevante
# def frase_corta_con_irrelevante(texto):
#     texto = texto.lower()
#     texto = re.sub(r"[^\w\s]", "", texto)  # quitar puntuación
#     palabras = texto.split()
#     return len(palabras) <= 10 and any(p in palabras_irrelevantes for p in palabras)

# Eliminar mensajes que sean solo emojis, solo stickers, gifs o enlaces tipo tenor/giphy
def es_contenido_irrelevante_visual(texto):
    texto = texto.strip().lower()
    # Si es solo emojis (todos los caracteres son emojis o espacios)
    solo_emojis = re.fullmatch(r"[\s\U0001F300-\U0001FAFF\U00002600-\U000026FF\U00002700-\U000027BF]+", texto)
    # Si contiene solo un link tipo Tenor o Giphy
    es_link_tenor_giphy = re.fullmatch(r"(https?:\/\/)?(www\.)?(tenor|giphy)\.com\S*", texto)
    # Si solo dice "sticker" o "gif"
    es_sticker_gif = texto in {"sticker", "gif"}

    return bool(solo_emojis or es_link_tenor_giphy or es_sticker_gif)

# eliminar solo numeros o combinacion de numero mas signo como +1
def es_solo_numeros_signos(texto):
    return bool(re.fullmatch(r"[+\d\s]+", texto))

# todos los filtros para obtener preguntas
  # que no sea de un docente (todo lo que sea de ellos es considerado respuesta)
      # y que tenga signo ¿? o frases tipicas de preguntas 

def es_docente(autor: str) -> bool:
    return autor.lower() in usuarios_docentes

# si un mensaje completo es una pregunta.
# La función toma una fila completa del DataFrame para analizar si el mensaje es pregunta 
# a partir del autor y de ciertos patrones
def es_pregunta(mensaje: str) -> bool:
    texto = mensaje. lower().strip() # convierte el mensaje que esta en texto para pasarlo a minúscula y le quita los espacios que pueda tener al incio y al final

    # Si contiene signos de interrogación
    if "?" in texto or "¿" in texto:
        return True

    # Si contiene alguna frase típica
    for frase in frases_clave_preguntas:
        if frase in texto:
            return True

    return False

def es_respuesta_docente(autor: str)-> bool:
    autor = autor.lower().strip() #lleva el autor a minuscula y le quita los espacios al inicio y al final
    return autor in usuarios_docentes # verificacion directa con in sin usar for

def es_mensaje_de_cierre_alumno(mensaje: str) -> bool:
    texto = mensaje.lower().strip()
    for frase in frases_cierre_alumnos:
        if frase in texto and len(texto) <= 10:  # Evitar mensajes largos tipo "gracias + nueva pregunta"
            return True
    return False

# para detectar si dentro del mensaje hay indicios de una nueva pregunta.
def contiene_pregunta(mensaje: str) -> bool:
    mensaje = mensaje.lower().strip()
    
    # Detectar si hay signos de pregunta
    if "?" in mensaje or "¿" in mensaje:
        return True

    # Detectar si contiene alguna frase típica de pregunta
    for frase in frases_clave_preguntas:
        if frase in mensaje:
            return True

    return False

def es_mensaje_de_validacion_docente(mensaje: str) -> bool:
    mensaje = mensaje.lower().strip()
    for frase in frases_validacion_docente:
        if frase in mensaje:
            return True
    return False


# para obtener frases cortas
def es_frase_corta(texto):
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)  # quitar puntuación
    palabras = texto.split()
    return len(palabras) <= 5

# Rutas al JSON
ruta_json1 = r"C:\Users\lourd\Downloads\Exportación Discord Diseño de Sistemas 2024\export\1221091721383903262\chat.json"
ruta_json2=r"C:\Users\lourd\Downloads\Exportación Discord Diseño de Sistemas 2024\export\1219817856288686083\chat.json"
ruta_json3=r"C:\Users\lourd\Downloads\Exportación Discord Diseño de Sistemas 2024\export\1221091674248446003\chat.json"

#lista de rutas del JSON
rutas_json=[ruta_json1,ruta_json2,ruta_json3]

# Procesar cada archivo JSON
for idx, ruta_json in enumerate(rutas_json, start=1): 
    # enumerate recibe lista para devolver una tupa(indice,valor), 
    # el start=1 es para que indice empiece en 1 y no en 0 que es por defecto
    
    # Cargar JSON
    with open(ruta_json, "r", encoding="utf-8") as f:
        datos = json.load(f)

    print(f"\n📄 Procesando archivo {idx}: {os.path.basename(os.path.dirname(ruta_json))}")
    
    # Convertir a DataFrame
    df = pd.DataFrame(datos)

    #cantidad total de mensajes en el json, en el Dataframe
    total_original = len(df)

    print(f"✅ Total mensajes en JSON: {total_original}")

    # Guardar CSVs con nombre distinto por archivo
    nombre_base = f"chat_{idx}"

    # Guardar solo el campo "content" del dataframe en un nuevo archivo CSV
    df[["content"]].to_csv(f"{nombre_base}_todo_el_content_sin_filtros.csv", index=False, encoding="utf-8")

    # Asegurarse de que 'content' exista y convertimos a string (por si hay None)
    df["content"] = df["content"].astype(str).str.strip()
    
    # Filtrar: se queda solo con los que tienen texto real (no vacío)
    df = df[df["content"] != ""]

    # cantidad total de mensajes no vacios en el Dataframe
    total_no_vacios = len(df)
    
    # os.path.dirname(ruta_json) : devuelve el nombre del directorio que contiene el archivo ruta_json
    #os.path.basename: obtiene solo el último segmento del directorio.
    print(f"✅ Mensajes no vacíos: {total_no_vacios}")
    
    # se obtienen en un DataFrame nuevo con los mensajes que son irrelevantes
    #iltradas_df = df[df["content"].apply(frase_corta_con_irrelevante)]

    
    # se aplica filtro al DataFrame: se quitan frases irrelevantes
    #f = df[~df["content"].apply(frase_corta_con_irrelevante)]

    # Guardar CSVs con nombre distinto por archivo
    nombre_base = f"chat_{idx}"

    # Guardar los mensajes sin frases irrelevantes y sin null en archivo CSV
    df[["content"]].to_csv(f"{nombre_base}_contenido_filtrado_sin_frases_irrelevantes_y_sin_null.csv", index=False, encoding="utf-8")

    # Guardar las frases descartadas en un nuevo archivo CSV
   #filtradas_df[["content"]].to_csv(f"{nombre_base}_frases_descartadas.csv", index=False, encoding="utf-8")

    #rint(f"✅ Mensajes irrelevantes eliminados: {len(filtradas_df)}")

    print(f"✅ Mensajes no vacíos y sin frases irrelevantes guardados: {len(df)}")

    # Filtrar los mensajes que tienen mensajes irrelevantes y colocarlos en nuevo Dataframe
    visuales_df = df[df["content"].apply(es_contenido_irrelevante_visual)]

    # Filtrar DataFrame sin vacios, quitandole los mensajes visuales irrelevantes (emojis, gifs, etc.)
    df = df[~df["content"].apply(es_contenido_irrelevante_visual)]

    # Guardar los mensjas con elementos visuales irrelevantes (emojis, gifs, etc.) en CSV
    visuales_df[["content"]].to_csv(f"{nombre_base}_emojis_gifs_descartados.csv", index=False, encoding="utf-8")
    print(f"✅ Mensajes visuales descartados (emojis, gifs, etc.): {len(visuales_df)}")

    # Guardar CSV final ya limpio
    df[["content"]].to_csv(f"{nombre_base}_sin_emojis_gifs.csv", index=False, encoding="utf-8")
    print(f"✅ Mensajes totalmente filtrados guardados (sin vacios,sin frases irrelevantes y sin emojis): {len(df)}")

    # se queda con mensajes que tengan solo combinacion de numero mas signo como +1
    sin_numeros_solos_df = df[df["content"].apply(es_solo_numeros_signos)]

    #filtra los mensajes que no tengan solo combinacion de numero mas signo como +1
    df = df[~df["content"].apply(es_solo_numeros_signos)]

    # Guardar los mensajes que tengan solo combinacion de numero mas signo como +1 en CSV
    sin_numeros_solos_df[["content"]].to_csv(f"{nombre_base}_numeros_descartados.csv", index=False, encoding="utf-8")
    print(f"✅ Mensajes con solo numeros descartados (emojis, gifs, etc.): {len(sin_numeros_solos_df)}")

    # Guardar CSV limpio
    df[["content"]].to_csv(f"{nombre_base}_json_sin_frases_cortas.csv", index=False, encoding="utf-8")
    print(f"✅ Mensajes filtrados guardados (sin vacios,sin frases irrelevantes,sin emojis, sin solo numeros): {len(df)}")

     #filtra los mensajes que no tengan solo combinacion de numero mas signo como +1
    df_frases_cortas = df[df["content"].apply(es_frase_corta)]
    df_frases_cortas[["content"]].to_csv(f"{nombre_base}_para_debug_frases_cortas_del_filtrado.csv", index=False, encoding="utf-8")

    #guarda los mensajes que no sean frases cortas: menor o igual a 4 palabras
    df = df[~df["content"].apply(es_frase_corta)]
    print(f"✅ La cantidad de frases cortas de {nombre_base} es: {len(df_frases_cortas)}")

    # Guardar CSV totalmente limpio
    df[["content"]].to_csv(f"{nombre_base}_json_final_filtrado.csv", index=False, encoding="utf-8")
    print(f"✅ Mensajes filtrados guardados (sin vacios,sin frases irrelevantes,sin emojis, sin solo numeros, sin frases cortas): {len(df)}")

    # aplicar la funicion a cada fila del Datagrama para saber si es pregunta
    # axis=1 es clave porque le estás pasando filas completas a la función, no solo una columna.
    df["es_pregunta"] = df.apply(es_pregunta, axis=1) 

    # Separar las preguntas detectadas en un nuevo DataFrame
    preguntas_df = df[df["es_pregunta"]]

    # Separar las respuestas detectadas en un nuevo DataFrame
    respuestas_df= df[~df["es_pregunta"]]

    # Guardar las preguntas en un nuevo CSV 
    preguntas_df[["content"]].to_csv(f"{nombre_base}_preguntas_detectadas.csv", index=False, encoding="utf-8")
    print(f"✅ Preguntas detectadas: {len(preguntas_df)}")

    # Guardar las respuestas en un nuevo CSV
    respuestas_df[["content"]].to_csv(f"{nombre_base}_respuestas_detectadas.csv", index=False, encoding="utf-8")
    print(f"✅ Respuestas detectadas: {len(respuestas_df)}")

    #creamos in dataframe para los datos obtenidos hasta ahora
    df_mensajes_limpios = df
    # Se convierte timestamp a tipo datetime de pandas
    df_mensajes_limpios["timestamp"] = pd.to_datetime(df_mensajes_limpios["timestamp"])
    # Se ordena por fecha 
    df_mensajes_limpios = df_mensajes_limpios.sort_values('timestamp').reset_index(drop=True)
    # Índices quedan desordenados porque se cambia a orden por fecha, 
    # entonces reset_index es para reinicia los índices y que se adapten a esa nueva forma de orden

    # Lógica para asociar respuestas a la última pregunta válida
    relaciones = [] # lista
    respuestas_sin_preguntas=[]
    preguntas_sin_respuestas=[]
    indice_pregunta_actual = None # no hay pregunta actual en este momento
    tiempo_limite = timedelta(hours=72) # limite de tiempo 48 hs entre pregunta y respuesta

    for i in range(len(df_mensajes_limpios)): # for recorre cada índices i de la secuencia generada por range que es 0,1, hasta len(df)-1 
        fila = df_mensajes_limpios.iloc[i] # recorre la fila i del datagrama
        # Ejemplo: df tiene 3 filas: fila = df.iloc[i]  es fila 0, luego fila 1, luego fila 2

        print(f"\n📝 Analizando mensaje {i}:")
        print(f"Contenido: {fila['content']}")
        
        if fila['es_pregunta']: # se evalua si el mensaje es pregunta a partir de la columna es_pregunta que es True or False
            print("👉 Es una PREGUNTA. Guardamos como pregunta activa.")
            indice_pregunta_actual = i 
            # si es pregunta se guarda como pregunta activa, como la pregunta actual, para ver si le sigue respuesta u otra pregunta

        else: # no es pregunta, entonces es respuesta
            print("💬 Es una RESPUESTA.")
            if indice_pregunta_actual is not None: # si el indice de pregunta actual no esta vacio, hay una pregunta actual
                fila_pregunta = df_mensajes_limpios.iloc[indice_pregunta_actual]  # se toma esa pregunta en una variable
                diferencia = fila['timestamp'] - fila_pregunta['timestamp'] # para poder hacer diferencia de tiempo entre fila actual que puede ser una respuesta y la fila de la pregunta que se evalua en este momento
                print(f"⏱️ Diferencia con la última pregunta: {diferencia}")

                if diferencia <= tiempo_limite: # se evalua si la respuesta esta dentro de las 48 hs
                    print(f"✅ Asociamos con la pregunta: {fila_pregunta['content']}")
                    relaciones.append({
                        "pregunta_id": fila_pregunta["id"],
                        "es_pregunta": fila_pregunta["es_pregunta"],
                        "autor_pregunta": fila_pregunta["author"],
                        "timestamp_pregunta": fila_pregunta["timestamp"],
                        "attachments_pregunta": fila_pregunta["attachments"],
                        "pregunta": fila_pregunta["content"],
                        "respuesta_id": fila["id"],
                        "respuesta": fila["content"],
                        "autor_respuesta": fila["author"],
                        "timestamp_respuesta": fila["timestamp"],
                        "attachments_respuesta": fila["attachments"],
                        "es_pregunta": fila_pregunta["es_pregunta"]
                    }) # lista de diccionarios que contiene la pregunta y la respuesta asociada
                else:
                    print("⛔ Muy tarde para asociarla. Se descarta como respuesta.")
            else:
                print("⛔ Es una respuesta sin pregunta.")
                respuestas_sin_preguntas.append({
                "respuesta_id": fila["id"],
                "respuesta": fila["content"],
                "autor_respuesta": fila["author"],
                "timestamp_respuesta": fila["timestamp"],
                "attachments_respuesta": fila["attachments"],
                "es_pregunta": fila_pregunta["es_pregunta"]
            }) # lista de diccionarios que contiene respuestas que no se asociaron a preguntas



    # Se Convierte las relaciones preguntas y respuestas en un nuevo DataFrame
    df_relaciones = pd.DataFrame(relaciones)
    print("\n🎯 Relaciones encontradas:")
    print(df_relaciones)

    # Guardar como CSV, opcionalmente 
    df_relaciones.to_csv("relaciones_preguntas_respuestas.csv", index=False)

        # Se Convierte las relaciones preguntas y respuestas en un nuevo DataFrame
    df_respuestas_sin_preguntas = pd.DataFrame(relaciones)
    print("\n🎯 Respuestas sin preguntas encontradas:")
    print(df_respuestas_sin_preguntas)

    # Guardar como CSV, opcionalmente 
    df_respuestas_sin_preguntas.to_csv("respuestas_sin_preguntas.csv", index=False)

        


