import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input
from .treinador import Treinador

class TreinadorML(Treinador):
    def __init__(self, ticker, data_inicio, data_fim, janela=60, batch_size=10, epochs=10):
        self.ticker = ticker
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.janela = janela
        self.batch_size = batch_size
        self.epochs = epochs

        self.dados = None
        self.scaler = None

        self.treino_x = None
        self.treino_y = None
        self.teste_x = None
        self.teste_y = None
        self.tamanho_treino = None

        self.modelo = None

    def carregar_dados(self):
        import yfinance as yf
        self.dados = yf.download(self.ticker, start=self.data_inicio, end=self.data_fim)
        return self.dados

    def preparar_dados(self, dados, janela):
        cotacao = dados['Close'].to_numpy().reshape(-1, 1)
        self.tamanho_treino = int(len(cotacao) * 0.8)

        self.scaler = MinMaxScaler(feature_range=(0, 1))
        dados_treino = self.scaler.fit_transform(cotacao[:self.tamanho_treino])
        dados_teste = self.scaler.transform(cotacao[self.tamanho_treino:])
        dados_esc = np.concatenate((dados_treino, dados_teste), axis=0)

        treino_x, treino_y = [], []
        for i in range(janela, self.tamanho_treino):
            treino_x.append(dados_esc[i - janela:i, 0])
            treino_y.append(dados_esc[i, 0])
        self.treino_x = np.array(treino_x).reshape(-1, janela, 1)
        self.treino_y = np.array(treino_y)

        dados_teste_janela = dados_esc[self.tamanho_treino - janela:]
        teste_x = []
        for i in range(janela, len(dados_teste_janela)):
            teste_x.append(dados_teste_janela[i - janela:i, 0])
        self.teste_x = np.array(teste_x).reshape(-1, janela, 1)

        self.teste_y = cotacao[self.tamanho_treino:]

    def criar_modelo(self):
        input_shape = self.treino_x.shape[1:]
        self.modelo = Sequential([
            Input(shape=input_shape),
            LSTM(50, return_sequences=True),
            LSTM(50, return_sequences=False),
            Dense(25),
            Dense(1)
        ])
        self.modelo.compile(optimizer='adam', loss='mean_squared_error')

    def treinar_modelo(self):
        self.modelo.fit(self.treino_x, self.treino_y,
                        batch_size=self.batch_size,
                        epochs=self.epochs)

    def prever(self):
        if self.dados is None:
            raise ValueError("Dados não carregados. Execute carregar_dados() primeiro.")

        pred = self.modelo.predict(self.teste_x)
        pred_rescaled = self.scaler.inverse_transform(pred).flatten()

        close_test = self.dados['Close'].iloc[self.tamanho_treino:].values[:len(pred_rescaled)].flatten()
        min_len = min(len(close_test), len(pred_rescaled))
        close_test = close_test[:min_len]
        pred_rescaled = pred_rescaled[:min_len]
        index_test = self.dados.index[self.tamanho_treino:self.tamanho_treino + min_len]

        df_teste = pd.DataFrame({
            "Close": close_test,
            "predicoes": pred_rescaled
        }, index=index_test)

        num_previsoes_futuras = 30
        ultimos_dados = self.scaler.transform(self.dados['Close'].values[-self.janela:].reshape(-1, 1)).flatten()
        previsao_futura = []
        entrada_atual = ultimos_dados.copy()

        for _ in range(num_previsoes_futuras):
            x_input = entrada_atual[-self.janela:].reshape(1, self.janela, 1)
            pred_futuro = self.modelo.predict(x_input)
            previsao_futura.append(pred_futuro[0, 0])
            entrada_atual = np.append(entrada_atual, pred_futuro[0, 0])

        previsao_futura_rescaled = self.scaler.inverse_transform(np.array(previsao_futura).reshape(-1, 1)).flatten()

        ultima_data = self.dados.index[-1]
        datas_futuras = pd.date_range(start=ultima_data + pd.Timedelta(days=1),
                                     periods=num_previsoes_futuras,
                                     freq='B')

        df_futuro = pd.DataFrame({
            "Close": [np.nan] * num_previsoes_futuras,
            "predicoes": previsao_futura_rescaled
        }, index=datas_futuras)

        df_resultado = pd.concat([df_teste, df_futuro])

        self.predicoes_df = df_resultado
        return self.predicoes_df
