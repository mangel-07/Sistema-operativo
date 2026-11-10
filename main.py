"""Punto de entrada unificado:  python main.py

Reúne los dos proyectos de Sistemas Operativos en una sola ventana con pestañas.
Cada proyecto conserva su propia estructura de carpetas y sus imports.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
for proyecto in ("RemplazoDePaginas", "proyecto_archivos"):
    sys.path.insert(0, os.path.join(RAIZ, proyecto))

import customtkinter as ctk  # noqa: E402

from views.app_window import PaginasFrame  # noqa: E402  (RemplazoDePaginas)
from vista.app import ArchivosFrame  # noqa: E402  (proyecto_archivos)

PESTANAS = (
    ("Reemplazo de páginas", PaginasFrame),
    ("Organización de archivos", ArchivosFrame),
)


class VentanaPrincipal(ctk.CTk):
    def __init__(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        super().__init__()
        self.title("Sistemas Operativos — Simuladores")
        self.geometry("1360x840")
        self.minsize(1150, 720)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.pestanas = ctk.CTkTabview(self, corner_radius=12)
        self.pestanas.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.pestanas._segmented_button.configure(font=ctk.CTkFont(size=15, weight="bold"))

        for nombre, clase in PESTANAS:
            tab = self.pestanas.add(nombre)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
            clase(tab).grid(row=0, column=0, sticky="nsew")

        self.pestanas.set(PESTANAS[0][0])


if __name__ == "__main__":
    VentanaPrincipal().mainloop()
