"""Interfaz gráfica (customtkinter)."""
import os
from tkinter import ttk, messagebox

import customtkinter as ctk

from modelo.registro import CAMPOS, ACTIVO, BORRADO, VACIO, ESTADOS, TAM_REG, Registro
from organizaciones import ORGS


FUENTE = "Roboto"


class ArchivosFrame(ctk.CTkFrame):
    """Contenido completo del simulador; se puede incrustar en una pestaña."""

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.carpeta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datos")
        os.makedirs(self.carpeta, exist_ok=True)
        self.filas = {}
        self.entradas = {}
        self.archivo = None
        self._estilo_tablas()
        self._armar()
        self._cambiar_org(next(iter(ORGS)))

    # ---------------------------------------------------------- construcción
    def _estilo_tablas(self):
        e = ttk.Style(self)
        e.theme_use("clam")
        e.configure("Treeview", background="#242424", fieldbackground="#242424", foreground="#e5e7eb",
                    rowheight=28, borderwidth=0, font=(FUENTE, 11))
        e.configure("Treeview.Heading", background="#334155", foreground="white", relief="flat",
                    font=(FUENTE, 11, "bold"))
        e.map("Treeview", background=[("selected", "#1f6aa5")], foreground=[("selected", "white")])
        e.map("Treeview.Heading", background=[("active", "#3b4a60")])

    def _armar(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(self, text="Simulador de organización de archivos",
                     font=ctk.CTkFont(FUENTE, 26, "bold")).grid(row=0, column=0, columnspan=2,
                                                                 sticky="w", padx=18, pady=(14, 8))
        self._panel_izq()
        self._panel_der()

    def _panel_izq(self):
        izq = ctk.CTkFrame(self, corner_radius=14, width=430)
        izq.grid(row=1, column=0, sticky="ns", padx=(14, 7), pady=(0, 14))
        izq.grid_propagate(False)
        ctk.CTkLabel(izq, text="Configuración", font=ctk.CTkFont(FUENTE, 20, "bold")
                     ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(18, 10))

        ctk.CTkLabel(izq, text="Organización", font=ctk.CTkFont(FUENTE, 13, "bold")
                     ).grid(row=1, column=0, sticky="w", padx=(20, 6), pady=4)
        self.org_var = ctk.StringVar()
        ctk.CTkOptionMenu(izq, values=list(ORGS), variable=self.org_var, width=220,
                          command=self._cambiar_org).grid(row=1, column=1, sticky="w", pady=4)
        self.lbl_desc = ctk.CTkLabel(izq, text="", wraplength=385, justify="left",
                                     font=ctk.CTkFont(FUENTE, 12), text_color="#9ca3af")
        self.lbl_desc.grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(4, 10))

        ctk.CTkLabel(izq, text="Datos del registro (longitud fija)", font=ctk.CTkFont(FUENTE, 13, "bold")
                     ).grid(row=3, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 4))
        for i, (k, etq, largo, _t) in enumerate(CAMPOS):
            ctk.CTkLabel(izq, text=f"{etq} ({largo})", font=ctk.CTkFont(FUENTE, 12)
                         ).grid(row=4 + i, column=0, sticky="w", padx=(20, 6), pady=3)
            var = ctk.StringVar()
            var.trace_add("write", lambda *_a, v=var, l=largo: v.set(v.get()[:l]) if len(v.get()) > l else None)
            ent = ctk.CTkEntry(izq, textvariable=var, width=220)
            ent.grid(row=4 + i, column=1, sticky="w", pady=3)
            self.entradas[k] = var

        bt = ctk.CTkFrame(izq, fg_color="transparent")
        bt.grid(row=14, column=0, columnspan=2, sticky="w", padx=20, pady=(16, 0))
        botones = [
            ("Alta", self.alta, {}), ("Buscar", self.buscar, {}),
            ("Modificar", self.modificar, {}),
            ("Baja", self.baja, {"fg_color": "#8a3b3b", "hover_color": "#a04848"}),
            ("Reorganizar", self.reorganizar, {"fg_color": "transparent", "border_width": 1}),
            ("Limpiar campos", self.limpiar, {"fg_color": "transparent", "border_width": 1}),
            ("Reiniciar archivo", self.reiniciar, {"fg_color": "transparent", "border_width": 1}),
        ]
        for i, (txt, cmd, kw) in enumerate(botones):
            ctk.CTkButton(bt, text=txt, command=cmd, width=120, **kw).grid(
                row=i // 3, column=i % 3, padx=(0, 8), pady=5)

    def _panel_der(self):
        der = ctk.CTkFrame(self, corner_radius=14)
        der.grid(row=1, column=1, sticky="nsew", padx=(7, 14), pady=(0, 14))
        der.grid_columnconfigure(0, weight=1)
        der.grid_rowconfigure(1, weight=1)
        self.lbl_res = ctk.CTkLabel(der, text="", font=ctk.CTkFont(FUENTE, 20, "bold"))
        self.lbl_res.grid(row=0, column=0, sticky="w", padx=20, pady=(18, 6))

        self.tabs = ctk.CTkTabview(der)
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 6))
        for t in ("Archivo de datos", "Estructura", "Bitácora"):
            self.tabs.add(t)
            self.tabs.tab(t).grid_columnconfigure(0, weight=1)

        # --- datos
        t = self.tabs.tab("Archivo de datos")
        t.grid_rowconfigure(0, weight=1)
        cols = ["Pos", "Offset", "Estado"] + [c[1] for c in CAMPOS]
        anchos = [50, 70, 90, 85, 120, 125, 100, 120, 90, 120, 120, 100]
        marco, self.t_datos = self._tabla(t, cols, anchos)
        marco.grid(row=0, column=0, sticky="nsew")
        self.t_datos.tag_configure("borrado", background="#6e4444")
        self.t_datos.tag_configure("vacio", foreground="#6b7280")
        self.t_datos.tag_configure("nuevo", background="#6b5f2e")
        self.t_datos.bind("<<TreeviewSelect>>", self._al_seleccionar)

        # --- estructura
        t = self.tabs.tab("Estructura")
        t.grid_rowconfigure(1, weight=1)
        self.lbl_est = ctk.CTkLabel(t, text="", font=ctk.CTkFont(FUENTE, 12), text_color="#9ca3af",
                                    wraplength=800, justify="left")
        self.lbl_est.grid(row=0, column=0, sticky="w", padx=6, pady=(4, 6))
        marco, self.t_est = self._tabla(t, ["—"], [120])
        marco.grid(row=1, column=0, sticky="nsew")

        # --- bitácora
        t = self.tabs.tab("Bitácora")
        t.grid_rowconfigure(0, weight=1)
        self.txt = ctk.CTkTextbox(t, font=("DejaVu Sans Mono", 12), wrap="word")
        self.txt.grid(row=0, column=0, sticky="nsew")
        self.txt.configure(state="disabled")

        self.lbl_pie = ctk.CTkLabel(der, text="", font=ctk.CTkFont(FUENTE, 13, "bold"))
        self.lbl_pie.grid(row=2, column=0, sticky="w", padx=20, pady=(2, 14))

    def _tabla(self, padre, columnas, anchos):
        marco = ctk.CTkFrame(padre, fg_color="transparent")
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)
        tv = ttk.Treeview(marco, columns=columnas, show="headings", selectmode="browse")
        sy = ctk.CTkScrollbar(marco, command=tv.yview)
        sx = ctk.CTkScrollbar(marco, orientation="horizontal", command=tv.xview)
        tv.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        tv.grid(row=0, column=0, sticky="nsew")
        sy.grid(row=0, column=1, sticky="ns")
        sx.grid(row=1, column=0, sticky="ew")
        self._config_cols(tv, columnas, anchos)
        return marco, tv

    @staticmethod
    def _config_cols(tv, columnas, anchos):
        tv["columns"] = columnas
        for c, a in zip(columnas, anchos):
            tv.heading(c, text=c)
            tv.column(c, width=a, anchor="center", stretch=False)

    # ----------------------------------------------------------- utilidades
    def _log(self, msg):
        self.txt.configure(state="normal")
        self.txt.insert("end", msg + "\n")
        self.txt.see("end")
        self.txt.configure(state="disabled")

    def _leer_form(self):
        return Registro(**{k: v.get() for k, v in self.entradas.items()})

    def _llenar(self, reg):
        for k, v in self.entradas.items():
            v.set(reg.valores[k])

    def _refrescar(self, resaltar=()):
        tv = self.t_datos
        tv.delete(*tv.get_children())
        self.filas = {}
        activos = 0
        filas = self.archivo.listar()
        for pos, est, reg in filas:
            if est == ACTIVO:
                activos += 1
            vacio = est == VACIO
            vals = [pos, pos * TAM_REG, ESTADOS[est]] + (["—"] * len(CAMPOS) if vacio
                                                         else [reg.valores[k] for k, *_ in CAMPOS])
            tag = "vacio" if vacio else "borrado" if est == BORRADO else ""
            if pos in resaltar and est == ACTIVO:
                tag = "nuevo"
            tv.insert("", "end", iid=str(pos), values=vals, tags=(tag,))
            self.filas[str(pos)] = (est, reg)
        if resaltar and tv.exists(str(resaltar[0])):
            tv.see(str(resaltar[0]))

        titulo, cols, datos = self.archivo.estructura()
        self.lbl_est.configure(text=titulo)
        self._config_cols(self.t_est, cols, [140] * len(cols))
        self.t_est.delete(*self.t_est.get_children())
        for f in datos:
            self.t_est.insert("", "end", values=list(f))

        nombres = " + ".join(self.archivo.archivos)
        self.lbl_pie.configure(
            text=f"Registros activos: {activos} de {len(filas)} posiciones   |   "
                 f"Tamaño del registro: {TAM_REG} bytes   |   Archivo: {nombres}")

    def _cambiar_org(self, nombre):
        self.archivo = ORGS[nombre](self.carpeta, self._log)
        self.org_var.set(nombre)
        self.lbl_desc.configure(text=self.archivo.descripcion)
        self.lbl_res.configure(text=f"Resultados — {nombre}")
        self._log(f"══ Organización: {nombre} ══")
        self._refrescar()

    def _al_seleccionar(self, _e):
        sel = self.t_datos.selection()
        if sel and sel[0] in self.filas:
            est, reg = self.filas[sel[0]]
            if est == ACTIVO:
                self._llenar(reg)

    def _ejecutar(self, titulo, fn, mostrar_error=True):
        self._log(f"\n── {titulo} ──")
        try:
            fn()
        except ValueError as e:
            self._log(f"✖ {e}")
            if mostrar_error:
                messagebox.showerror("No se pudo completar", str(e))
        self._refrescar(self.archivo.tocadas)

    # ----------------------------------------------------------- operaciones
    def alta(self):
        def f():
            reg = self._leer_form()
            reg.validar()
            self.archivo.insertar(reg)
        self._ejecutar("ALTA", f)

    def buscar(self):
        def f():
            txt = self.entradas["cuenta"].get().strip()
            Registro.validar_cuenta(txt)
            r = self.archivo.buscar(int(txt))
            if r:
                self._llenar(r[1])
            else:
                messagebox.showinfo("Búsqueda", "No se encontró esa cuenta.")
        self.archivo.tocadas = []
        self._ejecutar("BÚSQUEDA", f)

    def modificar(self):
        def f():
            reg = self._leer_form()
            reg.validar()
            self.archivo.actualizar(reg)
        self._ejecutar("MODIFICACIÓN (la cuenta es la llave y no cambia)", f)

    def baja(self):
        def f():
            txt = self.entradas["cuenta"].get().strip()
            Registro.validar_cuenta(txt)
            self.archivo.eliminar(int(txt))
            self.limpiar()
        self._ejecutar("BAJA", f)

    def reorganizar(self):
        self._ejecutar("REORGANIZAR", self.archivo.reorganizar)

    def limpiar(self):
        for v in self.entradas.values():
            v.set("")

    def reiniciar(self):
        if messagebox.askyesno("Reiniciar", "¿Borrar todos los registros de esta organización?"):
            self.archivo.reiniciar()
            self._log("\n── ARCHIVO REINICIADO ──")
            self._refrescar()


class App(ctk.CTk):
    """Ventana independiente (python main.py dentro de proyecto_archivos)."""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        super().__init__()
        self.title("Simulador de organización de archivos")
        self.geometry("1360x840")
        self.minsize(1150, 720)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        ArchivosFrame(self).grid(row=0, column=0, sticky="nsew")
