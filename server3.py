import socket
import json
import os

class Server:
    def __init__(self, host='127.0.0.1', port=31337, data_file='store.json'):
        self.store = {}
        self.host = host
        self.port = port
        self.data_file = data_file
        self.load_store()

    # on startup it runs
    def load_store(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.store = json.load(f)
        else:
            self.store = {}

    # just run after every command
    def save_store(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.store, f)

    def set(self, key, value):
        self.store[key] = value
        self.save_store()
        return f'stored {key}'

    def get(self, key):
        return self.store.get(key, None)

    def delete(self, key):
        if key in self.store:
            del self.store[key]
            self.save_store()
            return f'deleted {key}'
        return None

    def flush(self):
        self.store.clear()
        self.save_store()
        return 'cleared all data ruh roh'

    def mget(self, keys):
        return {key: self.store.get(key) for key in keys}

    def mset(self, items):
        for key, value in items.items():
            self.store[key] = value
        self.save_store()
        return 'stored multiple values :O'

    def mdelete(self, keys):
        if keys is None:
            return "no keys to delete"
        deleted_keys = []
        non_existent_keys = []
        for key in keys:
            if key in self.store:
                del self.store[key]
                deleted_keys.append(key)
            else:
                non_existent_keys.append(key)
        self.save_store()
        return {'deleted_keys': deleted_keys, 'non_existent_keys': non_existent_keys}

    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        command = json.loads(request)

        if command['action'] == 'SET':
            response = self.set(command['key'], command['value'])
        elif command['action'] == 'GET':
            response = self.get(command['key'])
        elif command['action'] == 'DELETE':
            response = self.delete(command['key'])
        elif command['action'] == 'FLUSH':
            response = self.flush()
        elif command['action'] == 'MGET':
            response = self.mget(command['keys'])
        elif command['action'] == 'MSET':
            response = self.mset(command['items'])
        elif command['action'] == 'MDELETE':
            response = self.mdelete(command['keys'])
        else:
            response = 'unknown command pls try again'

        client_socket.send(json.dumps(response).encode('utf-8'))
        client_socket.close()

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f'YAHOO server is running on {self.host}:{self.port}')

        while True:
            client_socket, addr = server_socket.accept()
            print(f'connection from {addr}')
            self.handle_client(client_socket)

if __name__ == '__main__':
    server = Server()
    server.run()
