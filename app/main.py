import socket
import re
import threading

def handle_connection(conn, addr):
    while True:
        request: bytes = conn.recv(1024)
        if not request:
            break
        data: str = request.decode()
        print(data)
        if "ping" in data.lower():
            response = "+PONG\r\n"
            print(response)
            conn.send(response.encode())
        elif "echo" in data.lower():
            elements = data.split("\r\n")
            index = int(elements[0][1])-1
            str_idx=4
            response = ""
            while index>0:
                response += elements[str_idx]
                str_idx+=2
                index-=1
            response = f"${len(response)}\r\n{response}\r\n"
            conn.send(response.encode())
    conn.close()

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379))
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Received a connection from {client_address}")
        threading.Thread(target=handle_connection, args=[client_socket, client_address]).start()
        # handle_connection(client_socket, client_address)

if __name__ == "__main__":
    main()