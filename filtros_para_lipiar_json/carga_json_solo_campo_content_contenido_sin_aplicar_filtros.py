import json
import pandas as pd

# Ruta al JSON exportado desde Discord
ruta_json = r"C:\Users\lourd\Downloads\Exportación Discord Diseño de Sistemas 2024\export\1221091721383903262\chat.json"

# Cargar los datos del archivo JSON
with open(ruta_json, "r", encoding="utf-8") as f:
    datos = json.load(f)

# Convertirlo en DataFrame y quedarnos solo con la columna 'content'
df = pd.DataFrame(datos)

# Asegurarse de que 'content' esté presente
if "content" in df.columns:
    df_content = df[["content"]]
else:
    print("⚠️ La clave 'content' no se encuentra en el JSON.")
    df_content = pd.DataFrame()

# Guardar a CSV
df_content.to_csv("solo_content.csv", index=False, encoding="utf-8")

print(f"✅ Archivo 'solo_content.csv' guardado con {len(df_content)} filas.")