import json
import sqlite3
import os

from dotenv import load_dotenv

load_dotenv()

def recreate_db() -> None:
    connection = sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH'))
    with connection:
        connection.execute('DROP TABLE IF EXISTS telegram_updates')
        connection.execute("""
            CREATE TABLE IF NOT EXISTS telegram_updates
            (
                id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """)
    connection.close()
    
def persist_update(update: dict) -> None:
    payload = json.dumps(update, ensure_ascii=False)
    with sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH")) as connection:
        with connection:
            connection.execute("INSERT INTO telegram_updates (payload) VALUES (?)", (payload,))
