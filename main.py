import os
import fdb
from flask import Flask
from flask_cors import CORS

# ✅ Cria o app UMA única vez
app = Flask(__name__)

# Configuração de Segurança
app.config['SECRET_KEY'] = 'chave_secreta_projeto_vendas'

# ✅ CORS configurado uma única vez
CORS(app, supports_credentials=True,
     origins=[
         "http://localhost:5173",
         "http://127.0.0.1:5173",
         "http://10.92.3.138:5000",
         "http://10.92.3.138:5173"
     ])

# Configuração de Pastas
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Conexão com banco
def get_db_connection():
    try:
        conn = fdb.connect(
            database=r'C:\Users\Aluno\Desktop\otavio\Back_otavio-main\BANCO.FDB',
            user='SYSDBA',
            password='sysdba',
            charset='UTF8',
            fb_library_name=r'C:\Program Files\Firebird\Firebird_3_0\fbclient.dll'
        )
        print(" CONECTOU COM SUCESSO AO FIREBIRD")
        return conn
    except Exception as e:
        print(" ERRO AO CONECTAR NO BANCO:")
        print(e)
        return None

# ✅ Importa as rotas por último

from view import *

if __name__ == '__main__':
    print("Servidor rodando...")
    app.run(host='0.0.0.0', port=5000, debug=True)