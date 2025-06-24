import socket
import threading

# Set this to '127.0.0.1' if you're testing on the same machine,
# or to your local IP address if you're connecting from another device.
host = '0.0.0.0'
port = 55555

# Create socket and bind to host and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print(f"Server is listening on {host}:{port}")

clients = []
nicknames = []

# Send message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual client communication
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove disconnected client
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f"{nickname} left the chat!".encode('utf-8'))
                nicknames.remove(nickname)
                break

# Accept new connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("Nick".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to the server!".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
