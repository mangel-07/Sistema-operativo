import customtkinter as ctk

from controllers.simulador_controller import SimuladorController
from models.base_algorithm import SimulationResult
from views.input_frame import InputFrame
from views.table_frame import TableFrame


class PaginasFrame(ctk.CTkFrame):
    """Contenido completo del simulador; se puede incrustar en una pestaña."""

    def __init__(self, master) -> None:
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(
            self,
            text="Simulador de reemplazo de páginas",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 12))

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        content.grid_columnconfigure(0, weight=0)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        self.table_frame = TableFrame(content)
        self.table_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.input_frame = InputFrame(content, self._simulate, self._clear)
        self.input_frame.grid(row=0, column=0, sticky="ns")

        self.controller = SimuladorController(
            self.input_frame.get_values,
            self._show_result,
            self._show_error,
            self._clear_views,
        )
        self.error_label = ctk.CTkLabel(
            self.input_frame, text="", text_color=("#B42318", "#FF8A80"),
            wraplength=250, justify="left",
        )
        self.error_label.grid(row=6, column=0, sticky="w", padx=18, pady=(0, 12))

    def _simulate(self) -> None:
        self.error_label.configure(text="")
        self.controller.simulate()

    def _clear(self) -> None:
        self.controller.clear()
        self.error_label.configure(text="")

    def _show_result(self, result: SimulationResult, algorithm_name: str) -> None:
        self.table_frame.display(result, algorithm_name)

    def _show_error(self, message: str) -> None:
        self.error_label.configure(text=message)

    def _clear_views(self) -> None:
        self.input_frame.clear()
        self.table_frame.clear_table()


class AppWindow(ctk.CTk):
    """Ventana independiente (python main.py dentro de RemplazoDePaginas)."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Simulador de reemplazo de páginas")
        self.geometry("1120x700")
        self.minsize(760, 560)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        PaginasFrame(self).grid(row=0, column=0, sticky="nsew")
