import socket
import json

#starting your server
class Server:
    def __init__(self, host='127.0.0.1', port=31337): #loopback ip address - local host(specifically for testing connections - doesnt connect to outside internet - always refers to own device), #port - door that lets data in/out (can pick any number btw 1024-65535(0-1023 is reserved for system proc - http,ftp))
        self.store= {} #memory
        self.host= host
        self.port= port

# adding your methods and responses for clarity
    def set(self,key,value):
        self.store[key] = value
        return f'stored {key}'

    def get(self,key):
        return self.store.get(key,None)

    def delete(self,key):
        if key in self.store:
            del self.store[key]
            return f'deleted {key}'
        return f'key {key} does not exist'

    def flush(self):
        self.store.clear()
        return 'cleared all data ruh roh'

    def mget(self, keys):
        return {key: self.store.get(key) for key in keys}

    def mset(self,items):
        for key, value in items.items():
            self.store[key] = value
        return 'stored multiple values :O'

    def mdelete(self, keys):
        non_existent_keys = [key for key in keys if key not in self.store]
        if non_existent_keys:
            return f'keys {non_existent_keys} do not exist'
        for key in keys:
            del self.store[key]
        return f'deleted keys {keys}'

#here we have to manage said methods w a client socket in a server
    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode('utf-8') #decode to conv to string format(json) + serialization
        command = json.loads(request)
        #this takes a JSON-encoded string as i/p and parses it into a py obj (dict) , request has the raw data from socket AS a utf-8 encoded string, and command becomes our py dict

        if command['action'] == 'SET':
            response= self.set(command['key'], command['value'])
        elif command['action'] == 'GET':
            response = self.get(command['key'])
        elif command['action'] == 'DELETE':
            response= self.delete(command['key'])
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
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket obj, AF_INET - IPv4 protocol, sock_stream -  TCP protocol
        server_socket.bind((self.host, self.port)) #binds the socket to host and port to listen to incoming connections
        server_socket.listen(5)
        print(f'YAHOO server is running on {self.host}:{self.port}')

        while True: #logging(?) because will go insane otherwise
            client_socket,addr = server_socket.accept()
            print(f'connection from {addr}')
            self.handle_client(client_socket)

if __name__ == '__main__': #code only runs when script is executed directly, NOT IMPORTED
    server= Server()
    server.run()
