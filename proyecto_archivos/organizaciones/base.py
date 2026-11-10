"""Clase base: interfaz CRUD común a todas las organizaciones."""
import os

from modelo.registro import decodificar


class Archivo:
    nombre = ""
    descripcion = ""
    archivos = ()

    def __init__(self, carpeta, salida=print):
        self.carpeta, self.salida, self.tocadas = carpeta, salida, []
        self._abrir()

    def log(self, msg):
        self.salida(msg)

    def ruta(self, nombre):
        return os.path.join(self.carpeta, nombre)

    def reiniciar(self):
        for a in self.archivos:
            if os.path.exists(self.ruta(a)):
                os.remove(self.ruta(a))
        self._abrir()
        self.tocadas = []

    def _ver(self, arch, i):
        return decodificar(arch.leer(i))

    def listar(self):
        """[(pos, estado, Registro)] en orden físico."""
        return [(i, *self._ver(self.dat, i)) for i in range(self.dat.n())]

    def estructura(self):
        return ("Esta organización no usa estructura auxiliar (índice/tabla).", ("—",), [])

    def reorganizar(self):
        self.log("Esta organización no necesita reorganización.")

    # interfaz CRUD (la implementan las subclases)
    def insertar(self, reg): ...
    def buscar(self, cuenta): ...
    def actualizar(self, reg): ...
    def eliminar(self, cuenta): ...
