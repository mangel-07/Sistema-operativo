import customtkinter as ctk

from models.base_algorithm import SimulationResult


class TableFrame(ctk.CTkFrame):
    REFERENCE_COLOR = ("#FFF59D", "#695F2D")
    FAULT_COLOR = ("#F7C5C5", "#754747")
    NORMAL_COLOR = ("#F4F6F8", "#292D32")
    HEADER_COLOR = ("#DCE7F2", "#343E4A")

    def __init__(self, master) -> None:
        super().__init__(master, corner_radius=12)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self, text="Tabla de estados", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        self.table_scroll = ctk.CTkScrollableFrame(
            self, orientation="horizontal", height=330, corner_radius=8
        )
        self.table_scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))
        self.summary = ctk.CTkLabel(
            self, text="Ingresa una cadena y presiona Simular.",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.summary.grid(row=2, column=0, sticky="w", padx=16, pady=(2, 14))
        self.clear_table()

    def display(self, result: SimulationResult, algorithm_name: str) -> None:
        self.clear_table()
        self.title.configure(text=f"Resultados — {algorithm_name}")

        self._cell(0, 0, "time", self.HEADER_COLOR, width=110, bold=True)
        for column, step in enumerate(result.steps, start=1):
            self._cell(0, column, str(step.time), self.HEADER_COLOR, width=82, bold=True)

        self._cell(1, 0, "Referencia", self.REFERENCE_COLOR, width=110, bold=True)
        for column, step in enumerate(result.steps, start=1):
            reference = str(step.reference.page)
            if step.reference.operation == "W":
                reference += ":W"
            self._cell(1, column, reference, self.REFERENCE_COLOR, width=82)

        for frame in range(result.frame_count):
            self._cell(frame + 2, 0, str(frame), self.REFERENCE_COLOR, width=110, bold=True)
            for column, step in enumerate(result.steps, start=1):
                value = step.memory[frame]
                text = "—" if value is None else str(value)
                if step.reference_bits:
                    text += f"\nR={step.reference_bits[frame]}"
                if step.modified_bits:
                    text += f" M={step.modified_bits[frame]}"
                previous_memory = (
                    result.steps[column - 2].memory
                    if column > 1
                    else (None,) * result.frame_count
                )
                changed_frame = step.fault and step.memory[frame] != previous_memory[frame]
                color = self.FAULT_COLOR if changed_frame else self.NORMAL_COLOR
                self._cell(frame + 2, column, text, color, width=82)

        self.summary.configure(
            text=(
                f"Fallos de página: {result.page_faults} de {len(result.steps)} referencias"
                f"    |    Tiempos con fallo: {', '.join(map(str, result.fault_times)) or 'ninguno'}"
            )
        )

    def clear_table(self) -> None:
        for child in self.table_scroll.winfo_children():
            child.destroy()
        self._cell(0, 0, "time", self.HEADER_COLOR, width=110, bold=True)
        self.summary.configure(text="Ingresa una cadena y presiona Simular.")
        self.title.configure(text="Tabla de estados")

    def _cell(
        self, row: int, column: int, text: str, color: str | tuple[str, str],
        width: int, bold: bool = False,
    ) -> None:
        label = ctk.CTkLabel(
            self.table_scroll,
            text=text,
            width=width,
            height=48,
            fg_color=color,
            corner_radius=5,
            font=ctk.CTkFont(size=12, weight="bold" if bold else "normal"),
        )
        label.grid(row=row, column=column, padx=2, pady=2, sticky="nsew")