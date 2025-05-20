import socket
import threading

# Fonction pour gérer la réception des messages du serveur
def receive_messages(s):
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(f"Données reçues du serveur : {data.decode()}")

# Configuration du client
HOST = '127.0.0.1'
PORT = 65432

# Création du socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Lancer un thread pour écouter les messages du serveur
thread = threading.Thread(target=receive_messages, args=(s,))
thread.start()

# Envoyer des messages
while True:
    message = input("Entrez le message à envoyer : ")
    s.send(message.encode())
