import psycopg2
import jwt
import time
from typing import Optional
from src.config.settings import AUTH_SETTINGS, DATABASE_SETTINGS
from src.models.character import Player
from src.display.common.message_view import MessageView

class SessionManagementService:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DATABASE_SETTINGS["DB_NAME"],
            user=DATABASE_SETTINGS["DB_USER"],
            password=DATABASE_SETTINGS["DB_PASSWORD"],
            host=DATABASE_SETTINGS["DB_HOST"],
            port=DATABASE_SETTINGS["DB_PORT"]
        )
        self.jwt_secret_key = AUTH_SETTINGS["JWT_SECRET_KEY"]
        self.jwt_algorithm = AUTH_SETTINGS["JWT_ALGORITHM"]
        self.session_timeout = AUTH_SETTINGS["SESSION_TIMEOUT"]

    def create_session(self, player: Player) -> str:
        session_id = self._generate_session_id(player)
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (session_id, player_data, expiration) VALUES (%s, %s, %s)",
            (session_id, jwt.encode(player.serialize(), self.jwt_secret_key, algorithm=self.jwt_algorithm), time.time() + self.session_timeout)
        )
        self.conn.commit()
        cursor.close()
        return session_id

    def get_session(self, session_id: str) -> Optional[Player]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT player_data FROM sessions WHERE session_id = %s", (session_id,))
        session_data = cursor.fetchone()
        cursor.close()
        if session_data:
            player_data = jwt.decode(session_data[0], self.jwt_secret_key, algorithms=[self.jwt_algorithm])
            return Player.deserialize(player_data)
        return None

    def _generate_session_id(self, player: Player) -> str:
        payload = {
            "player_id": player.name,
            "exp": time.time() + self.session_timeout,
        }
        return jwt.encode(payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

    def authenticate_player(self) -> Optional[Player]:
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Placeholder authentication logic
        if username == "player" and password == "password":
            player = Player(name=username, char_class=None)  # Replace with actual character class
            session_id = self.create_session(player)
            player.session_id = session_id
            return player
        else:
            MessageView.show_error("Invalid username or password")
            return None

    def show_login_screen(self):
        print("Welcome to the game! Please log in.")
