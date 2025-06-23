import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.core.ativo import Ativo
from src.models.Treinadores.treinadorML import TreinadorML
from src.models.Treinadores.treinador_prophet import TreinadorProphet
from src.utils.stats import calcular_estatisticas
from tkinter import messagebox

class TelaComparar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Layout principal
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkLabel(self, text="Comparar Ativos", font=("Arial", 24))
        self.header.grid(row=0, column=0, pady=(20, 10), padx=20)

        # Frame com seletores de ativos e modelos
        self.frame_scroll = ctk.CTkScrollableFrame(self, height=200)
        self.frame_scroll.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_scroll.grid_columnconfigure((0, 1, 2), weight=1)

        self.linhas_widgets = []
        self.adicionar_ativo()
        self.adicionar_ativo()

        # Botões de ação
        self.botoes = ctk.CTkFrame(self)
        self.botoes.grid(row=2, column=0, pady=10)

        self.botao_adicionar = ctk.CTkButton(self.botoes, text="+ Adicionar Ativo", command=self.adicionar_ativo, width=160)
        self.botao_adicionar.grid(row=0, column=0, padx=10)

        self.botao_comparar = ctk.CTkButton(self.botoes, text="Comparar", command=self.comparar_ativos, width=140)
        self.botao_comparar.grid(row=0, column=1, padx=10)

        self.botao_voltar = ctk.CTkButton(self.botoes, text="Voltar", command=lambda: self.controller.mostrar_frame("Home"), width=140)
        self.botao_voltar.grid(row=0, column=2, padx=10)

        # Frame para o gráfico
        self.frame_grafico = ctk.CTkFrame(self, height=300)
        self.frame_grafico.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.frame_grafico.grid_rowconfigure(0, weight=1)
        self.frame_grafico.grid_columnconfigure(0, weight=1)
        self.frame_grafico.grid_propagate(False)

        self.canvas = None

        self.frame_tabela = ctk.CTkScrollableFrame(self, height=250)
        self.frame_tabela.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.frame_tabela.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.linhas_tabela = []  # Guarda widgets para destruir depois



    def adicionar_ativo(self):
        row = len(self.linhas_widgets)

        seletor_ticker = ctk.CTkOptionMenu(self.frame_scroll, values=Ativo.TICKERS_VALIDOS)
        seletor_ticker.grid(row=row, column=0, padx=10, pady=5, sticky="ew")

        seletor_modelo = ctk.CTkOptionMenu(self.frame_scroll, values=["LSTM", "Prophet"])
        seletor_modelo.grid(row=row, column=1, padx=10, pady=5, sticky="ew")

        botao_remover = ctk.CTkButton(self.frame_scroll, text="–", width=40, command=lambda: self.remover_ativo(row))
        botao_remover.grid(row=row, column=2, padx=5)

        self.linhas_widgets.append((seletor_ticker, seletor_modelo, botao_remover))

    def remover_ativo(self, row_index):
        # Remove widgets da linha
        for widget in self.linhas_widgets[row_index]:
            widget.grid_forget()
            widget.destroy()

        del self.linhas_widgets[row_index]

        # Reorganiza visualmente os elementos restantes
        for new_index, (ticker, modelo, remover) in enumerate(self.linhas_widgets):
            ticker.grid(row=new_index, column=0, padx=10, pady=5, sticky="ew")
            modelo.grid(row=new_index, column=1, padx=10, pady=5, sticky="ew")
            remover.configure(command=lambda idx=new_index: self.remover_ativo(idx))
            remover.grid(row=new_index, column=2, padx=5)

    def comparar_ativos(self):
        fig = Figure(figsize=(10, 5), dpi=100, facecolor="#2b2b2b")
        ax = fig.add_subplot(111, facecolor="#2b2b2b")
        ax.tick_params(colors='white')           
        ax.xaxis.label.set_color('white')       
        ax.yaxis.label.set_color('white')  
        ax.title.set_color('white')  
        ax.grid(True, color='gray', linestyle='--', alpha=0.3)


        for seletor_ticker, seletor_modelo, _ in self.linhas_widgets:
            ticker = seletor_ticker.get()
            modelo_nome = seletor_modelo.get()

            if not ticker:
                continue

            treinador_cls = TreinadorML if modelo_nome == "LSTM" else TreinadorProphet

            try:
                ativo = Ativo(treinador_cls=treinador_cls, ticker=ticker)
                ativo.carregar_dados()
                ativo.preparar_dados()
                ativo.treinar()
                df_pred = ativo.prever()

                ax.plot(df_pred.index, df_pred["Close"], label=f"{ticker} - Real", linestyle="--")
                ax.plot(df_pred.index, df_pred["predicoes"], label=f"{ticker} - {modelo_nome}")
            except Exception as e:
                print(f"Erro ao processar {ticker}: {e}")

        ax.set_title("Comparação de Preços - Reais vs Previstos")
        ax.set_xlabel("Data")
        ax.set_ylabel("Preço de Fechamento")
        ax.legend()
        ax.grid(True)

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Limpa tabela anterior
        for linha in self.linhas_tabela:
            for widget in linha:
                widget.destroy()
        self.linhas_tabela.clear()

        # Cabeçalho
        cabecalho = ["Ticker", "Modelo", "Dias", "Acerto (%)", "Lucro Esperado", "G/P"]
        for i, texto in enumerate(cabecalho):
            label = ctk.CTkLabel(self.frame_tabela, text=texto, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5)
        self.linhas_tabela.append([label])

        # Métricas por ativo
        linha_atual = 1
        dias_avaliar = [1, 7, 30]

        for seletor_ticker, seletor_modelo, _ in self.linhas_widgets:
            ticker = seletor_ticker.get()
            modelo_nome = seletor_modelo.get()

            if not ticker:
                continue

            treinador_cls = TreinadorML if modelo_nome == "LSTM" else TreinadorProphet
            ativo = Ativo(treinador_cls=treinador_cls, ticker=ticker)
            try:
                ativo.carregar_dados()
            except Exception as e:
                messagebox.showwarning("Erro ao baixar dados", f"Ticker '{ticker}' não pôde ser carregado.\n{str(e)}")
                continue
            ativo.preparar_dados()
            ativo.treinar()
            df_pred = ativo.prever()

            for dias in dias_avaliar:
                est = calcular_estatisticas(df_pred, dias)

                valores = [
                    ticker,
                    modelo_nome,
                    str(dias),
                    f"{est['taxa_acerto'] * 100:.1f}",
                    f"{est['exp_mat_lucro']:.4f}",
                    f"{est['ganho_sobre_perda']:.2f}",
                ]

                widgets_linha = []
                for j, val in enumerate(valores):
                    cell = ctk.CTkLabel(self.frame_tabela, text=val, font=("Arial", 11))
                    cell.grid(row=linha_atual, column=j, padx=5, pady=2)
                    widgets_linha.append(cell)

                self.linhas_tabela.append(widgets_linha)
                linha_atual += 1