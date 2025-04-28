# se recomienda un archivo por clase si las clases son muy grandes, para que sea más ordenado.

class Persona: # Clase: Es una plantilla que define cómo deberían ser los objetos.
    # self: Siempre es el primer parámetro de los métodos de instancia.
    def __init__(self, nombre, edad):  # Constructor
        # Es una función especial que se llama automáticamente cuando creás un objeto.
        self.nombre = nombre
        self.edad = edad
        # Sirve para inicializar atributos (datos) del objeto.

    def saludar(self):
        print(f"Hola, soy {self.nombre} y tengo {self.edad} años.")

# Crear un objeto:
#persona1 = Persona("Lourdes", 24) # Objeto: Es una instancia concreta creada a partir de esa clase.

# Usar métodos del objeto:
#persona1.saludar()
