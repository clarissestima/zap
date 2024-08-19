import socket
import json
import threading
from config import HOST, PORT
from storage import *

clients = {}

def handle_registration(client_socket):
    client_id = generate_unique_id()
    save_client_id(client_id)
    clients[client_id] = client_socket
    response = f"02{client_id}"
    client_socket.sendall(response.encode('utf-8'))
    print(f"Cliente registrado com ID: {client_id}")

def send_pending_messages(client_id, client_socket):
    messages = get_pending_messages(client_id)
    for message in messages:
        client_socket.sendall(message.encode('utf-8'))

    pending_messages = load_pending_messages()
    if client_id in pending_messages:
        del pending_messages[client_id]
        with open(PENDING_MESSAGES_FILE, 'w') as file:
            json.dump(pending_messages, file)

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            print(f"Dados recebidos: {data}")

            if data.startswith('01'):
                handle_registration(client_socket)
            
            elif data.startswith('03'):
                client_id = data[2:]
                if client_id in clients:
                    send_pending_messages(client_id, client_socket)
                else:
                    print("Cliente não registrado.")
            
            elif data.startswith('05'):
                src_id = data[2:15]
                dst_id = data[15:28]
                message = data[28:]
                
                if dst_id in clients:
                    clients[dst_id].sendall(data.encode('utf-8'))
                else:
                    save_pending_message(src_id, dst_id, data)
                    
    except Exception as e:
        print(f"Erro ao processar dados do cliente: {e}")
    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor iniciado em {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão recebida de {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()