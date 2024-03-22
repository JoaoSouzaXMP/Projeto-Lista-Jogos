from main import app
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,InputRequired,Regexp
import os

''' FORMULARIOS '''
# Validação Inputs Jogos
VALIDACAO_JOGO = [DataRequired(),Length(min=2,max=50),InputRequired()]
class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo',validators=VALIDACAO_JOGO)
    categoria = StringField('Categoria',validators=VALIDACAO_JOGO)
    console = StringField('Console',validators=VALIDACAO_JOGO)
    salvar =  SubmitField('Salvar')
# Validação Inputs Usuarios
class FormularioUsuario(FlaskForm):
    nome = StringField('Nome de Usuário',validators=[DataRequired(),Length(min=4,max=50),InputRequired(),Regexp(r'/[\w-]/m')])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(min=4,max=50),InputRequired()])
    login = SubmitField('Login')

''' FUNÇÃO AUXILIARES IMAGENS '''
# Retorna a imagem do jogo baseado no id ou a capa padrão
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'
# Deleta a imagem do jogo baseado no id
def deletar_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))

''' COMANDOS SQL '''
SQL_QUERYS = {}
# Comandos tblJogos
SQL_QUERYS['SelectJogosAll'] = '''SELECT * FROM tblJogos'''
SQL_QUERYS['SelectJogoNome'] = '''SELECT * FROM tblJogos WHERE Nome LIKE ?'''
SQL_QUERYS['SelectJogoId'] = '''SELECT * FROM tblJogos WHERE JogoID=?'''
SQL_QUERYS['InsertJogo'] = '''INSERT INTO tblJogos(Nome,Categoria,Console) VALUES(?,?,?)'''
SQL_QUERYS['UpdateJogo'] = '''UPDATE tblJogos SET Nome=?, Categoria=?, Console=? WHERE JogoID=?'''
SQL_QUERYS['DeleteJogo'] = '''DELETE tblJogos WHERE JogoID=?'''
# Comandos tblUsuarios
SQL_QUERYS['SelectUsuarioNome'] = '''SELECT * FROM tblUsuarios WHERE Nome LIKE ?'''
SQL_QUERYS['InsertUsuario'] = '''INSERT INTO tblUsuarios(Nome,Senha) VALUES(?,?)'''
SQL_QUERYS['UpdateSenhaUsuario'] = '''UPDATE tblUsuarios SET Senha = ? WHERE nome LIKE ?'''
# Comandos tblImagens
SQL_QUERYS['SelectImagem'] = '''SELECT Imagem FROM tblImagens WHERE JogoID = ?'''
SQL_QUERYS['InsertImagem'] = '''INSERT INTO tblImagens VALUES (?,?)'''
SQL_QUERYS['UpdateImagem'] = '''UPDATE tblImagens SET Imagem = ? WHERE JogoID = ?'''
SQL_QUERYS['DeleteImagem'] = '''DELETE tblImagens WHERE JogoID = ?'''