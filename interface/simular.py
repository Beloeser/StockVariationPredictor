import customtkinter as ctk
from src.core.ativo import Ativo
from src.models.Treinadores.treinadorML import TreinadorML
from src.models.Treinadores.treinador_prophet import TreinadorProphet
import pandas as pd

class TelaSimular(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(list(range(9)), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Simulação de Investimento", font=("Arial", 24)).grid(
            row=0, column=0, pady=(30, 10), padx=20, sticky="n"
        )

        # Seletor de ativo
        self.ticker_box = ctk.CTkOptionMenu(self, values=Ativo.TICKERS_VALIDOS)
        self.ticker_box.grid(row=1, column=0, padx=80, pady=5, sticky="ew")

        # Seletor de modelo
        self.modelo_box = ctk.CTkOptionMenu(self, values=["LSTM", "Prophet"])
        self.modelo_box.grid(row=2, column=0, padx=80, pady=5, sticky="ew")

        # Seletor de período
        self.periodo_box = ctk.CTkOptionMenu(self, values=["1", "7", "15", "30"])
        self.periodo_box.set("30")
        self.periodo_box.grid(row=3, column=0, padx=80, pady=5, sticky="ew")

        # Valor investido
        self.valor_entry = ctk.CTkEntry(self, placeholder_text="Valor investido (R$)")
        self.valor_entry.grid(row=4, column=0, padx=80, pady=5, sticky="ew")

        # Resultado
        self.resultado_label = ctk.CTkLabel(self, text="", font=("Arial", 14), justify="center")
        self.resultado_label.grid(row=5, column=0, padx=20, pady=10, sticky="n")

        # Botões
        self.botao_simular = ctk.CTkButton(self, text="Simular", command=self.simular, height=38)
        self.botao_simular.grid(row=6, column=0, padx=100, pady=(10, 5), sticky="ew")

        self.botao_voltar = ctk.CTkButton(self, text="Voltar", command=lambda: self.controller.mostrar_frame("Home"))
        self.botao_voltar.grid(row=7, column=0, padx=100, pady=(5, 20), sticky="ew")

    def simular(self):
        try:
            ticker = self.ticker_box.get()
            modelo_nome = self.modelo_box.get()
            periodo = int(self.periodo_box.get())
            valor = float(self.valor_entry.get())
        except Exception:
            self.resultado_label.configure(text="⚠️ Preencha os campos corretamente.", text_color="orange")
            return

        treinador_cls = TreinadorML if modelo_nome == "LSTM" else TreinadorProphet
        ativo = Ativo(treinador_cls=treinador_cls, ticker=ticker)
        try:
            ativo.carregar_dados()
            ativo.preparar_dados()
            ativo.treinar()
            df = ativo.prever()
        except Exception as e:
            self.resultado_label.configure(text=f"Erro ao processar ativo:\n{e}", text_color="red")
            return

        df_validos = df[df['Close'].notna()]
        df_futuros = df[df['Close'].isna()]

        if len(df_futuros) < periodo:
            self.resultado_label.configure(
                text=f"❌ Previsão insuficiente para {periodo} dias úteis.",
                text_color="red"
            )
            return

        preco_hoje = df_validos["Close"].iloc[-1]
        preco_futuro = df_futuros["predicoes"].iloc[periodo - 1]

        retorno = (preco_futuro - preco_hoje) / preco_hoje
        resultado = valor * (1 + retorno)

        self.resultado_label.configure(
            text=f"📆 Período: {periodo} dias úteis\n💰 Retorno: {retorno:.2%}\nValor final: R${resultado:.2f}",
            text_color="lightgreen" if retorno >= 0 else "red"
        )
