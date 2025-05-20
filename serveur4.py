import socket
import threading

# Liste pour stocker les connexions clients
clients = []

# Fonction pour gérer la réception des messages du client
def handle_client(conn, addr):
    print(f"Connecté par {addr}")
    clients.append(conn)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Données reçues du client {addr}: {data.decode()}")

        # Transmettre le message à tous les clients connectés
        for client in clients:
            if client != conn:
                try:
                    client.send(data)
                except:
                    pass

# Configuration du serveur
host = "127.0.0.1"
port = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print(f"Serveur en écoute sur {host}:{port}")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()