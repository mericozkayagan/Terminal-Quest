import json
from typing import Dict, Any
from src.models.character import Player, Enemy
from src.config.settings import DATABASE_SETTINGS
import psycopg2


class GameStateService:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=DATABASE_SETTINGS["DB_NAME"],
            user=DATABASE_SETTINGS["DB_USER"],
            password=DATABASE_SETTINGS["DB_PASSWORD"],
            host=DATABASE_SETTINGS["DB_HOST"],
            port=DATABASE_SETTINGS["DB_PORT"],
        )
        self.cursor = self.connection.cursor()

    def save_game_state(self, player: Player, shop: Any) -> None:
        """Save the current game state to the database"""
        game_state = {
            "player": player.serialize(),
            "shop": shop.serialize(),
        }
        game_state_json = json.dumps(game_state)
        self.cursor.execute(
            """
            INSERT INTO game_states (player_id, game_state)
            VALUES (%s, %s)
            ON CONFLICT (player_id) DO UPDATE
            SET game_state = EXCLUDED.game_state
            """,
            (player.name, game_state_json),
        )
        self.connection.commit()

    def load_game_state(self, player: Player) -> Dict[str, Any]:
        """Load the game state from the database"""
        self.cursor.execute(
            """
            SELECT game_state FROM game_states
            WHERE player_id = %s
            """,
            (player.name,),
        )
        result = self.cursor.fetchone()
        if result:
            game_state_json = result[0]
            game_state = json.loads(game_state_json)
            return {
                "player": Player.deserialize(game_state["player"]),
                "shop": Shop.deserialize(game_state["shop"]),
            }
        return {}

    def serialize_game_object(self, obj: Any) -> str:
        """Serialize a game object to JSON"""
        return json.dumps(obj.serialize())

    def deserialize_game_object(self, json_str: str, obj_type: str) -> Any:
        """Deserialize a game object from JSON"""
        data = json.loads(json_str)
        if obj_type == "Player":
            return Player.deserialize(data)
        elif obj_type == "Enemy":
            return Enemy.deserialize(data)
        # Add more object types as needed
        return None

    def update_game_state(self, player: Player, shop: Any) -> None:
        """Update the game state in the database after each significant event"""
        self.save_game_state(player, shop)

    def close(self):
        """Close the database connection"""
        self.cursor.close()
        self.connection.close()
