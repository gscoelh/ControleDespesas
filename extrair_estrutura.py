import pyodbc

db_path = r"C:\Users\User\Documents\CONTROLE DESPESAS\NOVODESPESAS_OQUE TEM ESTE_20251120.mdb"

conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    fr"Dbq={db_path};"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

saida = []

saida.append("===== ESTRUTURA DO BANCO DE DADOS ACCESS =====\n")

# Lista todas as tabelas reais (ignorando MSys)
tables = []
for row in cursor.tables():
    if row.table_type == "TABLE" and not row.table_name.startswith("MSys"):
        tables.append(row.table_name)

# Para cada tabela, listar colunas e tipos
for table in tables:
    saida.append(f"TABELA: {table}")
    saida.append("-" * 50)

    try:
        for col in cursor.columns(table=table):
            nome = col.column_name
            tipo = col.type_name
            saida.append(f"  {nome}   ({tipo})")
    except Exception as e:
        saida.append(f"  ERRO ao ler colunas: {e}")

    saida.append("\n")

cursor.close()
conn.close()

# Salvar em arquivo TXT
arquivo_saida = r"C:\Users\User\Documents\estrutura_banco_access.txt"

with open(arquivo_saida, "w", encoding="utf-8") as f:
    f.write("\n".join(saida))

print(f"Estrutura exportada para:\n{arquivo_saida}")
