# src/data/preprocess.py
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preparar_dados(dados, janela):
    cotacao = dados['Close'].to_numpy().reshape(-1,1)
    tamanho_treino = int(len(cotacao)*0.8)
    
    scaler = MinMaxScaler(feature_range=(0,1))
    dados_treino = scaler.fit_transform(cotacao[:tamanho_treino])
    dados_teste = scaler.transform(cotacao[tamanho_treino:])
    
    dados_esc = np.concatenate((dados_treino, dados_teste), axis=0)

    # Construção das janelas para treino
    treino_x, treino_y = [], []
    for i in range(janela, tamanho_treino):
        treino_x.append(dados_esc[i - janela:i, 0])
        treino_y.append(dados_esc[i, 0])
    treino_x = np.array(treino_x).reshape(-1, janela, 1)
    treino_y = np.array(treino_y)

    # Construção das janelas para teste
    dados_teste_janela = dados_esc[tamanho_treino - janela:]
    teste_x = []
    for i in range(janela, len(dados_teste_janela)):
        teste_x.append(dados_teste_janela[i - janela:i, 0])
    teste_x = np.array(teste_x).reshape(-1, janela, 1)
    teste_y = cotacao[tamanho_treino:]
    
    return scaler, cotacao, treino_x, treino_y, teste_x, teste_y, tamanho_treino
