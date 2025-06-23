import os
from sklearn.preprocessing import MinMaxScaler
from ..models.avaliacao import avaliar_previsoes
from ..utils.plot import plotar_resultados
from ..utils.stats import calcular_estatisticas

class Ativo:
    TICKERS_VALIDOS = [
        "MODL11.SA", "LPSB3.SA", "BBDC3.SA", "BRIV4.SA",
        "BPAC3.SA", "BEES3.SA", "VIVT3.SA", "ITUB4.SA",
        "ABCB4.SA", "BRIV3.SA", "MODL3.SA", "BMGB4.SA",
        "SANB11.SA", "NUBR33.SA", "BSLI3.SA", "BRSR5.SA",
        "AGRO3.SA", "BBAS3.SA", "ITSA3.SA", "WEGE3.SA"
    ]

    @staticmethod
    def escolher_ticker():
        print("Escolha um ticker dentre os disponíveis:")
        for i, ticker in enumerate(Ativo.TICKERS_VALIDOS, 1):
            print(f"{i}. {ticker}")

        while True:
            escolha = input("Digite o número do ticker desejado: ")
            if escolha.isdigit():
                idx = int(escolha)
                if 1 <= idx <= len(Ativo.TICKERS_VALIDOS):
                    return Ativo.TICKERS_VALIDOS[idx - 1]
            print("Escolha inválida. Tente novamente.")

    def __init__(self, treinador_cls, ticker=None, 
             data_inicio="2015-06-17", data_fim="2025-06-17",
             janela=60, batch_size=10, epochs=1):
    


        if ticker is None:
            ticker = self.escolher_ticker()
        elif ticker not in self.TICKERS_VALIDOS:
            print("Ticker inválido, escolha novamente.")
            ticker = self.escolher_ticker()

        self.ticker = ticker
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.janela = janela
        self.batch_size = batch_size
        self.epochs = epochs

        self.treinador = treinador_cls(ticker, data_inicio, data_fim, janela, batch_size, epochs)

        self.scaler = MinMaxScaler()
        self.dados = None
        self.predicoes_df = None


    #Essa parte ajuda do chat revisar depois
    def carregar_dados(self, usar_cache=True):
        caminho_raw = f"db/raw/{self.ticker}.csv"
        os.makedirs(os.path.dirname(caminho_raw), exist_ok=True)

        if usar_cache and os.path.exists(caminho_raw):
            import pandas as pd
            try:
                self.dados = pd.read_csv(caminho_raw, index_col=0, parse_dates=True)
                self.dados.index = pd.to_datetime(self.dados.index, errors='raise')
                print(f"Carregando dados raw do cache {caminho_raw}")

            except Exception as e:
                print(f"❌ Arquivo de cache corrompido ou em formato incorreto ({e}). Excluindo e baixando novamente...")
                os.remove(caminho_raw)
                return self.carregar_dados(usar_cache=False) 

        else:
            import yfinance as yf
            print(f"Baixando dados do Yahoo para {self.ticker}...")
            self.dados = yf.download(self.ticker, start=self.data_inicio, end=self.data_fim)
            if self.dados.empty:
                raise ValueError(f"Não foi possível baixar dados para o ticker '{self.ticker}'")
            self.dados.to_csv(caminho_raw)
            print(f"✅ Dados raw salvos em {caminho_raw}")

        self.treinador.dados = self.dados
        return self.dados

    def preparar_dados(self): #prepara dado e os aalva no dbprocessed
        self.treinador.preparar_dados(self.dados, self.janela)

        caminho_processed = f"db/processed/{self.ticker}_processed.csv"
        os.makedirs(os.path.dirname(caminho_processed), exist_ok=True)

        if hasattr(self.treinador, 'treino_x'):
            self.treino_x = self.treinador.treino_x
            self.treino_y = self.treinador.treino_y
            self.teste_x = self.treinador.teste_x
            self.teste_y = self.treinador.teste_y
        else:
            self.treino_x = None
            self.treino_y = None
            self.teste_x = None
            self.teste_y = None

        self.dados.to_csv(caminho_processed)
        print(f"✅ Dados processados salvos em {caminho_processed}")

    def treinar(self):
        self.treinador.criar_modelo()
        self.treinador.treinar_modelo()

    def prever(self):
        """Realiza previsões e salva em db/processed/{ticker}_predictions.csv"""
        self.predicoes_df = self.treinador.prever()

        caminho_preds = f"db/processed/{self.ticker}_predictions.csv"
        os.makedirs(os.path.dirname(caminho_preds), exist_ok=True)

        self.predicoes_df.to_csv(caminho_preds)
        print(f"✅ Previsões salvas em {caminho_preds}")

        return self.predicoes_df

    def carregar_previsoes(self):
        """Carrega previsões previamente salvas no arquivo db/processed/{ticker}_predictions.csv"""
        caminho_preds = f"db/processed/{self.ticker}_predictions.csv"
        if os.path.exists(caminho_preds):
            import pandas as pd
            self.predicoes_df = pd.read_csv(caminho_preds, index_col=0, parse_dates=True)
            print(f"✅ Previsões carregadas de {caminho_preds}")
        else:
            raise FileNotFoundError(f"Não foi encontrado arquivo de previsões em {caminho_preds}. Rode o treino primeiro.")

    def avaliar(self):
        return avaliar_previsoes(self.predicoes_df)

    def plotar(self):
        if self.predicoes_df is None:
            raise ValueError("Não existem previsões carregadas ou calculadas para realizar o plot.")
        plotar_resultados(self.dados, self.predicoes_df)

    def estatisticas(self):
        for dias in [1, 7, 30, 60]:
            calcular_estatisticas(self.predicoes_df, dias)
