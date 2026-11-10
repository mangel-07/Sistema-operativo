"""Organización serial (heap)."""
from modelo.almacenamiento import Bin, busqueda_binaria
from organizaciones.base import Archivo
from modelo.registro import ACTIVO, BORRADO, VACIO, ESTADOS, TAM_REG, decodificar, Registro


class ArchivoSerial(Archivo):
    nombre = "Serial (heap)"
    descripcion = ("Los registros se guardan al final, en orden de llegada. Búsqueda lineal. "
                   "La baja es lógica (marca '*'); el espacio se recupera al reorganizar.")
    archivos = ("serial.dat",)

    def _abrir(self):
        self.dat = Bin(self.ruta("serial.dat"), TAM_REG)

    def buscar(self, cuenta):
        self.log(f"Búsqueda lineal de la cuenta {cuenta:07d}:")
        for i in range(self.dat.n()):
            est, reg = self._ver(self.dat, i)
            self.log(f"  leer pos {i} (offset {i * TAM_REG}) → cuenta {reg.valores['cuenta']} [{ESTADOS[est]}]")
            if est == ACTIVO and reg.clave == cuenta:
                self.log(f"✔ Encontrado en la posición {i}.")
                self.tocadas = [i]
                return i, reg
        self.log("✖ Se llegó al final del archivo sin encontrarla.")
        return None

    def insertar(self, reg):
        if self.buscar(reg.clave):
            raise ValueError("Ya existe un registro con ese número de cuenta.")
        pos = self.dat.n()
        self.dat.escribir(pos, reg.a_bytes())
        self.log(f"Alta: se agrega al final → pos {pos}, offset {pos * TAM_REG}, {TAM_REG} bytes.")
        self.tocadas = [pos]

    def actualizar(self, reg):
        r = self.buscar(reg.clave)
        if not r:
            raise ValueError("No existe esa cuenta.")
        self.dat.escribir(r[0], reg.a_bytes())
        self.log(f"Modificación: se sobrescribe en el mismo lugar (pos {r[0]}), mismo tamaño fijo.")
        self.tocadas = [r[0]]

    def eliminar(self, cuenta):
        r = self.buscar(cuenta)
        if not r:
            raise ValueError("No existe esa cuenta.")
        self.dat.escribir(r[0], r[1].a_bytes(BORRADO))
        self.log(f"Baja lógica: se cambia el byte de estado a '*' en pos {r[0]}. El registro sigue ocupando espacio.")
        self.tocadas = [r[0]]

    def reorganizar(self):
        vivos = [r for _, e, r in self.listar() if e == ACTIVO]
        antes = self.dat.n()
        self.dat.reiniciar(b"".join(r.a_bytes() for r in vivos))
        self.log(f"Reorganización: se reescribe el archivo sin bajas lógicas ({antes} → {len(vivos)} posiciones).")
        self.tocadas = []
