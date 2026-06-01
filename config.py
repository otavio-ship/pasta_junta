import fdb

SECRET_KEY = 'chave_secreta_projeto_vendas'

def get_db_connection():
    try:
        conn = fdb.connect(
            host="localhost",
            database=r'C:\Users\Aluno\Desktop\otavio\Back_otavio-main\BANCO.FDB',
            user='SYSDBA',
            password='sysdba',
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar no banco: {e}")
        return None