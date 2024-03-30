import socket
import re

def handle_connection(conn, addr):
    data = conn.recv(1024).decode('utf-8')
    print(data)
    pattern = re.compile(r'.*ping.*')
    matches = re.match(pattern, data)
    if matches:
        response = f"+PONG\r\n"
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