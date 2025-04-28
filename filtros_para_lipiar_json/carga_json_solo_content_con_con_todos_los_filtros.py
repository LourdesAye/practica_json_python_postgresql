import json
import pandas as pd
import re
import os

# Todos los filtros:
  # mensajes con frases irrelevantes : solo gracias, muchas garcias,...
  # mensaje con emojis, stickers, tenor/giphy 
  # mensajes que sea solo numeros o con algun signo como +1

# Palabras que están en respuestas irrelevenates
palabras_irrelevantes = {
    "gracias", "profe", "perfecto", "exacto", "dale", "ok", "hola",
    "buenas", "tarde", "mañana", "ahh", "sí", "no", "entiendo"
}

# filtrar palabras irrelevantes
# eliminar mensajes con 4 palabras o menos, y que contienen al menos una palabra irrelevante
def frase_corta_con_irrelevante(texto):
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)  # quitar puntuación
    palabras = texto.split()
    return len(palabras) <= 10 and any(p in palabras_irrelevantes for p in palabras)

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
    filtradas_df = df[df["content"].apply(frase_corta_con_irrelevante)]
    
    # se aplica filtro al DataFrame: se quitan frases irrelevantes
    df = df[~df["content"].apply(frase_corta_con_irrelevante)]

    # Guardar CSVs con nombre distinto por archivo
    nombre_base = f"chat_{idx}"

    # Guardar los mensajes sin frases irrelevantes y sin null en archivo CSV
    df[["content"]].to_csv(f"{nombre_base}_contenido_filtrado_sin_frases_irrelevantes_y_sin_null.csv", index=False, encoding="utf-8")

    # Guardar las frases descartadas en un nuevo archivo CSV
    filtradas_df[["content"]].to_csv(f"{nombre_base}_frases_descartadas.csv", index=False, encoding="utf-8")

    print(f"✅ Mensajes irrelevantes eliminados: {len(filtradas_df)}")

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

     # Guardar CSV final ya limpio
    df[["content"]].to_csv(f"{nombre_base}_final_filtrado.csv", index=False, encoding="utf-8")
    print(f"✅ Mensajes totalmente filtrados guardados (sin vacios,sin frases irrelevantes,sin emojis, sin solo numeros): {len(df)}")

    








