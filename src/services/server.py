import asyncio
import websockets
import json
from .session_management import SessionManagementService
from .game_state import GameStateService
from ..models.character import Player
from ..services.character_creation import CharacterCreationService

connected_clients = set()
waiting_clients = set()


async def handle_client(websocket, path):
    connected_clients.add(websocket)
    session_service = SessionManagementService()
    game_state_service = GameStateService()

    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")

            if action == "authenticate":
                player = session_service.authenticate_player(
                    data["username"], data["password"]
                )
                if player:
                    if not player.char_class:
                        classes = CharacterCreationService._get_character_classes()
                        await websocket.send(
                            json.dumps(
                                {
                                    "status": "success",
                                    "message": "Authenticated",
                                    "classes": [cls.name for cls in classes],
                                }
                            )
                        )
                    else:
                        await websocket.send(
                            json.dumps(
                                {
                                    "status": "success",
                                    "message": "Authenticated",
                                    "player": player.serialize(),
                                }
                            )
                        )
                else:
                    await websocket.send(
                        json.dumps(
                            {"status": "error", "message": "Authentication failed"}
                        )
                    )

            elif action == "select_class":
                class_name = data.get("class_name")
                classes = CharacterCreationService._get_character_classes()
                chosen_class = next(
                    (cls for cls in classes if cls.name == class_name), None
                )
                if chosen_class:
                    player.char_class = chosen_class
                    session_id = session_service.create_session(player)
                    player.session_id = session_id
                    await websocket.send(
                        json.dumps(
                            {
                                "status": "success",
                                "message": "Class selected",
                                "session_id": session_id,
                            }
                        )
                    )
                else:
                    await websocket.send(
                        json.dumps(
                            {"status": "error", "message": "Invalid class selection"}
                        )
                    )

            elif action == "load_game_state":
                player = Player.deserialize(data["player"])
                game_state = game_state_service.load_game_state(player)
                await websocket.send(
                    json.dumps({"status": "success", "game_state": game_state})
                )

            elif action == "wait_for_players":
                waiting_clients.add(websocket)
                await websocket.send(
                    json.dumps(
                        {
                            "status": "waiting",
                            "message": "Waiting for other players to connect..."
                        }
                    )
                )
                while len(waiting_clients) < 2:
                    await asyncio.sleep(1)
                waiting_clients.remove(websocket)
                await websocket.send(
                    json.dumps(
                        {
                            "status": "start_game",
                            "message": "All players connected. Starting the game..."
                        }
                    )
                )

    finally:
        connected_clients.remove(websocket)
        if websocket in waiting_clients:
            waiting_clients.remove(websocket)


async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
