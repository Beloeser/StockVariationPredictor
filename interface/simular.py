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

        # Datas
        data_compra_padrao = "2015-06-17"
        data_venda_padrao = "2025-06-17"

        self.data_entrada = ctk.CTkEntry(self, placeholder_text="Data de Compra (YYYY-MM-DD)", state="readonly")
        self.data_entrada.insert(0, data_compra_padrao)
        self.data_entrada.grid(row=3, column=0, padx=80, pady=5, sticky="ew")

        self.data_saida = ctk.CTkEntry(self, placeholder_text="Data de Venda (YYYY-MM-DD)", state="readonly")
        self.data_saida.insert(0, data_venda_padrao)
        self.data_saida.grid(row=4, column=0, padx=80, pady=5, sticky="ew")

        # Valor investido
        self.valor_entry = ctk.CTkEntry(self, placeholder_text="Valor investido (R$)")
        self.valor_entry.grid(row=5, column=0, padx=80, pady=5, sticky="ew")

        # Resultado
        self.resultado_label = ctk.CTkLabel(self, text="", font=("Arial", 14), justify="center")
        self.resultado_label.grid(row=6, column=0, padx=20, pady=10, sticky="n")

        # Botões
        self.botao_simular = ctk.CTkButton(self, text="Simular", command=self.simular, height=38)
        self.botao_simular.grid(row=7, column=0, padx=100, pady=(10, 5), sticky="ew")

        self.botao_voltar = ctk.CTkButton(self, text="Voltar", command=lambda: self.controller.mostrar_frame("Home"))
        self.botao_voltar.grid(row=8, column=0, padx=100, pady=(5, 20), sticky="ew")

    def simular(self):
        ticker = self.ticker_box.get()
        modelo_nome = self.modelo_box.get()
        data_ini = self.data_entrada.get()
        data_fim = self.data_saida.get()
        valor = float(self.valor_entry.get())

        treinador_cls = TreinadorML if modelo_nome == "LSTM" else TreinadorProphet
        ativo = Ativo(treinador_cls=treinador_cls, ticker=ticker)
        ativo.carregar_dados()
        ativo.preparar_dados()
        ativo.treinar()
        df = ativo.prever()

        try:
            preco_ini = df.loc[pd.to_datetime(data_ini)]["predicoes"]
            preco_fim = df.loc[pd.to_datetime(data_fim)]["predicoes"]
        except KeyError:
            self.resultado_label.configure(text="❌ Datas inválidas ou fora do intervalo.", text_color="red")
            return

        retorno = (preco_fim - preco_ini) / preco_ini
        resultado = valor * (1 + retorno)
        self.resultado_label.configure(
            text=f"💰 Retorno: {retorno:.2%}\nValor final: R${resultado:.2f}",
            text_color="lightgreen" if retorno >= 0 else "red"
        )
