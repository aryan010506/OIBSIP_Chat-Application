import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def start_server():
    server_socket.bind(('localhost', 5560)) 
    server_socket.listen(1)
    global conn  # Make conn accessible in send()
    conn, addr = server_socket.accept()
    chat_log.insert(tk.END, f"Connected to {addr}\n")

    def receive():
        while True:
            try:
                msg = conn.recv(1024).decode()
                if msg:
                    chat_log.insert(tk.END, f"Client: {msg}\n")
            except:
                break

    threading.Thread(target=receive, daemon=True).start()

def send():
    msg = msg_entry.get()
    chat_log.insert(tk.END, f"You: {msg}\n")
    try:
        conn.send(msg.encode())
    except:
        chat_log.insert(tk.END, "Failed to send message.\n")
    msg_entry.delete(0, tk.END)

# GUI
app = tk.Tk()
app.title("Server Chat")
app.geometry("400x400")

chat_log = scrolledtext.ScrolledText(app)
chat_log.pack(pady=10, fill=tk.BOTH, expand=True)

msg_entry = tk.Entry(app)
msg_entry.pack(fill=tk.X, padx=5, pady=5)

send_btn = tk.Button(app, text="Send", command=send)
send_btn.pack(pady=5)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = None  # Declare conn globally

threading.Thread(target=start_server, daemon=True).start()

app.mainloop()
