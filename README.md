# simple-redis-in-py

# Simple Redis-like TCP Server

## Requirements

- Python 3.x
- Modules: `socket` and `json` (both are part of Python’s standard library)

## How to Run

1. **Start the Server**:
   - Open a terminal and run the server:

     ```bash
     python server3.py
     ```

2. **Run the Client**:
   - Open another terminal and run the client to send commands to the server:

     ```bash
     python client3.py
     ```

## Storage

The server stores key-value pairs in memory using a Python dictionary. Commands like `SET`, `GET`, `DELETE`, and `MSET` allow you to manipulate and retrieve stored data. All stored data is volatile and will be lost when the server is restarted.

## Communication

The client and server communicate via a TCP connection using JSON-formatted strings. The client sends commands to the server in JSON format, and the server responds in JSON as well. This makes the protocol easy to understand and extend for various actions like `SET`, `GET`, `DELETE`, `FLUSH`, `MSET`, and `MGET`.
