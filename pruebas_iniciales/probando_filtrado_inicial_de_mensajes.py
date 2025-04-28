import json
import pandas as pd
import re

# 1. Ruta al archivo JSON original
ruta_json = r"C:\Users\lourd\Downloads\Exportación Discord Diseño de Sistemas 2024\export\1221091721383903262\chat.json"

# 2. Cargar datos JSON como lista de diccionarios en memoria
with open(ruta_json, "r", encoding="utf-8") as f:
    datos = json.load(f) # da lista de diccionarios

# 3. Convertir a DataFrame para verlo como tabla
df = pd.DataFrame(datos)

# 4. Nos quedamos solo con el campo "content" (contenido del mensaje)
df = df[df["content"].notnull()]
df["content"] = df["content"].astype(str).str.strip()
df = df[df["content"] != ""]

# 5. Mensajes irrelevantes por ser respuestas cortas
irrelevantes = [
    "hola", "buenas", "gracias", "dale", "ok", "okay", "perfecto", "exacto",
    "jajaja", "👍", "👌", "listo", "genial", "entendido"
]

def es_irrelevante(texto):
    return texto.lower().strip() in irrelevantes

df = df[~df["content"].apply(es_irrelevante)]

# 6. Eliminar mensajes que son solo emojis o símbolos (sin letras)
solo_simbolos = re.compile(r"^[^\wáéíóúüñÁÉÍÓÚÜÑ]+$", re.UNICODE)
df = df[~df["content"].apply(lambda x: bool(solo_simbolos.fullmatch(x)))]

# 7. Ignorar mensajes que contienen solo enlaces de Tenor, Giphy u otros
df = df[~df["content"].str.contains(r"(tenor\.com|giphy\.com)", case=False, na=False)]

# 8. Ignorar si es SOLO un enlace
df = df[~df["content"].str.match(r"^https?://\S+$", na=False)]

# 9. Limpiar emojis dentro del texto (opcional)
emoji_inside = re.compile(r"[^\w\s,.¿?¡!áéíóúÁÉÍÓÚüÜñÑ()\-/:;]+")

def limpiar_emojis(texto):
    return emoji_inside.sub("", texto)

df["content"] = df["content"].apply(limpiar_emojis)
df["content"] = df["content"].str.strip()
df = df[df["content"] != ""]

# 10. Guardar resultado limpio
df.to_csv("preguntas_limpias.csv", index=False, encoding="utf-8")
print("✅ Limpieza desde JSON completa. Archivo: preguntas_limpias.csv")