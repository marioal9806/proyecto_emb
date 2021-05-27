# Definir una clase de Estudiante para crear y añadir las instancias a la DB

class Estudiante:
    def __init__(self, nombre, matricula, uid, indice):
        self.nombre = nombre
        self.matricula = matricula
        self.uid = uid
        self.indice = indice
