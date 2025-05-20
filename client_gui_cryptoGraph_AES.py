import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")
        self.chat_box = scrolledtext.ScrolledText(root, width=60, height=20, bg="white", wrap=tk.WORD)
        self.chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5)

        self.send_button = tk.Button(root, text="Envoyer", width=10, command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10)

        self.HOST = '127.0.0.1'
        self.PORT = 65432
        self.key = b'mon_super_secret'
        self.start_client()

    def start_client(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

        thread = threading.Thread(target=self.receive_messages)
        thread.start()

    def receive_messages(self):
        while True:
            data = self.s.recv(1024)
            if not data:
                break
            decrypted_data = self.decrypt_message(data)
            self.chat_box.insert(tk.END, f"Serveur : {decrypted_data}\n")

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.chat_box.insert(tk.END, f"Moi : {message}\n")
            encrypted_message = self.encrypt_message(message)
            self.s.send(encrypted_message)
            self.message_entry.delete(0, tk.END)

    def encrypt_message(self, message):
        cipher = AES.new(self.key, AES.MODE_CBC)
        cipher_text = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + cipher_text

    def decrypt_message(self, cipher_text):
        iv = cipher_text[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(cipher_text[16:]), AES.block_size)
        return decrypted_data.decode()

# Lancement GUI
root = tk.Tk()
app = ClientGUI(root)
root.mainloop()
