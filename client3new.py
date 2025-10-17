import socket
import json
import pickle
import dbm
import shelve
import sys
import base64

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
                
                request_message = json.dumps(request).encode('utf-8')
                client_socket.sendall(request_message)
                
                response_data = client_socket.recv(1024)
                
                response_str = response_data.decode('utf-8')
                return json.loads(response_str)
        
        except ConnectionRefusedError:
            return {'status': 'error', 'message': f'Connection refused. Is the server running on {self.host}:{self.port}?'}
        except json.JSONDecodeError:
            return {'status': 'error', 'message': f'Failed to decode JSON response: {response_str}'}
        except Exception as e:
            return {'status': 'error', 'message': f'An error occurred: {e}'}

    def run(self):
        print("Currently in client - enter 'bye' to quit.")
        print("Use SET key <text> to send binary data.")
        while True:
            command = input("\nEnter command (example - SET key value, GET key, DELETE key, FLUSH, MSET key1=value1,key2=value2, MGET key1,key2): ")
            if command.lower() == 'bye':
                break
            
            parts = command.split()
            if not parts:
                continue

            action = parts[0].upper()
            response = None

            try:
                if action == 'SET':
                    key = parts[1]
                    raw_binary_data = b'\x01\x02\x03' + parts[2].encode('utf-8')
                    encoded_value = base64.b64encode(raw_binary_data).decode('utf-8')
                    response = self.send_request('SET', key=key, value=encoded_value)
                elif action == 'GET':
                    key = parts[1]
                    response = self.send_request(action, key=key)
                elif action == 'DELETE':
                    key = parts[1]
                    response = self.send_request(action, key=key)
                elif action == 'FLUSH':
                    response = self.send_request(action)
                elif action == 'MSET':
                    items = dict(item.split('=', 1) for item in parts[1].split(','))
                    response = self.send_request(action, items=items)
                elif action == 'MGET':
                    keys = parts[1].split(',')
                    response = self.send_request(action, keys=keys)
                else:
                    response = {'status': 'error', 'message': f"Unknown command: {action}"}
            except IndexError:
                response = {'status': 'error', 'message': f"Missing arguments for command: {action}"}
            except Exception as e:
                response = {'status': 'error', 'message': f"Command processing error: {e}"}

            print(f'Response: {response}')

if __name__ == '__main__':
    client = Client()
    client.run()
