from core.db import get_connection

def listar():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ROTEIRO, ROTNATUREZA, ROTCTADEB, ROTCTACRED, ROTHIST
        FROM ROTEIRODETA
        ORDER BY ROTEIRO
    """)
    return cur.fetchall()

def listar_por_roteiro(rot):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ROTEIRO, ROTNATUREZA, ROTCTADEB, ROTCTACRED, ROTHIST
        FROM ROTEIRODETA
        WHERE ROTEIRO = ?
    """, (rot,))
    return cur.fetchall()

def existe_conta_no_roteiro(rot, deb, cred):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM ROTEIRODETA
        WHERE ROTEIRO = ?
          AND ROTCTADEB = ?
          AND ROTCTACRED = ?
    """, (rot, deb, cred))
    return cur.fetchone()[0] > 0

def inserir(rot, natureza, deb, cred, hist):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ROTEIRODETA (ROTEIRO, ROTNATUREZA, ROTCTADEB, ROTCTACRED, ROTHIST)
        VALUES (?, ?, ?, ?, ?)
    """, (rot, natureza, deb, cred, hist))
    conn.commit()

def atualizar(rot, natureza, deb, cred, hist):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE ROTEIRODETA
        SET ROTNATUREZA=?, ROTCTADEB=?, ROTCTACRED=?, ROTHIST=?
        WHERE ROTEIRO=?
    """, (natureza, deb, cred, hist, rot))
    conn.commit()

def excluir(rot, deb, cred):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM ROTEIRODETA
        WHERE ROTEIRO=? AND ROTCTADEB=? AND ROTCTACRED=?
    """, (rot, deb, cred))
    conn.commit()
