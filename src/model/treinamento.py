# src/model/treinamento.py
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input

def criar_modelo(input_shape):
    modelo = Sequential([
        Input(shape=input_shape),
        LSTM(50, return_sequences=True),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])
    modelo.compile(optimizer='adam', loss='mean_squared_error')
    return modelo

def treinar_modelo(modelo, treino_x, treino_y, batch_size, epochs):
    modelo.fit(treino_x, treino_y, batch_size=batch_size, epochs=epochs)
    return modelo
