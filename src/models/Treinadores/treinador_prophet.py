import pandas as pd
from prophet import Prophet
from .treinador import Treinador

class TreinadorProphet(Treinador):
    def __init__(self, ticker, data_inicio, data_fim, janela=None, batch_size=None, epochs=None):
        self.ticker = ticker
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.janela = janela
        self.batch_size = batch_size
        self.epochs = epochs

        self.dados = None
        self.modelo = None
        self.predicoes_df = None
        self.df_prophet = None

    def carregar_dados(self):
        import yfinance as yf
        self.dados = yf.download(self.ticker, start=self.data_inicio, end=self.data_fim)
        return self.dados

    def preparar_dados(self, dados, janela=None):
        df_temp = dados.copy()

        if isinstance(df_temp.columns, pd.MultiIndex):
            df_temp.columns = df_temp.columns.get_level_values(0)

        df_temp = df_temp.reset_index()

        if 'Date' in df_temp.columns:
            df_temp = df_temp.rename(columns={'Date': 'ds'})
        elif 'ds' not in df_temp.columns:
            raise ValueError("Coluna de data não encontrada.")

        if 'Close' not in df_temp.columns:
            raise ValueError("Coluna 'Close' não encontrada.")

        df_temp = df_temp.rename(columns={'Close': 'y'})
        df_temp['y'] = pd.to_numeric(df_temp['y'], errors='coerce')
        df_temp = df_temp.dropna(subset=['y'])

        self.df_prophet = df_temp[['ds', 'y']]

    def criar_modelo(self):
        self.modelo = Prophet()

    def treinar_modelo(self):
        self.modelo.fit(self.df_prophet)

    def prever(self):
        datas_futuras = self.modelo.make_future_dataframe(periods=30, freq='B')
        forecast = self.modelo.predict(datas_futuras)
        predicoes = forecast.set_index('ds')['yhat']

        if isinstance(self.dados.columns, pd.MultiIndex):
            self.dados.columns = self.dados.columns.get_level_values(0)

        df_pred = pd.DataFrame({
            "Close": self.dados['Close'],
            "predicoes": predicoes
        })

        df_pred = df_pred.combine_first(predicoes.to_frame(name="predicoes"))
        df_pred = df_pred.dropna(subset=["predicoes"])
        self.predicoes_df = df_pred

        return self.predicoes_df
