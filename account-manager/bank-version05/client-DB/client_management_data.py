import sqlite3
from pathlib import Path

ROOT_PATH_DB = Path(__file__).parent / "client_data.sqlite"

def create_clients_table(connection, cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(150) NOT NULL,
        email VARCHAR(200) NOT NULL,
        date_birth INTEGER NOT NULL,
        cpf INTEGER NOT NULL,
        address VARCHAR(200) NOT NULL
    )
    """)
    connection.commit()

def save_client_infodb(name, email, date_birth, cpf, address):
    connection = sqlite3.connect(ROOT_PATH_DB)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Clients (name, email, date_birth, cpf, address) VALUES (?, ?, ?, ?, ?);", 
                   (name, email, date_birth, cpf, address))
    connection.commit()
    connection.close()

def initialize_db():
    connection = sqlite3.connect(ROOT_PATH_DB)
    cursor = connection.cursor()
    create_clients_table(connection, cursor)
    connection.close()