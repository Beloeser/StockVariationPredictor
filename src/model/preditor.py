import numpy as np
import pandas as pd

def prever(modelo, teste_x, teste_y, dados, scaler, split_idx):
    pred = modelo.predict(teste_x)
    pred_rescaled = scaler.inverse_transform(pred).flatten()

    close_test = dados['Close'].iloc[split_idx:].values[:len(pred_rescaled)].flatten()

    min_len = min(len(close_test), len(pred_rescaled))
    close_test = close_test[:min_len]
    pred_rescaled = pred_rescaled[:min_len]

    index_test = dados.index[split_idx:split_idx + min_len]

    df = pd.DataFrame({
        "Close": close_test,
        "predicoes": pred_rescaled
    }, index=index_test)

    return pred_rescaled, df


def prever_futuro(modelo, dados_ultimos, scaler, dias_futuros=120, index_inicial=None):
    janela = dados_ultimos.shape[0]
    previsoes_norm = []
    seq = dados_ultimos.copy()

    for _ in range(dias_futuros):
        x_input = seq.reshape(1, janela, 1)
        pred = modelo.predict(x_input, verbose=0)[0, 0]
        previsoes_norm.append(pred)
        seq = np.append(seq[1:], pred)

    previsoes_norm = np.array(previsoes_norm).reshape(-1, 1)
    previsoes_desnorm = scaler.inverse_transform(previsoes_norm).flatten()

    if index_inicial is None:
        index_inicial = pd.RangeIndex(start=0, stop=len(previsoes_desnorm), step=1)

    df_futuro = pd.DataFrame({
        "previsao_futura": previsoes_desnorm
    }, index=index_inicial)

    return df_futuro
