import pyodbc
import os

''' SEGURANÇA '''
# Prevenção contra manipulação de cookies.
SECRET_KEY = 'alura'

''' CONEXÃO SQL SERVER '''
# Usar mesmo SERVER e DATABASE especificados no arquivo "create_database.py", DRIVER muda conforme a instalação SQL Server.
try:
    SERVER = '.\SQLEXPRESS'
    DRIVER = 'ODBC Driver 17 for SQL Server'
    CONNECTIONSTRING = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=dbListaJogos;Trusted_Connection=yes;'
    CONN = pyodbc.connect(CONNECTIONSTRING, autocommit = True)
    CURSOR = CONN.cursor()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    if sqlstate == '42000':
        print("Erro de sintaxe SQL.")
    else:
        print(f"Ocorreu um erro: {ex}")
    exit()

''' OUTROS '''
# Define o caminho para salvar as imagens na pasta uploads
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'