from src.core.ativo import Ativo
from src.models.Treinadores.treinador_prophet import TreinadorProphet
from src.models.Treinadores.treinadorML import TreinadorML

def main():
    
    ativo = Ativo(treinador_cls=TreinadorML)

    ativo.carregar_dados(usar_cache=True)  
    ativo.preparar_dados()
    ativo.treinar()
    ativo.prever()
    ativo.avaliar()
    ativo.plotar()
    ativo.estatisticas()

if __name__ == "__main__":
    main()