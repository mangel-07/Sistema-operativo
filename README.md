# Sistemas Operativos — Simuladores

Una sola aplicación de escritorio (Python + CustomTkinter) con **dos pestañas**:

| Pestaña | Proyecto | Carpeta |
|---|---|---|
| Reemplazo de páginas | FIFO, LRU, Óptimo, Clock y Segunda oportunidad (R/M) — MVC | `RemplazoDePaginas/` |
| Organización de archivos | CRUD sobre Serial, Secuencial, Indexado y Hash con registros de longitud fija | `proyecto_archivos/` |

## Ejecutar

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Necesitas Tk instalado (Fedora: `sudo dnf install python3-tkinter`, Arch: `sudo pacman -S tk`).

## Estructura

```
SO/
├── main.py                  ← ventana con pestañas (único archivo a ejecutar)
├── requirements.txt
├── RemplazoDePaginas/       ← estructura original intacta
│   ├── controllers/  models/  utils/  views/  tests/
│   └── main.py              (sigue funcionando por separado)
└── proyecto_archivos/       ← estructura original intacta
    ├── modelo/  organizaciones/  vista/  datos/
    └── main.py              (sigue funcionando por separado)
```

Cada proyecto se puede seguir ejecutando solo (`python main.py` dentro de su carpeta).
Los datos del simulador de archivos se guardan en `proyecto_archivos/datos/`.

## Pruebas

```bash
cd RemplazoDePaginas && python -m unittest discover -s tests
```
