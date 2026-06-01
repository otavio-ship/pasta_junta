import datetime
import os
import re
import threading
import random
import jwt
from flask import jsonify, request
from main import app, get_db_connection
from funcao import (
    criptografar,
    checar_senha,
    enviando_email,
    verificar_senha,
    gerar_codigo
)
UPLOAD_FOLDER = os.path.join("uploads", "usuarios")  # caminho direto
# Configuração de Pasta de Upload
UPLOAD_FOLDER = os.path.join(app.config['UPLOAD_FOLDER'], "usuarios")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def validar_conexao(con):
    if con is None:
        return False
    return True


# ---------------------------------------------------------
# 1. CRIAR USUÁRIO (Com código de 6 dígitos)
# ---------------------------------------------------------
@app.route('/criar_usuario', methods=['POST'])
def criar_usuario():

    con = get_db_connection()
    cur = con.cursor()

    try:

        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # PERFIL
        tipo_nome = request.form.get('tipo', 'garcom').lower()

        foto = request.files.get('foto')

        # VALIDAR CAMPOS
        if not nome or not email or not senha:
            return jsonify({
                'erro': 'Nome, Email e Senha são obrigatórios.'
            }), 400

        # VALIDAR SENHA
        erro_senha = verificar_senha(senha)

        if erro_senha:
            return jsonify({
                'erro': erro_senha
            }), 400

        # VALIDAR TIPO
        if tipo_nome == 'admin':
            id_tipo = 1

        elif tipo_nome == 'garcom':
            id_tipo = 2

        else:
            return jsonify({
                'erro': 'Tipo inválido. Use admin ou garcom.'
            }), 400

        # VERIFICAR EMAIL
        cur.execute("""
            SELECT ID_USUARIO
            FROM USUARIO
            WHERE EMAIL = ?
        """, (email,))

        if cur.fetchone():
            return jsonify({
                'erro': 'E-mail já cadastrado.'
            }), 409

        # CRIPTOGRAFAR SENHA
        senha_hash = criptografar(senha)

        # GERAR CÓDIGO
        codigo_confirmacao = gerar_codigo()

        # INSERIR USUÁRIO
        cur.execute("""
            INSERT INTO USUARIO (
                NOME,
                EMAIL,
                SENHA,
                ID_TIPO,
                TIPO_NOME,
                CONTA_CONFIRMADA,
                BLOQUEADO,
                TENTATIVAS_LOGIN,
                ATIVO
            )
            VALUES (?, ?, ?, ?, ?, FALSE, FALSE, 0, TRUE)
            RETURNING ID_USUARIO
        """, (
            nome,
            email,
            senha_hash,
            id_tipo,
            tipo_nome
        ))

        id_usuario = cur.fetchone()[0]

        # SALVAR FOTO
        if foto:
            caminho_foto = os.path.join(
                UPLOAD_FOLDER,
                f"perfil_{id_usuario}.jpg"
            )

            foto.save(caminho_foto)

        # SALVAR CÓDIGO DE CONFIRMAÇÃO
        cur.execute("""
            INSERT INTO CONFIRMAR_CODIGO (
                ID_USUARIO,
                CODIGO,
                UTILIZADO
            )
            VALUES (?, ?, FALSE)
        """, (
            id_usuario,
            codigo_confirmacao
        ))

        con.commit()

        # ENVIAR EMAIL
        assunto = "Confirme seu cadastro"

        corpo = f"""
Seu código de confirmação é:

{codigo_confirmacao}
"""

        threading.Thread(
            target=enviando_email,
            args=(email, assunto, corpo)
        ).start()

        return jsonify({
            "mensagem": "Usuário criado com sucesso!",
            "id_usuario": id_usuario,
            "tipo": tipo_nome
        }), 201

    except Exception as e:

        con.rollback()

        return jsonify({
            'erro': f'Erro no banco: {str(e)}'
        }), 500

    finally:
        con.close()

