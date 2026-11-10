"""Organización secuencial ordenada."""
from modelo.almacenamiento import Bin, busqueda_binaria
from organizaciones.base import Archivo
from modelo.registro import ACTIVO, BORRADO, VACIO, ESTADOS, TAM_REG, decodificar, Registro


class ArchivoSecuencial(Archivo):
    nombre = "Secuencial ordenada"
    descripcion = ("Registros ordenados físicamente por número de cuenta. Búsqueda binaria. "
                   "Alta y baja desplazan los registros siguientes (baja física).")
    archivos = ("secuencial.dat",)

    def _abrir(self):
        self.dat = Bin(self.ruta("secuencial.dat"), TAM_REG)

    @staticmethod
    def _clave(d):
        return decodificar(d)[1].clave

    def buscar(self, cuenta):
        self.log(f"Búsqueda binaria de la cuenta {cuenta:07d}:")
        ok, pos = busqueda_binaria(self.dat, cuenta, self._clave, self.log)
        if ok:
            self.log(f"✔ Encontrado en la posición {pos}.")
            self.tocadas = [pos]
            return pos, self._ver(self.dat, pos)[1]
        self.log("✖ No existe.")
        return None

    def insertar(self, reg):
        self.log(f"Se busca el lugar de inserción de {reg.clave:07d}:")
        ok, pos = busqueda_binaria(self.dat, reg.clave, self._clave, self.log)
        if ok:
            raise ValueError("Ya existe un registro con ese número de cuenta.")
        n = self.dat.n()
        if pos < n:
            self.log(f"Se desplazan {n - pos} registro(s) una posición hacia abajo para abrir hueco en pos {pos}.")
        else:
            self.log(f"Va al final del archivo (pos {pos}).")
        self.dat.insertar_en(pos, reg.a_bytes())
        self.log(f"Alta: escrito en pos {pos}, offset {pos * TAM_REG}.")
        self.tocadas = [pos]

    def actualizar(self, reg):
        r = self.buscar(reg.clave)
        if not r:
            raise ValueError("No existe esa cuenta.")
        self.dat.escribir(r[0], reg.a_bytes())
        self.log(f"Modificación: la clave no cambia, se sobrescribe en pos {r[0]} sin mover nada.")
        self.tocadas = [r[0]]

    def eliminar(self, cuenta):
        r = self.buscar(cuenta)
        if not r:
            raise ValueError("No existe esa cuenta.")
        n = self.dat.n()
        self.dat.quitar_en(r[0])
        self.log(f"Baja física: se recorren {n - r[0] - 1} registro(s) hacia arriba y se trunca el archivo.")
        self.tocadas = []
