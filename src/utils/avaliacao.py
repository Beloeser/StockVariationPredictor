import numpy as np
import pandas as pd

def avaliar_previsoes(df_teste):
    df = df_teste.copy()
    df['variacao_percentual_acao'] = df['Close'].pct_change()
    df['variacao_percentual_modelo'] = df['predicoes'].pct_change()
    df = df.dropna()

    df['var_acao_maior_que_zero'] = df['variacao_percentual_acao'] > 0
    df['var_modelo_maior_que_zero'] = df['variacao_percentual_modelo'] > 0
    df['acertou_o_lado'] = df['var_acao_maior_que_zero'] == df['var_modelo_maior_que_zero']
    df['variacao_percentual_acao_abs'] = df['variacao_percentual_acao'].abs()

    return df
