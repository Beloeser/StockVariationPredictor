import customtkinter as ctk

class TelaEntrar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Entrar no Sistema", font=("Arial", 24))
        self.label.pack(pady=(40, 20), padx=20)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Digite seu nome de usuário", width=300)
        self.name_entry.pack(pady=10, padx=20)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Digite sua senha", show="*", width=300)
        self.password_entry.pack(pady=10, padx=20)

        self.login_button = ctk.CTkButton(self, text="Entrar", command=self.executar_login, width=300)
        self.login_button.pack(pady=20, padx=20)

        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.pack(pady=10)

        self.go_to_register_button = ctk.CTkButton(
            self,
            text="Não tem uma conta? Cadastre-se",
            fg_color="transparent",
            hover_color="#555",
            command=lambda: self.controller.mostrar_frame("Cadastro")
        )
        self.go_to_register_button.pack(pady=(20, 10))

    def executar_login(self):
        nome = self.name_entry.get()
        senha = self.password_entry.get()

        autenticacao = self.controller.checar_senha(nome, senha)

        if autenticacao:
            self.status_label.configure(text="Login bem sucedido!", text_color="green")
            self.controller.mostrar_frame("Home")
        else:
            self.status_label.configure(text="Nome de usuario ou senha incorretos.", text_color="red")