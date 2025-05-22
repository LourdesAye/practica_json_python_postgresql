import json
import pandas as pd

# Ruta al JSON
ruta_json = r"C:\Users\lourd\Downloads\Exportación Discord Diseño de Sistemas 2024\export\1221091721383903262\chat.json"

# Cargar JSON
with open(ruta_json, "r", encoding="utf-8") as f:
    datos = json.load(f)

# Convertir a DataFrame
df = pd.DataFrame(datos)

# Nos aseguramos de que 'content' exista y convertimos a string (por si hay None)
df["content"] = df["content"].astype(str).str.strip()

# Filtramos: nos quedamos solo con los que tienen texto real (no vacío)
df = df[df["content"] != ""]

# Guardar resultado para ver cuántos quedaron después de este primer filtro
df[["content"]].to_csv("content_no_vacios.csv", index=False, encoding="utf-8")

print(f"✅ Mensajes no vacíos guardados: {len(df)}")