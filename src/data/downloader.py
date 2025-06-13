# src/data/downloader.py
import yfinance as yf

def baixar_dados(ticker, inicio, fim):
    dados = yf.download(ticker, start=inicio, end=fim)
    return dados
