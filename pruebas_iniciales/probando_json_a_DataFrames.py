import json
import pandas as pd

# Ruta al archivo JSON (ajustala si es necesario)
ruta_json = r"C:\Users\lourd\Downloads\Exportación Discord Diseño de Sistemas 2024\export\1221091721383903262\chat.json"

# 🧠 Cargar el JSON en memoria
with open(ruta_json, "r", encoding="utf-8") as file:
    datos = json.load(file)  # esto te da una lista de diccionarios

# Convertir a un DataFrame para verlo como tabla
df = pd.DataFrame(datos)

# Mostrar los primeros mensajes
print(df[["id", "timestamp", "author", "content"]].head())


# 🧹 Filtramos mensajes vacíos
df = df[df["content"].notnull()]  # saca mensajes con None

# ❌ Sacamos mensajes triviales como "gracias", "ok", etc.
irrelevantes = ["gracias", "ok", "jajaja", "dale", "perfecto"]
df = df[~df["content"].str.lower().isin(irrelevantes)]

# Mostramos de nuevo
print(df[["id", "content"]].head())





# 🧠 Detectamos si es una pregunta (heurística básica)
df["es_pregunta"] = df["content"].str.strip().str.endswith("?")

# 📊 Mostrar solo preguntas
print(df[df["es_pregunta"]][["id", "content"]])