@app.route('/confirmar_codigo', methods=['POST'])
def confirmar_codigo():

    con = get_db_connection()
    cur = con.cursor()

    try:

        dados = request.get_json(silent=True) or request.form

        id_usuario = dados.get('id_usuario')
        codigo = dados.get('codigo')

        # VALIDAR CAMPOS
        if not id_usuario or not codigo:
            return jsonify({
                'erro': 'ID do usuário e código são obrigatórios.'
            }), 400

        # VERIFICAR CÓDIGO
        cur.execute("""
            SELECT UTILIZADO
            FROM CONFIRMAR_CODIGO
            WHERE ID_USUARIO = ?
            AND CODIGO = ?
        """, (
            id_usuario,
            codigo
        ))

        resultado = cur.fetchone()

        # CÓDIGO NÃO EXISTE
        if not resultado:
            return jsonify({
                'erro': 'Código inválido.'
            }), 400

        # CÓDIGO JÁ UTILIZADO
        if resultado[0]:
            return jsonify({
                'erro': 'Código já utilizado.'
            }), 400

        # CONFIRMAR CONTA
        cur.execute("""
            UPDATE USUARIO
            SET CONTA_CONFIRMADA = TRUE
            WHERE ID_USUARIO = ?
        """, (
            id_usuario,
        ))

        # MARCAR CÓDIGO COMO UTILIZADO
        cur.execute("""
            UPDATE CONFIRMAR_CODIGO
            SET UTILIZADO = TRUE
            WHERE ID_USUARIO = ?
            AND CODIGO = ?
        """, (
            id_usuario,
            codigo
        ))

        con.commit()

        return jsonify({
            'mensagem': 'Conta confirmada com sucesso!'
        }), 200

    except Exception as e:

        con.rollback()

        return jsonify({
            'erro': f'Erro ao confirmar código: {str(e)}'
        }), 500

    finally:
        con.close()

@app.route('/login_usuario', methods=['POST'])
def login_usuario():
    con = get_db_connection()

    if con is None:
        return jsonify({
            "erro": "Falha ao conectar ao banco de dados"
        }), 500

    def get_db_connection():
        try:
            print("Tentando conectar...")

            conn = fdb.connect(
                dsn=r'C:\Users\Aluno\Desktop\otavio\Back_otavio-main\BANCO.FDB',
                user='SYSDBA',
                password='sysdba',
                charset='UTF8',
                fb_library_name=r'C:\Program Files\Firebird\Firebird_3_0\fbclient.dll'
            )

            print("CONECTOU")
            return conn

        except Exception as e:
            print("ERRO REAL:")
            print(repr(e))
            raise
    cur = con.cursor()
    dados = request.get_json(silent=True) or request.form

    email = dados.get('email')
    senha = dados.get('senha')

    try:

        # VALIDAR CAMPOS
        if not email or not senha:
            return jsonify({
                'erro': 'Email e senha são obrigatórios.'
            }), 400

        # BUSCAR USUÁRIO
        cur.execute("""
            SELECT
                ID_USUARIO,
                SENHA,
                NOME,
                ID_TIPO,
                TIPO_NOME,
                CONTA_CONFIRMADA,
                BLOQUEADO,
                TENTATIVAS_LOGIN,
                ATIVO
            FROM USUARIO
            WHERE EMAIL = ?
        """, (email,))

        resultado = cur.fetchone()

        # USUÁRIO NÃO EXISTE
        if not resultado:
            return jsonify({
                'erro': 'Usuário não encontrado.'
            }), 404

        (
            id_usuario,
            senha_hash,
            nome,
            id_tipo,
            tipo_nome,
            confirmado,
            bloqueado,
            tentativas,
            ativo
        ) = resultado

        # USUÁRIO INATIVO
        if not ativo:
            return jsonify({
                'erro': 'Usuário desativado.'
            }), 403

        # CONTA BLOQUEADA
        if bloqueado:
            return jsonify({
                'erro': 'Conta bloqueada por excesso de tentativas.'
            }), 403

        # CONTA NÃO CONFIRMADA
        if not confirmado:
            return jsonify({
                'erro': 'E-mail não confirmado.'
            }), 403

        # VERIFICAR SENHA
        if checar_senha(senha, senha_hash):

            # RESETAR TENTATIVAS
            cur.execute("""
                UPDATE USUARIO
                SET TENTATIVAS_LOGIN = 0
                WHERE ID_USUARIO = ?
            """, (
                id_usuario,
            ))

            con.commit()

            # TOKEN JWT
            payload = {
                'id_usuario': id_usuario,
                'id_tipo': id_tipo,
                'tipo': tipo_nome,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }

            token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            return jsonify({
                'mensagem': f'Bem-vindo {nome}!',
                'token': token,
                'id_usuario': id_usuario,
                'tipo': tipo_nome,
                'id_tipo': id_tipo
            }), 200

        # SENHA INCORRETA
        else:
            tentativas += 1

            # BLOQUEAR APÓS 3 TENTATIVAS
            if tentativas >= 3:

                cur.execute("""
                    UPDATE USUARIO
                    SET
                        TENTATIVAS_LOGIN = ?,
                        BLOQUEADO = TRUE
                    WHERE ID_USUARIO = ?
                """, (
                    tentativas,
                    id_usuario
                ))

                con.commit()

                return jsonify({
                    'erro': 'Conta bloqueada após 3 tentativas.'
                }), 403

            # ATUALIZAR TENTATIVAS
            else:

                cur.execute("""
                    UPDATE USUARIO
                    SET TENTATIVAS_LOGIN = ?
                    WHERE ID_USUARIO = ?
                """, (
                    tentativas,
                    id_usuario
                ))

                con.commit()

                return jsonify({
                    'erro': f'Senha incorreta. Tentativa {tentativas} de 3.'
                }), 401

    except Exception as e:

        con.rollback()

        return jsonify({
            'erro': f'Erro interno: {str(e)}'
        }), 500

    finally:
        con.close()

