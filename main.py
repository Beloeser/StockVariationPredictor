from src.core.ativo import Ativo
import config

def main():
    acao = Ativo(
        ticker=config.TICKER,
        data_inicio=config.DATA_INICIO,
        data_fim=config.DATA_FIM,
        janela=config.JANELA,
        batch_size=config.BATCH_SIZE,
        epochs=config.EPOCHS
    )

    acao.carregar_dados()
    acao.preparar_dados()
    acao.treinar()
    acao.prever()
    acao.avaliar()
    acao.plotar()
    acao.estatisticas()


if __name__ == "__main__":
    main()
