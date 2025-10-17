import socket
import json

class Client:
    def __init__(self,host='127.0.0.1', port=31337):
        self.host= host
        self.port= port

    def send_request(self,action, key=None, value=None, keys=None, items=None, expiry = None):
        request = {'action': action} 
        if key is not None:
            request['key'] = key
        if value is not None:
            request['value'] = value
        if keys is not None:
            request['keys'] = keys
        if items is not None:
            request['items']= items
        if expiry is not None:
            request['expiry'] = expiry

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.send(json.dumps(request).encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            return json.loads(response)

    def run(self):
        print("currently in client - enter 'bye' to quit:c")
        while True:
            command = input("\nenter command (example - SET key value, GET key, DELETE key, FLUSH, MSET key1=value1,key2=value2, MGET key1,key2): ")
            if command.lower()== 'bye':
                break
            
            parts = command.split()
            action= parts[0].upper()

            if action == 'SET':

                if len(parts) < 3:
                    print("Error: SET requires at least key and value")
            
                expiry = None
                key= parts[1]
                value = parts[2]

                if len(parts) > 3:
                    if parts[3].upper() == 'EX':
                        if len(parts) != 5:
                            print("Error: EX requires seconds parameter")
                            continue
                        try:
                            expiry = int(parts[4])
                        except ValueError:
                            print("Error: EX seconds must be an integer")
                            continue
                    else: print("Please enter EX to implement expiry")

                response = self.send_request(action,key=key, value=value, expiry=expiry)

                
            elif action == 'GET':
                key = parts[1]
                response = self.send_request(action,key=key)
            elif action == 'DELETE':
                key= parts[1]
                response = self.send_request(action, key=key)
            elif action == 'FLUSH':
                response = self.send_request(action)
            elif action== 'MSET':
                items = dict(item.split('=') for item in parts[1].split(','))
                response = self.send_request(action,items=items)
            elif action == 'MGET':
                keys = parts[1].split(',')
                response = self.send_request(action,keys=keys)
            else:
                response= 'Unknown command'

            print(f'response: {response}')

if __name__ == '__main__':
    client= Client()
    client.run()
