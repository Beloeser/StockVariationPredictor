from src.data.downloader import BancoDadosDownloader


def main():
    instituicoes = [
        "ABC BRASIL", "ALFA HOLDING", "ALFA INVEST", "AMAZONIA", "BANCO BMG", "BANCO PAN", "BANESE",
        "BANESTES", "BANPARA", "BANRISUL", "BR PARTNERS", "BRADESCO", "BRASIL", "BRB BANCO",
        "BTGP BANCO", "INTER CO", "ITAUSA", "ITAUUNIBANCO", "MERC BRASIL", "MERC INVEST", "MODALMAIS",
        "NORD BRASIL", "NU-NUBANK", "PINE", "SANTANDER BR", "BCO SOFISA S.A.", "BRB BCO DE BRASILIA S.A."
    ]

    downloader = BancoDadosDownloader(ano=2022, instituicoes=instituicoes, arquivo_saida="valores_bancos_2022.csv")
    downloader.baixar_e_processar()

if __name__ == "__main__":
    main()
#teste tambem
