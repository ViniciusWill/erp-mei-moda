import sqlite3
from pathlib import Path


class BaseRepository:
    def __init__(self):
       self.caminho_db = Path(r"C:\Users\vinicius.gomes\Desktop\py\loja-roupa-py\dados\sistema_loja.db") 
    
    def __conection__(self):
        conn = sqlite3.connect(self.caminho_db)
        conn.row_factory = sqlite3.Row
        return conn