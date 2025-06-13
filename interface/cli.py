# interface/cli.py
from config import TICKER, DATA_INICIO, DATA_FIM, EPOCHS, BATCH_SIZE, JANELA
from src.data.downloader import baixar_dados
from src.data.preprocess import preparar_dados
from src.model.treinamento import criar_modelo, treinar_modelo
from src.model.preditor import prever
from src.model.avaliacao import avaliar_previsoes
from src.utils.stats import imprimir_estatisticas
from src.utils.plot import plotar_resultados

def run_pipeline():
    dados = baixar_dados(TICKER, DATA_INICIO, DATA_FIM)
    scaler, cotacao, treino_x, treino_y, teste_x, teste_y, split_idx = preparar_dados(dados, JANELA)
    
    modelo = criar_modelo(treino_x.shape[1:])
    modelo = treinar_modelo(modelo, treino_x, treino_y, BATCH_SIZE, EPOCHS)
    
    predicoes, df_teste = prever(modelo, teste_x, teste_y, dados, scaler, split_idx)
    
    df_teste_avaliado = avaliar_previsoes(df_teste)
    
    imprimir_estatisticas(df_teste_avaliado)
    plotar_resultados(dados, df_teste_avaliado)
