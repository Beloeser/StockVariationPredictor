from abc import ABC, abstractmethod
import pandas as pd

class Treinador(ABC):
    @abstractmethod
    def __init__(self, ticker, data_inicio, data_fim):
        pass

    @abstractmethod
    def carregar_dados(self):
       
        pass

    @abstractmethod
    def preparar_dados(self, dados: pd.DataFrame, janela=None):
        pass

    @abstractmethod
    def criar_modelo(self):
        pass

    @abstractmethod
    def treinar_modelo(self):
        pass

    @abstractmethod
    def prever(self):
        pass
