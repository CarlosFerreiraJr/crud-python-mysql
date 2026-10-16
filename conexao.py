
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Recupera as configurações
host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT", "3306"))
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

#===========================================================
#     Descrição:
#         Estabelece uma conexão com o banco de dados MySQL,
#         utilizando as credenciais armazenadas no arquivo .env.

#     Parâmetros:
#         Nenhum.

#     Retorno:
#         Objeto de conexão MySQL, caso seja bem-sucedida.
#         None, caso ocorra algum erro.
#===========================================================
def conectar():
    conexao = None

    try:
        conexao = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
        )

        return conexao

    except Error as erro:
        print(f"Erro ao consultar MySQL: {erro}")

#============================================================
#    Descrição:
#        Encerra uma conexão ativa com o banco de dados MySQL.
#
#    Parâmetros:
#        conexao: Objeto de conexão MySQL que será encerrado.
#
#    Retorno:
#        Nenhum.
#============================================================
def desconectar(conexao):
    try:
        if conexao is not None and conexao.is_connected():
            conexao.close()

    except Error as erro:
        print(f"\nErro ao desconectar do MySQL: {erro}")
