# Pruebas Iniciales: Filtrado y Clasificación de Datos

Este repositorio contiene scripts de procesamiento desarrollados como parte de las prácticas previas al proyecto **"Chatbot con IA Generativa"**, enfocado en asistir en la organización y recuperación de conocimiento en el canal de Discord de la materia **Diseño de Sistemas (UTN FRBA)**.

El objetivo principal es **limpiar, filtrar y clasificar los mensajes** exportados desde Discord, de modo que puedan ser utilizados posteriormente para construir una base de datos relacional y otra vectorial.

---

## Funcionalidades Principales

### 1. Filtrado de mensajes irrelevantes

A partir de un archivo `.json` exportado desde Discord (convertido previamente en un `DataFrame`), se aplican múltiples filtros para descartar mensajes no informativos o ruido, como:

- Mensajes vacíos
- Solo emojis
- Solo stickers o GIFs
- Solo enlaces (por ejemplo, de Giphy o Tenor)
- Respuestas automáticas o de saludo (ej. “hola”, “ok”, “dale, gracias”)

📂 Carpeta relevante: `filtros_para_lipiar_json/`

---

### 2. Identificación de preguntas

Se aplican reglas semánticas y sintácticas para detectar si un mensaje es una **pregunta válida**. Algunos de los criterios utilizados:

- Signos de interrogación
- Palabras clave como “cómo”, “cuándo”, “por qué”, etc.
- Ubicación en el hilo de la conversación

📂 Carpeta relevante: `filtros_para_obtener_preguntas/`

Los resultados se guardan en archivos `.csv`, donde se indica si un mensaje fue clasificado como pregunta o no.

---

## Tecnologías utilizadas

- Python 3.11+
- pandas
- json
- re (expresiones regulares)
- csv

---

## Estructura del Repositorio

- `filtros_para_lipiar_json/`: scripts para limpiar mensajes irrelevantes.
- `filtros_para_obtener_preguntas/`: lógica para identificar preguntas en los mensajes.
---

## Cómo ejecutar

1. Cloná el repositorio:
   ```
   git clone https://github.com/LourdesAye/pruebas_iniciales_filtrado_y_clasificacion_de_datos.git
   cd pruebas_iniciales_filtrado_y_clasificacion_de_datos
   ```
2. Instalá dependencias necesarias:
```
pip install -r requirements.txt
```

## Sobre mí
Lourdes Ayelén González  
Estudiante de Ingeniería en Sistemas de Información – UTN FRBA
   
