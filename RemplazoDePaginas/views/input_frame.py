import customtkinter as ctk

from controllers.simulador_controller import ALGORITHMS


class InputFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_simulate,
        on_clear,
    ) -> None:
        super().__init__(master, corner_radius=12)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="Configuración de la simulación", font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 10))

        ctk.CTkLabel(self, text="Cadena de referencia").grid(
            row=1, column=0, sticky="w", padx=18, pady=(4, 5)
        )
        self.references_entry = ctk.CTkTextbox(self, height=78, wrap="word")
        self.references_entry.grid(row=2, column=0, sticky="ew", padx=18)
        self.references_entry.insert("1.0", "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2")

        ctk.CTkLabel(
            self, text="Para Segunda oportunidad puedes indicar lectura/escritura: 2:R, 4:W."
        ).grid(row=3, column=0, sticky="w", padx=18, pady=(5, 10))

        settings = ctk.CTkFrame(self, fg_color="transparent")
        settings.grid(row=4, column=0, sticky="ew", padx=18, pady=(2, 10))
        settings.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(settings, text="Número de marcos").grid(row=0, column=0, sticky="w")
        self.frames_entry = ctk.CTkEntry(settings, width=90)
        self.frames_entry.insert(0, "3")
        self.frames_entry.grid(row=0, column=1, sticky="w", padx=(10, 0))

        ctk.CTkLabel(settings, text="Algoritmo").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.algorithm_menu = ctk.CTkOptionMenu(
            settings, values=list(ALGORITHMS), width=230
        )
        self.algorithm_menu.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(10, 0))

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.grid(row=5, column=0, sticky="ew", padx=18, pady=(4, 18))
        ctk.CTkButton(buttons, text="Simular", command=on_simulate).pack(
            side="left", padx=(0, 8)
        )
        ctk.CTkButton(
            buttons, text="Limpiar", command=on_clear, fg_color="transparent",
            border_width=1, text_color=("gray10", "gray90"),
        ).pack(side="left")

    def get_values(self) -> tuple[str, str, str]:
        return (
            self.references_entry.get("1.0", "end").strip(),
            self.frames_entry.get(),
            self.algorithm_menu.get(),
        )

    def clear(self) -> None:
        self.references_entry.delete("1.0", "end")
        self.frames_entry.delete(0, "end")
        self.frames_entry.insert(0, "3")