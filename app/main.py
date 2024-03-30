import socket
import threading
from datetime import datetime

def resp_parser(param):
    lines = param.split("\r\n")
    vars = [lines[i] for i in range(2, len(lines), 2)]
    return vars

def resp_response(outp):
    return f"${len(outp)}\r\n{outp}\r\n"

def handle_connection(conn, addr, store):
    output_format = "%Y-%m-%d %H:%M:%S"
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
            conn.send(response.encode())
        elif vars[0] == "echo":
            response = "".join(vars[i] for i in range(1, len(vars)))
            response = resp_response(response)
            conn.send(response.encode())
        elif vars[0] == "set":
            if len(vars) == 5:
                date_string = datetime.now().strftime(output_format)
                store[vars[1]] = vars[2] + f"|time->{date_string}->" + vars[4]
            else:
            # no expiry time
                store[vars[1]] = vars[2] + "|-1"
            print(store[vars[1]])
            response = f"+OK\r\n"
            conn.send(response.encode())
        elif vars[0] == "get":
            response = store[vars[1]]
            if "|-1" in response:
            # no expiry time
                response = resp_response(response.split("|")[0])
            else:
                milisecs = int(response.split("|")[1].split("->")[2])
                time = datetime.strptime(response.split("|")[1].split("->")[1], output_format)
                if int((datetime.now() - time).total_seconds()*1000) > milisecs:
                    response = "$-1\r\n"
                else:
                    response = resp_response(response.split("|")[0])
            conn.send(response.encode())
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