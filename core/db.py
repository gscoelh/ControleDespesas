import pyodbc
from core import config

def get_connection():
    DB_PATH = config.get_db_path()


    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        fr"Dbq={DB_PATH};"
    )
    
    conn = pyodbc.connect(conn_str)
    return conn
