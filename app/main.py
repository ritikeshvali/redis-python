import socket
import re

def handle_connection(conn, addr):
    while True:
        request: bytes = conn.recv(1024)
        if not request:
            break
        data: str = request.decode()
        if "ping" in data.lower():
            response = "+PONG\r\n"
            print(response)
            conn.send(response.encode())
    conn.close()

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379))
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Received a connection from {client_address}")
        handle_connection(client_socket, client_address)

if __name__ == "__main__":
    main()