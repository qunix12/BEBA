import socket
import threading

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            broadcast(data, client_socket)
        except:
            break
    client_socket.close()
    if client_socket in clients:
        clients.remove(client_socket)

def start_server(host='localhost', port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Сервер запущено на {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"Підключено: {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
