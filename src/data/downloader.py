import os
import requests
import zipfile
import io
import pandas as pd
from datetime import datetime
import urllib3

class BancoDadosDownloader:
    def __init__(self, ano, instituicoes, pasta_saida):
        self.ano = ano
        self.url = f"https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{ano}.ZIP"
        self.instituicoes = [nome.upper() for nome in instituicoes]
        self.pasta_saida = pasta_saida
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
    def baixar_e_processar(self):
        print(f"Baixando dados para o ano {self.ano}...")
        res = requests.get(self.url, verify=False)

        with zipfile.ZipFile(io.BytesIO(res.content)) as zip_file:
            # Extrai nome do arquivo TXT dentro do ZIP
            nome_arquivo = [name for name in zip_file.namelist() if name.endswith(".TXT")][0]
            with zip_file.open(nome_arquivo) as file:
                linhas = [linha.decode("latin1") for linha in file if linha.startswith(b"01")]

        registros = []
        for linha in linhas:
            cod_bdi = linha[10:12]
            if cod_bdi not in ["02", "96"]:
                continue
            data = datetime.strptime(linha[2:10], "%Y%m%d").date()
            cod_neg = linha[12:24].strip()
            nome_empresa = linha[27:39].strip().upper()
            tipo_mercado = linha[24:27]
            preabe = int(linha[56:69]) / 100
            preult = int(linha[108:121]) / 100

            if any(nome in nome_empresa for nome in self.instituicoes):
                registros.append([data, cod_neg, nome_empresa, tipo_mercado, preabe, preult])

        df = pd.DataFrame(registros, columns=[
            "DATA", "COD_NEGOCIACAO", "NOME_EMPRESA", "TIPO_MERCADO", "PRECO_ABERTURA", "PRECO_FECHAMENTO"
        ])

        if not os.path.exists(self.pasta_saida):
            os.makedirs(self.pasta_saida)

        arquivo_saida = os.path.join(self.pasta_saida, f"acoes_{self.ano}.csv")
        df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")
        print(f"✅ Arquivo salvo como: {arquivo_saida}")
