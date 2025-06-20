import json
import bcrypt

class GerenciaUsuarios:
    def __init__(self, arquivo_usuarios='usuarios.json'):
        self.arquivo_usuarios = arquivo_usuarios

    def _carregar_usuarios(self):
        try:
            with open(self.arquivo_usuarios, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"usuarios": []}
        
    def salvar_dados(self, dados):
        with open(self.arquivo_usuarios, 'w') as f:
            json.dump(dados, f, indent=2)
        
    def cadastrar_usuario(self, nome, senha):
        if not nome or not senha:
            return False
        
        dados = self._carregar_usuarios()
        if any(u['nome'] == nome for u in dados['usuarios']):
            print(f"Usuário '{nome}' já existe.")
            return False
        
        encoded_senha = senha.encode('utf-8')
        senha_hash = bcrypt.hashpw(encoded_senha, bcrypt.gensalt())

        #Criando o novo usuario
        novo_usuario = {
            "nome": nome,
            "senha": senha_hash.decode('utf-8')
        }
        
        dados['usuarios'].append(novo_usuario)
        self.salvar_dados(dados)
        print(f"Usuário '{nome}' cadastrado com sucesso.")
        return True
    
    def checar_senha(self, nome, senha):
        dados = self._carregar_usuarios()
        dados_usuarios = next((u for u in dados['usuarios'] if u['nome'] == nome), None)

        if dados_usuarios:
            senha_hash = dados_usuarios['senha'].encode('utf-8')
            encoded_senha = senha.encode('utf-8')

            if bcrypt.checkpw(encoded_senha, senha_hash):
                print(f"Senha correta para o usuário '{nome}'.")
                return True
        
        print(f"Senha incorreta para o usuário '{nome}'.")
        return False
    
    