# src/model/preditora.py
import pandas as pd

def prever(modelo, teste_x, teste_y, dados, scaler, split_idx):
    """
    Faz previsões, desscala os valores e cria DataFrame com valores reais e previstos.

    Args:
        modelo: modelo treinado
        teste_x: dados de entrada para teste
        teste_y: valores reais para teste (não usado diretamente aqui, mas pode ser útil)
        dados: DataFrame original com dados da ação (com índice de datas)
        scaler: objeto MinMaxScaler usado para desscalar
        split_idx: índice no DataFrame onde começa a base de teste

    Returns:
        pred_rescaled: array 1D das previsões desscaladas
        df: DataFrame com colunas "Close" (real) e "predicoes" (previsão), indexado pelas datas corretas
    """

    pred = modelo.predict(teste_x)
    pred_rescaled = scaler.inverse_transform(pred).reshape(-1)

    # Seleciona os valores reais correspondentes
    close_test = dados['Close'].iloc[split_idx:].values[:len(pred_rescaled)]

    # Garante que sejam arrays 1D para evitar erros ao criar DataFrame
    if close_test.ndim > 1:
        close_test = close_test.flatten()
    if pred_rescaled.ndim > 1:
        pred_rescaled = pred_rescaled.flatten()

    # Ajusta tamanho para o menor comprimento para evitar descompasso
    min_len = min(len(close_test), len(pred_rescaled))
    close_test = close_test[:min_len]
    pred_rescaled = pred_rescaled[:min_len]

    # Índice para DataFrame com as datas da base de teste
    index_test = dados.index[split_idx:split_idx + min_len]

    df = pd.DataFrame({
        "Close": close_test,
        "predicoes": pred_rescaled
    }, index=index_test)

    return pred_rescaled, df
