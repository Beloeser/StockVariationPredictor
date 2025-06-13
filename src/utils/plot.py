import matplotlib.pyplot as plt

def plotar_resultados(dados_completos, df_teste):
    split_index = df_teste.index[0]
    dados_treino = dados_completos[dados_completos.index < split_index]

    plt.figure(figsize=(16, 8))
    plt.title('Modelo de Previsão de Ações')
    plt.xlabel('Data', fontsize=18)
    plt.ylabel('Preço de Fechamento', fontsize=18)

    plt.plot(dados_treino.index, dados_treino['Close'], label='Treinamento')
    plt.plot(df_teste.index, df_teste['Close'], label='Real')
    plt.plot(df_teste.index, df_teste['predicoes'], label='Previsões')

    plt.legend(loc=2, prop={'size': 16})
    plt.grid(True)
    plt.tight_layout()
    plt.show()
