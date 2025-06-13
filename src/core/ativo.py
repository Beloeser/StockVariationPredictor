import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from ..model.treinamento import criar_modelo, treinar_modelo
from ..model.preditor import prever
from ..model.avaliacao import avaliar_previsoes
from ..utils.plot import plotar_resultados
from ..utils.stats import imprimir_estatisticas
from config import TICKER, DATA_INICIO, DATA_FIM, EPOCHS, BATCH_SIZE, JANELA

class Ativo:
    def __init__(self, ticker=TICKER, data_inicio=DATA_INICIO, data_fim=DATA_FIM,
                 janela=JANELA, batch_size=BATCH_SIZE, epochs=EPOCHS):
        self.ticker = ticker
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.janela = janela
        self.batch_size = batch_size
        self.epochs = epochs

        self.modelo = None
        self.scaler = MinMaxScaler()
        self.dados = None
        self.predicoes_df = None

    def carregar_dados(self):
        self.dados = yf.download(self.ticker, start=self.data_inicio, end=self.data_fim)
        return self.dados

    def preparar_dados(self):
        dados = self.dados[['Close']].values
        dados_escalados = self.scaler.fit_transform(dados)
        x, y = [], []
        for i in range(self.janela, len(dados_escalados)):
            x.append(dados_escalados[i-self.janela:i, 0])
            y.append(dados_escalados[i, 0])
        x, y = np.array(x), np.array(y)
        x = np.reshape(x, (x.shape[0], x.shape[1], 1))
        split = int(len(x) * 0.8)
        self.treino_x, self.teste_x = x[:split], x[split:]
        self.treino_y, self.teste_y = y[:split], y[split:]
        self.split_idx = len(self.dados) - len(self.teste_x)
        return self.treino_x, self.treino_y, self.teste_x, self.teste_y

    def treinar(self):
        self.modelo = criar_modelo(self.treino_x.shape[1:])
        self.modelo = treinar_modelo(self.modelo, self.treino_x, self.treino_y, self.batch_size, self.epochs)

    def prever(self):
        _, self.predicoes_df = prever(self.modelo, self.teste_x, self.teste_y, self.dados, self.scaler, self.split_idx)
        return self.predicoes_df

    def avaliar(self):
        return avaliar_previsoes(self.predicoes_df)

    def plotar(self):
        plotar_resultados(self.dados, self.predicoes_df)


    def estatisticas(self):
        for dias in [1, 7, 30, 60]: # podemos colocar um imput aqui
            imprimir_estatisticas(self.predicoes_df, dias)
