import socket
import threading

class ChatClient:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, 32973))
        print("Connected to the server.")

        # Create thread for receiving messages
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        #Call Send message function
        self.send_messages()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                print("Received:", message)
            except Exception as e:
                print("Server connection closed.")
                break

    def send_messages(self):
        while True:
            message = input("Enter a message: ")
            self.client_socket.send(message.encode('utf-8'))

        self.client_socket.close()

if __name__ == "__main__":
    
    chat_client = ChatClient("35.208.151.24") #Server IP address
    chat_client.start()
