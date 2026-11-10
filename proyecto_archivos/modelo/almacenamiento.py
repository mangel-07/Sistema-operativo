"""Archivo binario de registros de tamaño fijo (acceso por posición) y búsqueda binaria."""
import os


class Bin:
    def __init__(self, ruta, tam, inicial=b""):
        self.ruta, self.tam = ruta, tam
        if not os.path.exists(ruta):
            with open(ruta, "wb") as f:
                f.write(inicial)

    def n(self):
        return os.path.getsize(self.ruta) // self.tam

    def leer(self, i):
        with open(self.ruta, "rb") as f:
            f.seek(i * self.tam)
            d = f.read(self.tam)
        return d if len(d) == self.tam else None

    def escribir(self, i, datos):
        with open(self.ruta, "r+b") as f:
            f.seek(i * self.tam)
            f.write(datos)

    def insertar_en(self, i, datos):          # desplaza la cola hacia abajo
        with open(self.ruta, "r+b") as f:
            f.seek(i * self.tam)
            cola = f.read()
            f.seek(i * self.tam)
            f.write(datos + cola)

    def quitar_en(self, i):                   # recorre la cola hacia arriba
        with open(self.ruta, "r+b") as f:
            f.seek((i + 1) * self.tam)
            cola = f.read()
            f.seek(i * self.tam)
            f.write(cola)
            f.truncate()

    def reiniciar(self, inicial=b""):
        with open(self.ruta, "wb") as f:
            f.write(inicial)


def busqueda_binaria(arch, clave, extraer, log):
    """Devuelve (encontrado, posición). Si no existe, posición = lugar de inserción."""
    lo, hi = 0, arch.n() - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        k = extraer(arch.leer(mid))
        log(f"  [lo={lo}, hi={hi}] leer pos {mid} (offset {mid * arch.tam}) → clave {k:07d}")
        if k == clave:
            return True, mid
        if k < clave:
            lo = mid + 1
        else:
            hi = mid - 1
    return False, lo
