import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start_client():
    client_socket.connect(('localhost', 5560))
    chat_log.insert(tk.END, "Connected to server.\n")

    def receive():
        while True:
            try:
                msg = client_socket.recv(1024).decode()
                if msg:
                    chat_log.insert(tk.END, f"Server: {msg}\n")
            except:
                break

    threading.Thread(target=receive, daemon=True).start()

    def send():
        msg = msg_entry.get()
        chat_log.insert(tk.END, f"You: {msg}\n")
        client_socket.send(msg.encode())
        msg_entry.delete(0, tk.END)

    send_btn.config(command=send)

# GUI
app = tk.Tk()
app.title("Client Chat")
app.geometry("400x400")

chat_log = scrolledtext.ScrolledText(app)
chat_log.pack(pady=10, fill=tk.BOTH, expand=True)

msg_entry = tk.Entry(app)
msg_entry.pack(fill=tk.X, padx=5, pady=5)

send_btn = tk.Button(app, text="Send")
send_btn.pack(pady=5)

threading.Thread(target=start_client, daemon=True).start()

app.mainloop()
