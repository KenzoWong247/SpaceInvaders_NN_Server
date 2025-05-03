import asyncio
import atexit
import json

from websockets import serve
from websockets.exceptions import ConnectionClosedError

from game_agent import GameAgent

class Server:
    shutdown_event = asyncio.Event()
    clients_close_event = asyncio.Event()
    server_close_complete = asyncio.Event()
    clients = {}

    def __init__(self):
        atexit.register(self.cleanup)

    def cleanup(self):
        pass

    def close_server(self):
        self.shutdown_event.set()

    def handle_message(self):
        pass

    def handle_data(self):
        pass

    async def send_data(self, data):
        pass


    async def _handle_data(self, websocket):
        client = GameAgent()

        try:
            async for message in websocket:
                print(f'Client Message: {message}')

                try:
                    data =  json.loads(message)
                except ValueError:
                    return None


        except ConnectionClosedError:
            print(f'Client {client.client_id} disconnected')
        finally:
            pass

    # noinspection PyTypeChecker
    async def start(self):
        async with serve(self._handle_data, "", 8001) as server:
            print("Server Started")
            await self.shutdown_event.wait()
            server.close()
            await self.server_close_complete.wait()
            print("Server Closed")
