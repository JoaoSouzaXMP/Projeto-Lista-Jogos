import pyodbc
from flask_bcrypt import generate_password_hash

''' Conecta ao SQLExpress '''
print('Conectando...')
try:
    SERVER = 'REDRAGON-PC\SQLEXPRESS'
    DRIVER = 'ODBC Driver 17 for SQL Server'
    CONNECTIONSTRING = f'DRIVER={DRIVER};SERVER={SERVER};Trusted_Connection=yes;'
    CONN = pyodbc.connect(CONNECTIONSTRING, autocommit = True)
    CURSOR = CONN.cursor()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    if sqlstate == '42000':
        print("Erro de sintaxe SQL.")
    else:
        print(f"Ocorreu um erro: {ex}")
    exit()

''' CRIAR BANCO E TABELAS '''
CURSOR.execute(''' DROP DATABASE IF EXISTS dbAula ''')
CURSOR.execute(''' CREATE DATABASE dbAula ''')
CURSOR.execute(''' USE dbAula ''')
TABELAS = {}
TABELAS['Jogos'] = ('''
    CREATE TABLE tblJogos(
	JogoID INT NOT NULL identity(1,1) primary key,
    Nome VARCHAR(MAX) NOT NULL,
    Categoria VARCHAR(MAX) NOT NULL,
    Console VARCHAR(MAX) NOT NULL,
); ''')
TABELAS['Usuarios'] = ('''
    CREATE TABLE tblUsuarios(
	UsuarioID INT NOT NULL identity(1,1) primary key,
    Nome VARCHAR(MAX) NOT NULL,
    Senha VARCHAR(MAX) NOT NULL,
); ''')
TABELAS['Imagens'] = ('''
    CREATE TABLE tblImagens(
	ImagemID INT NOT NULL identity(1,1) primary key,
	JogoID INT NOT NULL,
	Imagem VARBINARY(MAX) NOT NULL,
);
ALTER TABLE [dbo].[tblImagens] ADD CONSTRAINT [FK_dbo.tblImagens_dbo.tblJogos_JogoID] FOREIGN KEY ([JogoID]) REFERENCES [dbo].[tblJogos] ([JogoID])
''')
for tabela_nome in TABELAS:
    tabela_sql = TABELAS[tabela_nome]
    try:
        print('Criando {}:'.format(tabela_nome))
        CURSOR.execute(tabela_sql)
    except pyodbc.Error as ex:
        sqlstate = ex.args[0] 
        if sqlstate == '42000':
            print("Erro de sintaxe SQL.")
        else:
            print(f"Ocorreu um erro: {ex}")
        exit()

''' COMANDOS SQL'''
SQL_QUERYS = {}
SQL_QUERYS['SEtblJogos'] = '''SELECT * FROM tblJogos'''
SQL_QUERYS['SEtblUsuarios'] = '''SELECT * FROM tblUsuarios'''
SQL_QUERYS['INtblJogos'] = '''INSERT INTO tblJogos(Nome,Categoria,Console) VALUES(?,?,?)'''
SQL_QUERYS['INtblUsuarios'] = '''INSERT INTO tblUsuarios(Nome,Senha) VALUES(?,?)'''

''' POPULAR TABELAS '''
JOGOS = [('Minecraft','Simulação, Aventura','Any'),
         ('Genshin Impact','RPG, Aventura','PC, PS'),
         ('Word of Tanks','Ação','PC'),
         ('Counter-Strike','FPS','PC'),
         ('Elder Ring','RPG, Aventura','PC'),
         ('Valorant','FPS','PC'),
         ('League of Legends','MOBA, RPG','PC'),
         ('GTA5','Ação','PC')]
USUARIOS = [('admin',generate_password_hash('1234').decode('utf-8')),
            ('cicada',generate_password_hash('3301').decode('utf-8'))]
CURSOR.executemany(SQL_QUERYS['INtblJogos'],JOGOS)
CURSOR.executemany(SQL_QUERYS['INtblUsuarios'],USUARIOS)

''' EXIBIR TABELAS '''
print('------------------- USUARIOS: -------------------')
CURSOR.execute(SQL_QUERYS['SEtblUsuarios'])
for usuario in CURSOR.fetchall():
    print(usuario[1])
print('------------------- JOGOS: -------------------')
CURSOR.execute(SQL_QUERYS['SEtblJogos'])
for jogo in CURSOR.fetchall():
    print(jogo[1])

CURSOR.close()
CONN.close()