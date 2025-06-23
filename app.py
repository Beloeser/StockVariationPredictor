import customtkinter as ctk
from interface import *
from src.core.gerencia_usuarios import GerenciaUsuarios

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stock Variation Predictor")
        self.iconbitmap("interface\imagens\logo.ico")
        self.geometry("700x400")

        self.gerencia_usuario = GerenciaUsuarios()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F, name in [(TelaEntrar, "Login"), (TelaCadastro, "Cadastro"), (TelaInicial, "Home"), (TelaComparar, "Comparar"), (TelaSimular, "Simular")]:
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
