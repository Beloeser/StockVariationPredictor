# %%
import math
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
from datetime import timedelta
from keras.layers import Input
pd.options.mode.chained_assignment = None

# %%
acao = "WEGE3.SA" #encontrar o jeito de pegar direto dos dados e modularizar o baguio

inicio = "2014-12-31"
final = "2022-09-15"

dados_acao = yf.download(acao, start=inicio, end=final)

print(dados_acao.head())

# %%
cotacao = dados_acao['Close'].to_numpy().reshape(-1,1)


cotacao

# %%
tamanho_dados_treinamento = int(len(cotacao)*0.8)

tamanho_dados_treinamento

# %%
escalador = MinMaxScaler(feature_range=(0,1))

dados_entre_0_e_1_treinamento = escalador.fit_transform(cotacao[0: tamanho_dados_treinamento , :])

dados_entre_0_e_1_teste = escalador.transform(cotacao[tamanho_dados_treinamento : , :])

dados_entre_0_e_1 = list(dados_entre_0_e_1_treinamento.reshape(
    len(dados_entre_0_e_1_treinamento))) + list(dados_entre_0_e_1_teste.reshape(len(dados_entre_0_e_1_teste)))


dados_entre_0_e_1 = np.array(dados_entre_0_e_1).reshape(len(dados_entre_0_e_1) , 1)

dados_entre_0_e_1



# %%
dados_para_treinamento = dados_entre_0_e_1[0:tamanho_dados_treinamento, :]

treinamento_x = []
treinamento_y = []

for i in range(60, len(dados_para_treinamento)):

    treinamento_x.append(dados_para_treinamento[i - 60:i, 0])
    
    treinamento_y.append(dados_para_treinamento[i, 0])

    if i <= 61:
        print(treinamento_x)
        print(treinamento_y)



# %%
#passando as listas para array e dando reshape para 3 dimensoes porque o modelo funciona assim
treinamento_x , treinamento_y = np.array(treinamento_x) , np.array(treinamento_y)

print(treinamento_x)

treinamento_x = treinamento_x.reshape(treinamento_x.shape[0], treinamento_x.shape[1], 1)

print(treinamento_x)

# %%

modelo = Sequential()

modelo.add(Input(shape=(treinamento_x.shape[1], 1)))
modelo.add(LSTM(50, return_sequences=True))

modelo.add(LSTM(50, return_sequences=False))

modelo.add(Dense(25))

modelo.add(Dense(1))


print("Número de passos de tempo usados como entrada (treinamento_x.shape[1]):", treinamento_x.shape[1])


# %%

modelo.compile(optimizer= "adam" , loss = "mean_squared_error")

# %%
modelo.fit(treinamento_x , treinamento_y , batch_size=10, epochs= 1)


# %%
dados_teste = dados_entre_0_e_1[tamanho_dados_treinamento - 60: , :]

teste_x = []
teste_y = cotacao[tamanho_dados_treinamento: ,  :]

for i in range(60 , len(dados_teste)):
    teste_x.append(dados_teste[i-60 : i , 0])

# %%

teste_x = np.array(teste_x)
teste_x = teste_x.reshape(teste_x.shape[0], teste_x.shape[1] , 1)

# %%
predicoes = modelo.predict(teste_x)

predicoes = escalador.inverse_transform(predicoes)



predicoes

# %%
#pegando o erro medio quadratico 

rmse = np.sqrt(np.mean(predicoes - teste_y)**2)

rmse

# %%
# Garanta que close_test é 1D
close_test = dados_acao['Close'].iloc[tamanho_dados_treinamento:].values
if close_test.ndim > 1:
    close_test = close_test.flatten()

# Garanta que predicoes_1d é 1D
predicoes_1d = predicoes
if predicoes.ndim > 1:
    predicoes_1d = predicoes.reshape(-1)

# Verifique shapes e tipos
print("close_test shape:", close_test.shape)
print("predicoes_1d shape:", predicoes_1d.shape)
print("close_test ndim:", close_test.ndim)
print("predicoes_1d ndim:", predicoes_1d.ndim)

# Ajuste para o menor tamanho para evitar erro de alinhamento
min_len = min(len(close_test), len(predicoes_1d))

index_test = dados_acao.index[tamanho_dados_treinamento:tamanho_dados_treinamento + min_len]

# Agora crie o DataFrame
df_teste = pd.DataFrame({
    "Close": close_test[:min_len],
    "predicoes": predicoes_1d[:min_len]
}, index=index_test)



# %%

#grafico 
plt.figure(figsize=(16, 8))
plt.title('Modelo')
plt.xlabel('Data', fontsize=18)
plt.ylabel("Preço de fechamento", fontsize=18)

plt.plot(treinamento.index, treinamento['Close'], label='Treinamento')
plt.plot(df_teste.index, df_teste['Close'], label='Real')
plt.plot(df_teste.index, df_teste['predicoes'], label='Previsões')

plt.legend(loc=2, prop={'size': 16})
plt.show()

# %%
df_teste.sort_index()

df_teste

# %%
# Cálculo de variações
df_teste['variacao_percentual_acao'] = df_teste['Close'].pct_change()
df_teste['variacao_percentual_modelo'] = df_teste['predicoes'].pct_change()
df_teste = df_teste.dropna()

# Comparação de direção
df_teste['var_acao_maior_que_zero'] = df_teste['variacao_percentual_acao'] > 0
df_teste['var_modelo_maior_menor_que_zero'] = df_teste['variacao_percentual_modelo'] > 0
df_teste['acertou_o_lado'] = df_teste['var_acao_maior_que_zero'] == df_teste['var_modelo_maior_menor_que_zero']
df_teste['variacao_percentual_acao_abs'] = df_teste['variacao_percentual_acao'].abs()

# %%
# Estatísticas
acertou_lado = df_teste['acertou_o_lado'].mean()
errou_lado = 1 - acertou_lado
media_lucro = df_teste.groupby('acertou_o_lado')['variacao_percentual_acao_abs'].mean()
lucro_acerto = media_lucro.get(True, 0)
lucro_erro = media_lucro.get(False, 0)
exp_mat_lucro = acertou_lado * lucro_acerto - errou_lado * lucro_erro
ganho_sobre_perda = lucro_acerto / lucro_erro if lucro_erro != 0 else float('inf')

#estatisticas
print("Média de lucro (acertou=False, acertou=True):")
print(media_lucro)
print(f"\nGanho sobre perda: {ganho_sobre_perda:.2f}")
print(f"Taxa de acerto: {acertou_lado:.2%}")
print(f"Expectativa matemática de lucro: {exp_mat_lucro:.4f}")

#comentario soh para testar o pull request