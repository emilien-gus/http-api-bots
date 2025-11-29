from bot.domain.storage import Storage
import json
import pg8000
import os
from dotenv import load_dotenv

load_dotenv()


class StoragePostgres(Storage):
    def _get_connection(self):
        """Get PostgreSQL connection using pg8000."""
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        database = os.getenv("POSTGRES_DB")

        if host is None:
            raise ValueError("POSTGRES_PASSWORD environment variable is not set")
        if port is None:
            raise ValueError("POSTGRES_PORT environment variable is not set")
        if user is None:
            raise ValueError("POSTGRES_USER environment variable is not set")
        if password is None:
            raise ValueError("POSTGRES_PASSWORD environment variable is not set")
        if database is None:
            raise ValueError("POSTGRES_DB environment variable is not set")

        return pg8000.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )

    def recreate_db(self) -> None:
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS telegram_updates")
                cursor.execute("DROP TABLE IF EXISTS users")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS telegram_updates
                    (
                        id SERIAL PRIMARY KEY,
                        payload TEXT NOT NULL
                    )
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users
                    (
                        id SERIAL PRIMARY KEY,
                        telegram_id BIGINT NOT NULL UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        state TEXT DEFAULT NULL,
                        data TEXT DEFAULT NULL
                    )
                    """
                )
            connection.commit()
        finally:
            connection.close()

    def persist_update(self, update: dict) -> None:
        payload = json.dumps(update, ensure_ascii=False)
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO telegram_updates (payload) VALUES (%s)", (payload,)
                )
            connection.commit()
        finally:
            connection.close()

    def ensure_user_exists(self, telegram_id: int) -> None:
        """Ensure a user with the given telegram_id exists in the users table."""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM users WHERE telegram_id = %s", (telegram_id,)
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO users (telegram_id) VALUES (%s)", (telegram_id,)
                    )
            connection.commit()
        finally:
            connection.close()

    def get_user(self, telegram_id: int) -> dict:
        """Get complete user object from the users table by telegram_id."""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, telegram_id, created_at, state, data 
                    FROM users WHERE telegram_id = %s
                    """,
                    (telegram_id,),
                )
                result = cursor.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "telegram_id": result[1],
                        "created_at": result[2],
                        "state": result[3],
                        "data": result[4],
                    }
                return None
        finally:
            connection.close()

    def update_user_state(self, telegram_id: int, state: str) -> None:
        """Update user state in the users table."""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET state = %s WHERE telegram_id = %s",
                    (state, telegram_id),
                )
            connection.commit()
        finally:
            connection.close()

    def update_user_data(self, telegram_id: int, data: dict) -> None:
        """Update user data with a JSON object in the users table."""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET data = %s WHERE telegram_id = %s",
                    (json.dumps(data, ensure_ascii=False), telegram_id),
                )
            connection.commit()
        finally:
            connection.close()

    def clear_user_data(self, telegram_id: int) -> None:
        """Clear user state and data in the users table."""
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET state = NULL, data = NULL WHERE telegram_id = %s",
                    (telegram_id,),
                )
            connection.commit()
        finally:
            connection.close()
