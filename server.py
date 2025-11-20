import asyncio
import atexit
import json

from websockets import serve
from websockets.exceptions import ConnectionClosedError

from game_agent import GameAgent
from network_trainer import Trainer

class Server:
    shutdown_event = asyncio.Event()
    clients_close_event = asyncio.Event()
    server_close_complete = asyncio.Event()
    clients = {}
    server_commands = {
        "shutdown": shutdown_event,
        "close_clients": clients_close_event
    }
    command_responses = {
        "shutdown": "Server set to shutdown confirmed",
        "close_clients": "Clients sent shutdown command"
    }


    def __init__(self, trainer: Trainer):
        atexit.register(self.cleanup)
        self.trainer = trainer

    def cleanup(self):
        pass

    def close_server(self):
        self.shutdown_event.set()

    def handle_message(self, message):
        # TODO: Handle client commands
        server_command = self.server_commands.get(message)
        if server_command:
            server_command.set()
            return {'message': self.command_responses[message]}
        else:
            print(f'Unknown Command: {message}')

    def handle_data(self, client_id, data):
        # TODO: Pass Data to Game Agent and receive a game action in return
        if client_id in self.clients.keys():
            return self.clients[client_id].get_action(data)
        else:
            print(f'Unknown client: {client_id}')

    async def send_data(self, websocket, data):
        json_data = json.dumps(data)

    async def _handle_data(self, websocket):
        client = GameAgent(self.trainer)

        try:
            async for message in websocket:
                print(f'Client Message: {message}')


                try:
                    data =  json.loads(message)
                    response = self.handle_data(client.client_id, data)
                except ValueError:
                    response = self.handle_message(message)

                if response:
                    await websocket.send(response)

        except ConnectionClosedError:
            print(f'Client {client.client_id} disconnected')
        finally:
            # TODO: Agent cleanup and deletion
            pass

    # noinspection PyTypeChecker
    async def start(self):
        async with serve(self._handle_data, "", 8001) as server:
            print("Server Started")
            await self.shutdown_event.wait()
            server.close()
            await self.server_close_complete.wait()
            print("Server Closed")
