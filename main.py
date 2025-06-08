from src.data.downloader import BancoDadosDownloader

def main():
    instituicoes = [
        "ABC BRASIL", "ALFA HOLDING", "ALFA INVEST", "AMAZONIA", "BANCO BMG", "BANCO PAN", "BANESE",
        "BANESTES", "BANPARA", "BANRISUL", "BR PARTNERS", "BRADESCO", "BRASIL", "BRB BANCO",
        "BTGP BANCO", "INTER CO", "ITAUSA", "ITAUUNIBANCO", "MERC BRASIL", "MERC INVEST", "MODALMAIS",
        "NORD BRASIL", "NU-NUBANK", "PINE", "SANTANDER BR", "BCO SOFISA S.A.", "BRB BCO DE BRASILIA S.A."
    ]

    pasta_saida = "db/raw"  # Pasta para salvar os arquivos

    for ano in range(2020, 2026):
        downloader = BancoDadosDownloader(ano=ano, instituicoes=instituicoes, pasta_saida=pasta_saida)
        downloader.baixar_e_processar()

if __name__ == "__main__":
    main()
