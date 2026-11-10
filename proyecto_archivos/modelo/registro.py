"""Estructura del registro de longitud fija y conversión a/desde bytes."""

# (clave, etiqueta, longitud, tipo)   tipo: alfa | num (hasta N) | numf (exacto N)
CAMPOS = [
    ("cuenta",    "Número de cuenta",   7,  "numf"),
    ("nombre",    "Nombre",             15, "alfa"),
    ("apellido",  "Apellido paterno",   15, "alfa"),
    ("telefono",  "Teléfono",           10, "numf"),
    ("calle",     "Calle",              15, "alfa"),
    ("numero",    "Núm. ext/int",       4,  "num"),
    ("colonia",   "Colonia",            15, "alfa"),
    ("municipio", "Municipio",          15, "alfa"),
    ("cp",        "Código postal",      5,  "numf"),
]
ACTIVO, BORRADO, VACIO = "A", "*", " "
ESTADOS = {ACTIVO: "Activo", BORRADO: "Baja lógica", VACIO: "Vacío"}
TAM_DATOS = sum(c[2] for c in CAMPOS)          # 101 bytes de datos
TAM_REG = 1 + TAM_DATOS                        # + 1 byte de estado = 102 bytes


class Registro:
    def __init__(self, **valores):
        self.valores = {k: str(valores.get(k, "")).strip() for k, *_ in CAMPOS}

    @property
    def clave(self):
        return int(self.valores["cuenta"])

    @staticmethod
    def validar_cuenta(texto):
        if not (texto.isascii() and texto.isdigit() and len(texto) == 7):
            raise ValueError("El número de cuenta debe tener exactamente 7 dígitos.")

    def validar(self):
        for k, etq, largo, tipo in CAMPOS:
            v = self.valores[k]
            if not v:
                raise ValueError(f"'{etq}' es obligatorio.")
            if len(v) > largo:
                raise ValueError(f"'{etq}' admite máximo {largo} caracteres.")
            if tipo in ("num", "numf"):
                if not (v.isascii() and v.isdigit()):
                    raise ValueError(f"'{etq}' debe ser numérico.")
                if tipo == "numf" and len(v) != largo:
                    raise ValueError(f"'{etq}' debe tener exactamente {largo} dígitos.")
            else:
                if not all(c.isalnum() or c == " " for c in v):
                    raise ValueError(f"'{etq}' debe ser alfanumérico.")
                try:
                    v.encode("latin-1")
                except UnicodeEncodeError:
                    raise ValueError(f"'{etq}' tiene caracteres no soportados.")

    def a_bytes(self, estado=ACTIVO):
        partes = []
        for k, _, largo, tipo in CAMPOS:
            v = self.valores[k]
            partes.append(v.zfill(largo) if tipo in ("num", "numf") else v.ljust(largo))
        return (estado + "".join(partes)).encode("latin-1")


def decodificar(datos):
    """bytes -> (estado, Registro)"""
    estado = chr(datos[0])
    texto = datos[1:].decode("latin-1")
    valores, i = {}, 0
    for k, _, largo, _t in CAMPOS:
        valores[k] = texto[i:i + largo].strip()
        i += largo
    return estado, Registro(**valores)
