import socket
import json


class Client:
    def __init__(self, host='127.0.0.1', port=31337):
        self.host = host
        self.port = port

    def send_request(self, action, key=None, value=None, keys=None, items=None):
        request = {'action': action}
        if key is not None:
            request['key'] = key
        if value is not None:
            request['value'] = value
        if keys is not None:
            request['keys'] = keys
        if items is not None:
            request['items'] = items

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                client_socket.send(json.dumps(request).encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                return json.loads(response)
        except ConnectionRefusedError:
            return "Could not connect to the server"

    def run(self):
        print("Currently in client - enter 'bye' to quit:")
        while True:
            try:
                command = input(
                    "\nEnter command (example - SET key value, GET key, DELETE key, FLUSH, MSET key1=value1,key2=value2, MGET key1,key2): "
                ).strip()
                if command.lower() == 'bye':
                    break

                parts = command.split()

                if len(parts) == 0:
                    print("Error: Command cannot be empty.")
                    continue

                action = parts[0].upper()

                if action == 'SET':
                    if len(parts) != 3:
                        print("Error: SET command requires exactly 2 arguments (key and value).")
                        continue
                    key = parts[1]
                    value = parts[2]
                    response = self.send_request(action, key=key, value=value)

                elif action == 'GET':
                    if len(parts) != 2:
                        print("Error: GET command requires exactly 1 argument (key).")
                        continue
                    key = parts[1]
                    response = self.send_request(action, key=key)

                elif action == 'DELETE':
                    if len(parts) != 2:
                        print("Error: DELETE command requires exactly 1 argument (key).")
                        continue
                    key = parts[1]
                    response = self.send_request(action, key=key)

                elif action == 'FLUSH':
                    response = self.send_request(action)

                elif action == 'MSET':
                    if len(parts) != 2:
                        print("Error: MSET command requires 1 argument (key1=value1,key2=value2,...).")
                        continue
                    try:
                        items = dict(item.split('=') for item in parts[1].split(','))
                        response = self.send_request(action, items=items)
                    except ValueError:
                        print("Error: Invalid format for MSET. Use key=value pairs separated by commas.")
                        continue

                elif action == 'MGET':
                    if len(parts) != 2:
                        print("Error: MGET command requires 1 argument (key1,key2).")
                        continue
                    keys = parts[1].split(',')
                    response = self.send_request(action, keys=keys)

                else:
                    response = "Unknown command."

                print(f"Response: {response}")
            finally:
                self.run

if __name__ == '__main__':
    client = Client()
    client.run()
