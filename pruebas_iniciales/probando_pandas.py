import json
import pandas as pd
import re

# Ruta al archivo JSON (ajustala si es necesario)
ruta_json = r"C:\Users\lourd\Downloads\Exportación Discord Diseño de Sistemas 2024\export\1221091721383903262\chat.json"

# Cargar los mensajes del JSON
with open(ruta_json, "r", encoding="utf-8") as f:
    datos = json.load(f)

#Lista de palabras interrogativas
interrogativos = ["qué", "como", "cómo", "cuándo", "cuando", "dónde", "donde", "por qué", "cuál", "cuáles", "quién", "quiénes", "para qué"]

# Función para detectar preguntas
def es_pregunta(texto):
    texto = texto.strip().lower()
    texto = re.sub(r"^[¿\?¡!]+", "", texto)
    primer_palabra = texto.split()[0] if texto else ""
    return primer_palabra in interrogativos or texto.endswith("?")

# Filtrar los mensajes que son preguntas
preguntas = [m["contenido"] for m in datos if es_pregunta(m.get("contenido", ""))]

# Exportar a CSV
df = pd.DataFrame(preguntas, columns=["content"])
df.to_csv("preguntas_filtradas.csv", index=False, encoding="utf-8")
print("todo salio bien! :)")