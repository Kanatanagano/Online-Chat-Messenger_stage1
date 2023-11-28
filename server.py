import socket
import threading
import time

class ChatServer:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        self.clients = {}

    def handle_client(self, message, client_address):
        username_len = message[0]
        username = message[1 : username_len + 1].decode('utf-8')
        user_message = message[username_len + 1 :].decode('utf-8')

        if client_address not in self.clients:
            self.clients[client_address] = {
                "username": username,
                "last_activity": time.time()
            }

        print(f"Received message from {username}: {user_message}")

        # Update last activity time
        self.clients[client_address]["last_activity"] = time.time()

        # Relay the message to all connected clients
        for addr in self.clients:
            if addr != client_address:
                self.server_socket.sendto(message, addr)

    def cleanup_inactive_clients(self):
        # Remove inactive clients
        current_time = time.time()
        inactive_clients = [addr for addr, info in self.clients.items() if current_time - info["last_activity"] > 60]  # 60 seconds inactivity timeout

        for addr in inactive_clients:
            del self.clients[addr]
            print(f"Client {self.clients[addr]['username']} at {addr} has been removed due to inactivity.")

    def start(self):
        print("Chat server is running...")
        while True:
            message, client_address = self.server_socket.recvfrom(4096)
            threading.Thread(target=self.handle_client, args=(message, client_address)).start()

            # Clean up inactive clients
            self.cleanup_inactive_clients()

if __name__ == "__main__":
    server = ChatServer('127.0.0.1', 12345)
    server.start()

