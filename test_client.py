from websockets.sync.client import connect
import json
URI = "ws://localhost:8001"




def send_message():

    with connect(URI) as websocket:
        while True:
            try:
                message = input("What is your message? ")

                if message.lower() == 'data':
                    pass
                    # message = json.dumps(mock_data)

                websocket.send(message)
                print(f"Sent {message} to server")

                response = websocket.recv()
                if response:
                    response_dict = json.loads(response)
                    print(f"Server responded with: {response}")
                    # if response_dict["response"] in close_messages:
                    #   exit(1)
                else:
                    print("No Response from Server")

            except KeyboardInterrupt:
                print("Exited Manually")
