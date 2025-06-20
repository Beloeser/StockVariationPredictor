import customtkinter as ctk

class TelaCadastro(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Adicionar Novo Usuário", font=("Arial", 24))
        self.label.pack(pady=(40, 20), padx=20)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Digite o nome", width=300)
        self.name_entry.pack(pady=10, padx=20)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Digite a senha", show="*", width=300)
        self.password_entry.pack(pady=10, padx=20)

        self.save_button = ctk.CTkButton(self, text="Salvar", command=self.executar_cadastro, width=300)
        self.save_button.pack(pady=20, padx=20)

        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.pack(pady=10)
        
        # --- NOVO BOTÃO DE NAVEGAÇÃO ---
        # Este botão levará de volta para a tela de login.
        self.go_to_login_button = ctk.CTkButton(
            self,
            text="Já tem uma conta? Faça o login",
            fg_color="transparent",
            hover_color="#555",
            command=lambda: self.controller.mostrar_frame("Login")
        )
        self.go_to_login_button.pack(pady=(20, 10))

    def executar_cadastro(self):
        nome = self.name_entry.get()
        senha = self.password_entry.get()

        feito = self.controller.cadastrar_usuario(nome, senha)

        if feito:
            self.status_label.configure(text=f"Usuário '{nome}' foi salvo com sucesso!", text_color="green")
            self.name_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
        else:
            self.status_label.configure(text=f"Erro: Usuário já existe ou dados inválidos.", text_color="red")
