import customtkinter as ctk
from PIL import Image

class TelaInicial(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(fg_color="#2b2b2b")  # Fundo cinza médio

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Topo
        self.header_frame = ctk.CTkFrame(self, fg_color="#3a3a3a")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure((1, 2, 3), weight=1)

        logo_img = ctk.CTkImage(light_image=Image.open("interface/imagens/logo.png"), size=(120, 80))
        logo_label = ctk.CTkLabel(self.header_frame, image=logo_img, text="")
        logo_label.grid(row=0, column=0, padx=(0, 10))

        welcome_label = ctk.CTkLabel(
            self.header_frame,
            text=f"Bem-vindo(a), Invetstidor.",
            font=("Arial", 16),
            text_color="white"
        )
        welcome_label.grid(row=0, column=1, sticky="w")

        logout_button = ctk.CTkButton(
            self.header_frame, text="Sair",
            command=lambda: self.controller.mostrar_frame("Login")
        )
        logout_button.grid(row=0, column=4, padx=(10, 0))

        # Cards
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, padx=20, pady=20, sticky="n")
        self.cards_frame.grid_columnconfigure((0, 1), weight=1)

        card1 = self.criar_card("📊 Comparar Modelos", "Comparar")
        card1.grid(row=0, column=0, padx=20, pady=10)

        card2 = self.criar_card("💸 Simular Investimento", "Simular")
        card2.grid(row=0, column=1, padx=20, pady=10)

    def criar_card(self, titulo, frame_destino):
        card = ctk.CTkFrame(self.cards_frame, fg_color="#444", corner_radius=10)
        label = ctk.CTkLabel(card, text=titulo, font=("Arial", 18), text_color="white")
        label.pack(pady=10, padx=20)

        botao = ctk.CTkButton(card, text="Abrir", command=lambda: self.controller.mostrar_frame(frame_destino))
        botao.pack(pady=10)

        return card
