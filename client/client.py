import asyncio
import websockets
import json


async def connect_to_server():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Authenticate player
        await websocket.send(
            json.dumps(
                {"action": "authenticate", "username": "player", "password": "password"}
            )
        )
        response = await websocket.recv()
        print(response)

        # If class selection is required
        response_data = json.loads(response)
        if "classes" in response_data:
            print("Available classes:")
            for i, class_name in enumerate(response_data["classes"], 1):
                print(f"{i}. {class_name}")

            class_choice = int(input("Select your class: ")) - 1
            selected_class = response_data["classes"][class_choice]

            # Send class selection to server
            await websocket.send(
                json.dumps({"action": "select_class", "class_name": selected_class})
            )
            response = await websocket.recv()
            print(response)

        # Load game state
        await websocket.send(
            json.dumps({"action": "load_game_state", "player": {"name": "player"}})
        )
        response = await websocket.recv()
        print(response)

        # Wait for other players to connect
        await websocket.send(json.dumps({"action": "wait_for_players"}))
        response = await websocket.recv()
        print(response)
        response_data = json.loads(response)
        if response_data.get("status") == "waiting":
            print("Waiting for other players to connect...")
            while response_data.get("status") == "waiting":
                response = await websocket.recv()
                response_data = json.loads(response)
                print(response_data.get("message"))

        if response_data.get("status") == "start_game":
            print("All players connected. Starting the game...")


if __name__ == "__main__":
    asyncio.run(connect_to_server())