# ---------------------------------------------------------
# 3. LISTAR USUÁRIOS
# ---------------------------------------------------------
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    con = get_db_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT ID_USUARIO, NOME, EMAIL, TIPO_NOME, CONTA_CONFIRMADA FROM USUARIO")
        rows = cur.fetchall()
        res = [{'id': r[0], 'nome': r[1], 'email': r[2], 'tipo': r[3], 'confirmado': r[4]} for r in rows]
        return jsonify(res), 200
    finally:
        con.close()


import re


@app.route('/editar_usuario/<int:id>', methods=['PUT'])
def editar_usuario(id):
    con = get_db_connection()
    if con is None:
        return jsonify({'erro': 'Erro de conexão com o banco de dados.'}), 500

    cur = con.cursor()
    try:
        dados = request.get_json(silent=True) or request.form
        nome = dados.get('nome')
        nova_senha = dados.get('senha')

        # 1. VALIDAÇÃO DO NOME (Não permite branco)
        if nome is not None:
            nome_limpo = nome.strip()
            if not nome_limpo:
                return jsonify({"erro": "O nome não pode estar em branco."}), 400
            cur.execute("UPDATE USUARIO SET NOME = ? WHERE ID_USUARIO = ?", (nome_limpo, id))

        # 2. VALIDAÇÃO DE SENHA (Forte + Diferente da anterior)
        if nova_senha:
            # Regras de Senha Forte
            if (len(nova_senha) < 8 or
                    not re.search(r"[a-z]", nova_senha) or
                    not re.search(r"[A-Z]", nova_senha) or
                    not re.search(r"[0-9]", nova_senha)):
                return jsonify(
                    {"erro": "A senha deve ter pelo menos 8 caracteres, com maiúsculas, minúsculas e números."}), 400

            # --- VERIFICAÇÃO DE SENHA ANTERIOR ---
            cur.execute("SELECT SENHA FROM USUARIO WHERE ID_USUARIO = ?", (id,))
            resultado = cur.fetchone()

            if resultado:
                senha_hash_atual = resultado[0]
                # Se a nova senha (texto puro) for igual ao hash atual...
                if checar_senha(nova_senha, senha_hash_atual):
                    return jsonify({"erro": "A nova senha não pode ser igual à senha atual."}), 400
            # -------------------------------------

            # Criptografa e atualiza
            senha_final_hash = criptografar(nova_senha)
            cur.execute("UPDATE USUARIO SET SENHA = ? WHERE ID_USUARIO = ?", (senha_final_hash, id))

        # 3. TRATAMENTO DA FOTO
        foto = request.files.get('foto')
        if foto:
            foto.save(os.path.join(UPLOAD_FOLDER, f"perfil_{id}.jpg"))

        con.commit()
        return jsonify({"mensagem": "Dados atualizados com sucesso"}), 200

    except Exception as e:
        if con: con.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if con: con.close()

