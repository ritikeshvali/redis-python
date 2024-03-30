import socket
import re
import threading

def resp_parser(param):
    lines = param.split("\r\n")
    cnt = int(lines[0][1])
    vars = [lines[i] for i in range(2, len(lines), 2)]
    return vars

def resp_response(outp):
    return f"${len(outp)}\r\n{outp}\r\n"

def handle_connection(conn, addr, store):
    while True:
        request: bytes = conn.recv(1024)
        if not request:
            break
        data: str = request.decode()
        print(data)
        vars = resp_parser(data)
        print(vars)
        if vars[0]=="ping":
            response = "+PONG\r\n"
            print(response)
        elif vars[0] == "echo":
            response = "".join(vars[i] for i in range(1, len(vars)))
            response = resp_response(response)
        elif vars[0] == "set":
            store[vars[1]] = vars[2]
            response = f"+OK\r\n"
        elif vars[0] == "get":
            response = store[vars[1]]
            response = resp_response(response)
    conn.sendall(response.encode())
    conn.close()

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379))
    while True:
        store = {}
        client_socket, client_address = server_socket.accept()
        print(f"Received a connection from {client_address}")
        threading.Thread(target=handle_connection, args=[client_socket, client_address, store]).start()
        # handle_connection(client_socket, client_address)

if __name__ == "__main__":
    main()