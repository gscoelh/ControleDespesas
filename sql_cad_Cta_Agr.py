from db import get_connection

def listar():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM CADCTAAGR ORDER BY COD_AGR")
    return cur.fetchall()

def inserir(nome, descricao):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO CADCTAAGR (NOME_AGR, DESCRICAO) VALUES (?, ?)", (nome, descricao))
    conn.commit()

def atualizar(cod, nome, descricao):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE CADCTAAGR SET NOME_AGR=?, DESCRICAO=? WHERE COD_AGR=?", (nome, descricao, cod))
    conn.commit()

def excluir(cod):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM CADCTAAGR WHERE COD_AGR=?", (cod,))
    conn.commit()
