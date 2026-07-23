from core.db import get_connection

def listar():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT CODLOTE, DESCRLOTE, FORMAT(DTAABERTURA, 'dd/mm/yyyy')
        FROM TIPOLOTE
        ORDER BY CODLOTE
    """)
    return cur.fetchall()

def existe(cod):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM TIPOLOTE WHERE CODLOTE=?", (cod,))
    return cur.fetchone()[0] > 0

def inserir(cod, descr, dta):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO TIPOLOTE (CODLOTE, DESCRLOTE, DTAABERTURA)
        VALUES (?, ?, ?)
    """, (cod, descr, dta))
    conn.commit()

def atualizar(cod, descr, dta):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE TIPOLOTE
        SET DESCRLOTE=?, DTAABERTURA=?
        WHERE CODLOTE=?
    """, (descr, dta, cod))
    conn.commit()

def excluir(cod):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM TIPOLOTE WHERE CODLOTE=?", (cod,))
    conn.commit()
