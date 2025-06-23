import customtkinter as ctk

class TelaInicial(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.header_frame.grid_columnconfigure(3, weight=1)

        self.comparar_button = ctk.CTkButton(self.header_frame, text="Comparar", width=120, command=lambda: self.controller.mostrar_frame("Comparar"))
        self.comparar_button.grid(row=0, column=0, padx=(0, 10))

        self.salvos_button = ctk.CTkButton(self.header_frame, text="Salvos", width=120)
        self.salvos_button.grid(row=0, column=1, padx=0)

        self.simular_button = ctk.CTkButton(self.header_frame, text="Simular", width=120, command=lambda: self.controller.mostrar_frame("Simular"))
        self.simular_button.grid(row=0, column=2, padx=10)
        
        self.image_placeholder = ctk.CTkFrame(self.header_frame, fg_color="#555555", width=100, height=28)
        self.image_placeholder.grid(row=0, column=4, sticky="ns")

        self.welcome_label = ctk.CTkLabel(self, text="Selecione uma opção acima para começar", font=("Arial", 20))
        self.welcome_label.grid(row=1, column=0, padx=20, pady=20)