# ---------------------------------------------------------
# 5. EXCLUIR USUÁRIO
# ---------------------------------------------------------
@app.route('/excluir_usuario/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    con = get_db_connection()
    if not validar_conexao(con): return jsonify({'erro': 'Banco offline'}), 500
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM USUARIO WHERE ID_USUARIO = ?", (id,))
        con.commit()
        return jsonify({"mensagem": "Usuário removido"}), 200
    except Exception as e:
        con.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        con.close()


@app.route('/solicitar_recuperacao', methods=['POST'])
def solicitar_recuperacao():
    con = get_db_connection()
    if con is None:
        return jsonify({'erro': 'Erro de conexão com o banco de dados.'}), 500

    cur = con.cursor()
    try:
        # Aceita JSON ou Formulário
        dados = request.get_json(silent=True) or request.form
        email = dados.get('email')

        if not email:
            return jsonify({'erro': 'O e-mail é obrigatório.'}), 400

        # 1. Verificar se o usuário existe
        cur.execute("SELECT ID_USUARIO FROM USUARIO WHERE EMAIL = ?", (email,))
        user = cur.fetchone()

        if user:
            id_usuario = user[0]

            # 2. Gerar código de 6 dígitos aleatório
            codigo = str(random.randint(100000, 999999))

            # 3. Definir expiração (ex: 15 minutos a partir de agora)
            expiracao = datetime.datetime.now() + datetime.timedelta(minutes=15)

            # 4. Inserir na tabela RECUPERAR_SENHA conforme seu SQL
            cur.execute("""
                INSERT INTO RECUPERAR_SENHA (ID_USUARIO, CODIGO, EXPIRACAO, UTILIZADO) 
                VALUES (?, ?, ?, False)
            """, (id_usuario, codigo, expiracao))

            con.commit()

            # 5. Enviar o e-mail de forma assíncrona (Thread) para não travar a resposta
            threading.Thread(target=enviando_email, args=(
                email,
                "Recuperação de Senha",
                f"Seu código de recuperação é: {codigo}. Ele expira em 15 minutos."
            )).start()

            return jsonify(
                {"mensagem": "Se o e-mail informado estiver cadastrado, você receberá um código de 6 dígitos."}), 200

        # Por segurança, mesmo que o e-mail não exista, damos a mesma resposta para evitar varredura de e-mails
        return jsonify(
            {"mensagem": "Você receberá um código de 6 dígitos para criar uma nova senha."}), 200

    except Exception as e:
        if con: con.rollback()
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500
    finally:
        if con: con.close()



# ---------------------------------------------------------
# 6. REDEFINIR SENHA (Nova Senha e Confirmar Senha)
# ---------------------------------------------------------
@app.route('/redefinir_senha', methods=['POST'])
def redefinir_senha():
    con = get_db_connection()
    if con is None:
        return jsonify({'erro': 'Erro de conexão com o banco de dados.'}), 500

    cur = con.cursor()
    try:
        # Resolve o Erro 415: Aceita JSON ou Form-data do Postman
        dados = request.get_json(silent=True) or request.form

        codigo = dados.get('codigo')
        nova_senha = dados.get('nova_senha')
        confirmar_senha = dados.get('confirmar_senha')

        # 1. Validações básicas de preenchimento
        if not all([codigo, nova_senha, confirmar_senha]):
            return jsonify({"erro": "Todos os campos (codigo, nova_senha, confirmar_senha) são obrigatórios."}), 400

        if nova_senha != confirmar_senha:
            return jsonify({"erro": "As senhas não coincidem."}), 400

        # 2. Validação de Senha Forte
        if (len(nova_senha) < 8 or
                not re.search(r"[a-z]", nova_senha) or
                not re.search(r"[A-Z]", nova_senha) or
                not re.search(r"[0-9]", nova_senha)):
            return jsonify({
                               "erro": "A nova senha deve ter no mínimo 8 caracteres, incluindo letras maiúsculas, minúsculas e números."}), 400

        # 3. Verifica se o código é válido e pertence a um usuário
        cur.execute("""
            SELECT ID_USUARIO FROM RECUPERAR_SENHA 
            WHERE CODIGO = ? AND UTILIZADO = False AND EXPIRACAO > CURRENT_TIMESTAMP
        """, (codigo,))
        res = cur.fetchone()

        if not res:
            return jsonify({"erro": "Código inválido, já utilizado ou expirado."}), 400

        id_u = res[0]

        # 4. Verificação de reuso: Não permite a senha que já está no banco
        cur.execute("SELECT SENHA FROM USUARIO WHERE ID_USUARIO = ?", (id_u,))
        senha_hash_atual = cur.fetchone()[0]

        if checar_senha(nova_senha, senha_hash_atual):
            return jsonify({"erro": "A nova senha não pode ser igual à senha antiga."}), 400

        # 5. Atualiza a senha e invalida o código usado
        cur.execute("UPDATE USUARIO SET SENHA = ? WHERE ID_USUARIO = ?", (criptografar(nova_senha), id_u))
        cur.execute("UPDATE RECUPERAR_SENHA SET UTILIZADO = True WHERE CODIGO = ?", (codigo,))

        con.commit()
        return jsonify({"mensagem": "Senha alterada com sucesso!"}), 200

    except Exception as e:
        if con: con.rollback()
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500
    finally:
        if con: con.close()


@app.route('/buscar_usuario', methods=['GET'])
def buscar_usuario():
    con = get_db_connection()
    if con is None:
        return jsonify({'erro': 'Erro de conexão com o banco de dados.'}), 500

    cur = con.cursor()
    try:
        # Pega o termo da URL
        termo = request.args.get('termo', '').strip()

        # Se o usuário não digitar nada, em vez de erro, retornamos todos (ou uma lista vazia)
        if not termo:
            cur.execute("SELECT ID_USUARIO, NOME, EMAIL, TIPO_NOME FROM USUARIO")
        elif termo.isdigit():
            # Busca por ID exato
            cur.execute("""
                SELECT ID_USUARIO, NOME, EMAIL, TIPO_NOME 
                FROM USUARIO WHERE ID_USUARIO = ?
            """, (termo,))
        else:
            # Busca por Nome ou Email usando LIKE (formatado para o banco)
            # O UPPER garante que não haja erro entre maiúsculas e minúsculas
            filtro = f"%{termo.upper()}%"
            cur.execute("""
                SELECT ID_USUARIO, NOME, EMAIL, TIPO_NOME 
                FROM USUARIO 
                WHERE UPPER(NOME) LIKE ? OR UPPER(EMAIL) LIKE ?
            """, (filtro, filtro))

        rows = cur.fetchall()

        # Converte para JSON
        resultados = []
        for r in rows:
            resultados.append({
                'id': r[0],
                'nome': r[1],
                'email': r[2],
                'tipo': r[3]
            })

        return jsonify(resultados), 200

    except Exception as e:
        return jsonify({'erro': f'Erro no banco: {str(e)}'}), 500
    finally:
        if con:
            con.close()



@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"mensagem": "Logout realizado. Delete o token no cliente."}), 200