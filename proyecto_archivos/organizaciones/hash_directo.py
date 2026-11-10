"""Organización hash (dirección directa con sondeo lineal)."""
from modelo.almacenamiento import Bin, busqueda_binaria
from organizaciones.base import Archivo
from modelo.registro import ACTIVO, BORRADO, VACIO, ESTADOS, TAM_REG, decodificar, Registro


class ArchivoHash(Archivo):
    nombre = "Hash (directa)"
    descripcion = ("Dirección = cuenta mod 31. El archivo tiene 31 casillas fijas. Las colisiones se "
                   "resuelven con sondeo lineal (siguiente casilla libre). La baja deja una marca '*'.")
    archivos = ("hash.dat",)
    M = 31

    def _abrir(self):
        self.dat = Bin(self.ruta("hash.dat"), TAM_REG, b" " * TAM_REG * self.M)

    def _sonda(self, cuenta):
        h = cuenta % self.M
        return h, [(h + k) % self.M for k in range(self.M)]

    def buscar(self, cuenta):
        h, ruta = self._sonda(cuenta)
        self.log(f"h({cuenta:07d}) = {cuenta} mod {self.M} = {h}. Se sondea desde la casilla {h}:")
        for p in ruta:
            est, reg = self._ver(self.dat, p)
            if est == VACIO:
                self.log(f"  casilla {p} vacía → la cuenta no existe.")
                return None
            if est == ACTIVO and reg.clave == cuenta:
                self.log(f"✔ Encontrado en la casilla {p}" + ("" if p == h else " (por colisión)") + ".")
                self.tocadas = [p]
                return p, reg
            self.log(f"  casilla {p} ocupada por otra cuenta [{ESTADOS[est]}] → siguiente.")
        self.log("✖ Se recorrió toda la tabla.")
        return None

    def insertar(self, reg):
        if self.buscar(reg.clave):
            raise ValueError("Ya existe un registro con ese número de cuenta.")
        h, ruta = self._sonda(reg.clave)
        for p in ruta:
            if self._ver(self.dat, p)[0] != ACTIVO:
                self.dat.escribir(p, reg.a_bytes())
                if p == h:
                    self.log(f"Alta: casilla {h} libre → se escribe en offset {p * TAM_REG}.")
                else:
                    self.log(f"Alta: COLISIÓN en la casilla {h}; se usa la casilla {p} (offset {p * TAM_REG}).")
                self.tocadas = [p]
                return
        raise ValueError(f"La tabla está llena ({self.M} casillas). Elimine registros o reorganice.")

    def actualizar(self, reg):
        r = self.buscar(reg.clave)
        if not r:
            raise ValueError("No existe esa cuenta.")
        self.dat.escribir(r[0], reg.a_bytes())
        self.log(f"Modificación: se sobrescribe la casilla {r[0]}; la clave no cambia, así que sigue en su dirección.")
        self.tocadas = [r[0]]

    def eliminar(self, cuenta):
        r = self.buscar(cuenta)
        if not r:
            raise ValueError("No existe esa cuenta.")
        self.dat.escribir(r[0], r[1].a_bytes(BORRADO))
        self.log(f"Baja: casilla {r[0]} marcada '*' (lápida). No se deja vacía para no cortar cadenas de colisión.")
        self.tocadas = [r[0]]

    def reorganizar(self):
        vivos = [r for _, e, r in self.listar() if e == ACTIVO]
        self.dat.reiniciar(b" " * TAM_REG * self.M)
        for r in vivos:
            h, ruta = self._sonda(r.clave)
            p = next(p for p in ruta if self._ver(self.dat, p)[0] == VACIO)
            self.dat.escribir(p, r.a_bytes())
        self.log(f"Reorganización: se reinsertaron {len(vivos)} registros y se eliminaron las lápidas.")
        self.tocadas = []

    def estructura(self):
        filas = []
        for p, e, r in self.listar():
            if e == ACTIVO:
                h = r.clave % self.M
                filas.append((r.valores["cuenta"], h, p, "Sí" if p != h else "No"))
        return (f"Tabla hash: h(cuenta) = cuenta mod {self.M}. Casillas totales: {self.M}.",
                ("Cuenta", "h(cuenta)", "Casilla real", "Colisión"), filas)
