"""Organización indexada (datos + índice)."""
from modelo.almacenamiento import Bin, busqueda_binaria
from organizaciones.base import Archivo
from modelo.registro import ACTIVO, BORRADO, VACIO, ESTADOS, TAM_REG, decodificar, Registro


TAM_IDX = 13   # cuenta (7) + posición en datos (6)


class ArchivoIndexado(Archivo):
    nombre = "Indexada"
    descripcion = ("Archivo de datos en orden de llegada + archivo de índice ordenado (cuenta → posición). "
                   "Se busca en el índice con búsqueda binaria y luego se salta al dato.")
    archivos = ("indexado.dat", "indexado.idx")

    def _abrir(self):
        self.dat = Bin(self.ruta("indexado.dat"), TAM_REG)
        self.idx = Bin(self.ruta("indexado.idx"), TAM_IDX)

    @staticmethod
    def _k(d):
        return int(d[:7])

    def _buscar_idx(self, cuenta):
        self.log(f"Búsqueda binaria en el ÍNDICE de la cuenta {cuenta:07d}:")
        return busqueda_binaria(self.idx, cuenta, self._k, self.log)

    def buscar(self, cuenta):
        ok, i = self._buscar_idx(cuenta)
        if not ok:
            self.log("✖ No está en el índice.")
            return None
        pos = int(self.idx.leer(i)[7:])
        self.log(f"✔ Entrada de índice {i} → apunta a la posición {pos} del archivo de datos (offset {pos * TAM_REG}).")
        self.tocadas = [pos]
        return pos, self._ver(self.dat, pos)[1]

    def insertar(self, reg):
        ok, i = self._buscar_idx(reg.clave)
        if ok:
            raise ValueError("Ya existe un registro con ese número de cuenta.")
        pos = self.dat.n()
        self.dat.escribir(pos, reg.a_bytes())
        self.log(f"Dato agregado al final del archivo de datos: pos {pos}.")
        self.idx.insertar_en(i, f"{reg.clave:07d}{pos:06d}".encode())
        self.log(f"Índice: se inserta la entrada {reg.clave:07d} → {pos} en el lugar {i} (el índice se mantiene ordenado).")
        self.tocadas = [pos]

    def actualizar(self, reg):
        r = self.buscar(reg.clave)
        if not r:
            raise ValueError("No existe esa cuenta.")
        self.dat.escribir(r[0], reg.a_bytes())
        self.log(f"Modificación: se sobrescribe el dato en pos {r[0]}; el índice no cambia.")
        self.tocadas = [r[0]]

    def eliminar(self, cuenta):
        ok, i = self._buscar_idx(cuenta)
        if not ok:
            raise ValueError("No existe esa cuenta.")
        pos = int(self.idx.leer(i)[7:])
        reg = self._ver(self.dat, pos)[1]
        self.dat.escribir(pos, reg.a_bytes(BORRADO))
        self.idx.quitar_en(i)
        self.log(f"Baja: dato marcado '*' en pos {pos} y se elimina su entrada del índice (lugar {i}).")
        self.tocadas = [pos]

    def reorganizar(self):
        vivos = sorted((r for _, e, r in self.listar() if e == ACTIVO), key=lambda r: r.clave)
        self.dat.reiniciar(b"".join(r.a_bytes() for r in vivos))
        self.idx.reiniciar(b"".join(f"{r.clave:07d}{p:06d}".encode() for p, r in enumerate(vivos)))
        self.log(f"Reorganización: datos compactados ({len(vivos)} registros) e índice reconstruido.")
        self.tocadas = []

    def estructura(self):
        filas = []
        for i in range(self.idx.n()):
            d = self.idx.leer(i)
            filas.append((i, d[:7].decode(), int(d[7:])))
        return ("Archivo de índice (indexado.idx): entradas ordenadas por cuenta, 13 bytes cada una.",
                ("Entrada", "Cuenta", "Posición en datos"), filas)
