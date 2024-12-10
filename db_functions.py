from config import * 
import mysql.connector

def conectar_db():
    conexao = mysql.connector.connect(
        host = DB_HOST, 
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )
    return conexao

def encerrar_db(cursor, conexao):
    cursor.close()
    conexao.close()

def iniciar_db():
    conexao = conectar_db()
    cursor = conexao.cursor()
    return conexao, cursor