import socket
import threading

class Server:
    def __init__(self):
        self.server_socket = None
        self.client_sockets = []

    def start(self, ip_address):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip_address, 8000))
        self.server_socket.listen(5)

        print(f"Server started. Listening for connections on {ip_address}...")

        while True:
            client_socket, address = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print(f"Client connected: {address}")

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def stop(self):
        for client_socket in self.client_sockets:
            client_socket.close()

        if self.server_socket:
            self.server_socket.close()

        print("Server stopped.")

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    self.broadcast_message(message, client_socket)
            except Exception as e:
                print(f"Client disconnected: {client_socket.getpeername()}")
                self.client_sockets.remove(client_socket)
                client_socket.close()
                break

    def broadcast_message(self, message, sender_socket):
        for client_socket in self.client_sockets:
            if client_socket != sender_socket:
                client_socket.send(message.encode('utf-8'))
        print("Sent:", message)

if __name__ == "__main__":
    server = Server()
    server.start("0.0.0.0")  # Replace with the server's IP address
