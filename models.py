from config import CURSOR
from helpers import SQL_QUERYS
import base64

class Jogo:
    def __init__(self,nome,categoria,console):
        self._nome = nome
        self._categoria = categoria
        self._console = console
    def __repr__(self):
        return f"'{self._nome}','{self._categoria}','{self._console}'"
    @classmethod
    def exibir(cls):
        return CURSOR.execute(SQL_QUERYS['SelectJogosAll']).fetchall()
    def consultarnome(self):
        return CURSOR.execute(SQL_QUERYS['SelectJogoNome'],self._nome).fetchone()
    def consultarid(id):
        return CURSOR.execute(SQL_QUERYS['SelectJogoId'],id).fetchone()
    def adicionar(self):
        CURSOR.execute(SQL_QUERYS['InsertJogo'],self._nome,self._categoria,self._console)
    def atualizar(id,nome,categoria,console):
        CURSOR.execute(SQL_QUERYS['UpdateJogo'],nome,categoria,console,id)
    def deletar(id):
        CURSOR.execute(SQL_QUERYS['DeleteJogo'],id)

class Usuario:
    def __init__(self,nome,senha):
        self._nome = nome
        self._senha = senha
    def __repr__(self):
        return f"'{self._nome}','{self._senha}'"
    def consultarnome(self):
        return CURSOR.execute(SQL_QUERYS['SelectUsuarioNome'],self._nome).fetchone()
    def adicionar(self):
        CURSOR.execute(SQL_QUERYS['InsertUsuario'],self._nome,self._senha)
    def redefinirsenha(self):
        CURSOR.execute(SQL_QUERYS['UpdateSenhaUsuario'],self._senha,self._nome)

class Imagem:
    def recuperar_imagem(id):
        img_data = CURSOR.execute(SQL_QUERYS['SelectImagem'],id).fetchone()
        if img_data:
            img_base64 = base64.b64encode(img_data[0]).decode('utf-8')
            return img_base64
        return False
    def salvar_imagem(id,arquivo):
        img_bytes = arquivo.read()
        arquivo.seek(0)
        CURSOR.execute(SQL_QUERYS['InsertImagem'],id,img_bytes)
    def editar_imagem(id,arquivo):
        row = CURSOR.execute(SQL_QUERYS['SelectImagem'],id).fetchone()
        if row:
            img_bytes = arquivo.read()
            arquivo.seek(0)
            CURSOR.execute(SQL_QUERYS['UpdateImagem'],img_bytes,id)
        else:
            Imagem.salvar_imagem(id,arquivo)
