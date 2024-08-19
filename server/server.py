import socket
import threading
from config import HOST, PORT
from storage import *

clients = {}
groups = {}

def handle_registration(client_socket):
    client_id = generate_unique_id()
    save_client_id(client_id)
    clients[client_id] = client_socket
    response = f"02{client_id}"
    client_socket.sendall(response.encode('utf-8'))
    print(f"Cliente registrado com ID: {client_id}")

def send_pending_messages(client_id, client_socket):
    messages = get_pending_messages(client_id)
    print(messages)
    for message in messages:
        print(message)
        client_socket.sendall(message.encode('utf-8'))

    pending_messages = load_pending_messages()
    if client_id in pending_messages:
        del pending_messages[client_id]
        with open(PENDING_MESSAGES_FILE, 'w') as file:
            json.dump(pending_messages, file)

def handle_group_creation(data):
    creator_id = data[2:15]
    timestamp = data[15:25]
    members = [data[i:i+13] for i in range(25, len(data), 13)]
    group_id = generate_unique_id()
    
    group_data = {
        "group_id": group_id,
        "creator_id": creator_id,
        "timestamp": timestamp,
        "members": members
    }
    save_group(group_data)
    groups[group_id] = group_data

    notification = f"11{group_id}{timestamp}{''.join(members)}"
    message = f"Bem-vindo ao grupo de {creator_id}"
    for member_id in members:
        if member_id in clients:
            clients[member_id].sendall(notification.encode('utf-8'))
        else:
            save_pending_message(creator_id, member_id, timestamp, message)

    print(f"Grupo criado com ID: {group_id}, membros: {members}")

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
                if client_exists(client_id):
                    send_pending_messages(client_id, client_socket)
                else:
                    print("Cliente não registrado.")
            
            elif data.startswith('05'):
                src_id = data[2:15]
                dst_id = data[15:28]
                timestamp = data[28:44]
                message = data[44:]
                
                print(src_id, dst_id, timestamp, message)

                if dst_id in clients:
                    message.sendall(data.encode('utf-8'))
                elif dst_id in groups:
                    for member_id in groups[dst_id][members]:
                        if member_id in clients:
                            member_id.sendall(notification.encode('utf-8'))
                        else:
                            save_pending_message(src_id, member_id, timestamp, message)
                else:
                    save_pending_message(src_id, dst_id, timestamp, message)

            elif data.startswith('08'):
                src_id = data[2:15]
                timestamp = data[15:]
                
                if client_exists(src_id):
                    notification = f'09{src_id}{timestamp}'
                    clients[src_id].sendall(notification.encode('utf-8'))
                    print(f"Notificação de leitura enviada para {src_id}")
            
            elif data.startswith('10'):
                handle_group_creation(data)

    except Exception as e:
        print(f"Erro ao processar dados do cliente: {e}")
    finally:
        client_socket.close()
        print("Soquete fechado.")

#def handle_message():

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor iniciado em {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão recebida de {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    main()