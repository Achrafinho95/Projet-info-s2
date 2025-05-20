import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from queue import Queue

class Server:
    def __init__(self, root):
        self.root = root
        self.root.title("Serveur")
        self.message_queue = Queue()

        # Interface
        self.chat_box = scrolledtext.ScrolledText(root, width=60, height=20, bg="white", wrap=tk.WORD)
        self.chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5)

        self.send_button = tk.Button(root, text="Envoyer", width=10, command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10)

        self.clients = []

    def send_message(self):
        msg = self.message_entry.get()
        if msg:
            self.chat_box.insert(tk.END, f"Serveur : {msg}\n")
            for client in self.clients:
                client.send(msg.encode())
            self.message_entry.delete(0, tk.END)

    def handle_client(self, conn, addr):
        self.chat_box.insert(tk.END, f"[Connexion] Client {addr}\n")
        self.clients.append(conn)
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                message = f"[{addr}] {data.decode()}"
                self.message_queue.put(message)
            except:
                break
        conn.close()

    def start_server(self):
        HOST = "127.0.0.1"
        PORT = 65432
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        self.chat_box.insert(tk.END, f"Serveur en écoute sur {HOST}:{PORT}\n")

        def accept_clients():
            while True:
                conn, addr = server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()

        threading.Thread(target=accept_clients, daemon=True).start()

    def process_messages(self):
        while True:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                self.chat_box.insert(tk.END, message + "\n")

# Lancer l'application
root = tk.Tk()
app = Server(root)

# Thread de traitement des messages
threading.Thread(target=app.process_messages, daemon=True).start()

app.start_server()
root.mainloop()
