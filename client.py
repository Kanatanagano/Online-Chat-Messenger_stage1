import socket

class ChatClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (host, port)
        self.username = input("Enter your username: ")

    def send_message(self, message):
        encoded_message = bytes([len(self.username)]) + self.username.encode('utf-8') + message.encode('utf-8')
        self.client_socket.sendto(encoded_message, self.server_address)

    def start(self):
        print("Chat client is running...")
        while True:
            user_message = input("Enter your message: ")
            self.send_message(user_message)

if __name__ == "__main__":
    client = ChatClient('127.0.0.1', 12345)
    client.start()


    