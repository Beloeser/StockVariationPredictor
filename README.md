# Stock Variation Predictor

**Stock Variation Predictor** is a GUI-based application for forecasting stock prices. It uses machine learning models (LSTM with Keras/TensorFlow and Prophet) to predict trends for both Brazilian and international stock tickers. The tool allows users to train models, simulate investments, compare model performance, and visualize predictions in an intuitive interface built with `CustomTkinter`.

## Features

- Forecasting using LSTM (deep learning) and Prophet (time series) models
- Investment simulation for selected tickers and timeframes
- Side-by-side comparison of predictions for different models and stocks
- Graphical visualization of actual vs predicted prices
- User login and registration with password encryption
- Statistical analysis including accuracy, expected return, and gain/loss ratio

## Python Version Requirement

This project requires **Python 3.8 to 3.10**.

> TensorFlow is not fully compatible with Python 3.11+ in many environments. Using Python 3.8, 3.9, or 3.10 is strongly recommended to avoid installation issues.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-user/stock-variation-predictor.git
cd stock-variation-predictor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Requirements

```
numpy
pandas
scikit-learn
matplotlib
seaborn
tensorflow
keras
prophet
yfinance
customtkinter
bcrypt
```

Note: Ensure your system has `tk` support installed for the GUI to function correctly.

## How to Run

Run the application with:

```bash
python main.py
```

This will launch the graphical interface for login, training, simulation, and analysis.

## Project Structure

```
├── main.py
├── app.py
├── interface/
│   ├── entrar.py
│   ├── cadastrar.py
│   ├── home.py
│   ├── comparar.py
│   └── simular.py
├── src/
│   ├── core/
│   ├── data/
│   ├── models/
│   ├── utils/
│   └── avaliacao.py
├── db/
├── requirements.txt
└── README.md
```

## Supported Tickers

The system includes support for various stock tickers (e.g., `ITUB4.SA`, `BBAS3.SA`, `NUBR33.SA`). You can modify the available list in `src/core/ativo.py`.
