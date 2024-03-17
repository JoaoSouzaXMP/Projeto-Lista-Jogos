from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
import os

# Usado para limpar o terminal ao reiniciar
os.system('cls')

# Define as Configurações do site
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Proteção Contra Cross-Site Request Forgery
csrf = CSRFProtect(app)
# Proteção Criptografar Senhas com Hash 
bcrypt = Bcrypt(app)

''' CONTEÚDO SITE '''
from views_game import *
from views_user import *

# Inicializor do Site
if __name__ == '__main__':
    #app.run(ssl_context="adhoc", host='0.0.0.0', port=25565, debug=True)
    app.run(host='0.0.0.0', port=25565, debug=True)