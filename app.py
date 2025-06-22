import customtkinter as ctk

from src.core.gerencia_usuarios import GerenciaUsuarios
from interface.entrar import TelaEntrar
from interface.cadastrar import TelaCadastro
from interface.home import TelaInicial

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stock Variation Predictor")
        self.geometry("700x400")

        self.gerencia_usuario = GerenciaUsuarios()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F, name in [(TelaEntrar, "Login"), (TelaCadastro, "Cadastro"), (TelaInicial, "Home")]:
            frame = F(container, self) 
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.mostrar_frame("Login")

    def mostrar_frame(self, frame_atual):
        frame = self.frames[frame_atual]
        frame.tkraise()
        
    def cadastrar_usuario(self, nome, senha):
        return self.gerencia_usuario.cadastrar_usuario(nome, senha)

    def checar_senha(self, nome, senha):
        return self.gerencia_usuario.checar_senha(nome, senha)
