import socket
import threading
from config import HOST, PORT
from storage import *

clients = {}
groups = load_groups()

def handle_registration(client_socket):
    client_id = generate_unique_id()
    save_client_id(client_id)
    clients[client_id] = client_socket
    response = f"02{client_id}"
    client_socket.sendall(response.encode('utf-8'))
    print(f"Dados enviados: {response}")
    print(f"Cliente registrado com ID: {client_id}")

def send_pending_messages(client_id, client_socket):
    messages = get_pending_messages(client_id)
    for message in messages:
        msg = ''.join(message)
        client_socket.sendall(f'05{msg}'.encode('utf-8'))
        print(f"Dados enviados: {''.join(message)}")

    pending_messages = load_pending_messages()
    if client_id in pending_messages:
        del pending_messages[client_id]
        with open(PENDING_MESSAGES_FILE, 'w') as file:
            json.dump(pending_messages, file)

def handle_group_creation(data):
    group_id = generate_unique_id()
    creator_id = data[2:15]
    timestamp = data[15:31]
    members = [data[i:i+13] for i in range(31, len(data), 13)]
    
    group_data = {
        "group_id": group_id,
        "creator_id": creator_id,
        "timestamp": timestamp,
        "members": members
    }
    save_group(group_data)

    notification = f"11{group_id}{timestamp}{''.join(members)}"
    message = f"Bem-vindo ao grupo de {creator_id}"
    for member_id in members:
        if member_id in clients:
            clients[member_id].sendall(notification.encode('utf-8'))
            save_pending_message(creator_id, member_id, timestamp, message)
        else:
            save_pending_message(creator_id, member_id, timestamp, message)
    print(f"Grupo criado com ID: {group_id}, membros: {members}")

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print("Cliente desconectado.")
                break

            print(f"Dados recebidos: {data}")

            if data.startswith('01'):
                handle_registration(client_socket)
            elif data.startswith('03'):
                client_id = data[2:]
                if client_exists(client_id):
                    clients[client_id] = client_socket
                    send_pending_messages(client_id, client_socket)
                else:
                    print("Cliente não registrado.")
            elif data.startswith('05'):
                src_id = data[2:15]
                dst_id = data[15:28]
                timestamp = data[28:44]
                message = data[44:]
                
                if dst_id in clients:
                    try:
                        clients[dst_id].sendall(data.encode('utf-8'))
                        print(f"Dados enviados: {data}")
                    except OSError as e:
                        print(f"Erro ao enviar mensagem para o cliente {dst_id}: {e}")
                        save_pending_message(src_id, dst_id, timestamp, message)
                elif dst_id in groups:
                    for member in groups[dst_id]["members"]:
                        if member in clients:
                            try:
                                clients[member].sendall(data.encode('utf-8'))
                                print(f"Dados enviados: {data}")
                            except OSError as e:
                                print(f"Erro ao enviar mensagem para o cliente {member}: {e}")
                                save_pending_message(src_id, member, timestamp, message)
                        else:
                            print(f"Mensagem para {member} salva em mensagens pendentes.")
                            save_pending_message(src_id, member, timestamp, message)
                else:
                    print(f"Cliente {dst_id} não está conectado. Salvando mensagem.")
                    save_pending_message(src_id, dst_id, timestamp, message)
            elif data.startswith('08'):
                dst_id = data[2:15]
                src_id = data[15:28]
                timestamp = data[28:]
                message = f"Sua mensagem para {src_id} foi lida."

                if dst_id in clients:
                    try:
                        notification = f'09{src_id}{timestamp}'
                        clients[dst_id].sendall(notification.encode('utf-8'))
                        print(f"Dados enviados: {notification}")
                        print(f"Notificação de leitura enviada para {dst_id}")
                    except OSError as e:
                        print(f"Erro ao enviar notificação para {dst_id}: {e}")
                        save_pending_message("0000000000000", dst_id, timestamp, message)
                else:
                    print(f"Cliente {dst_id} não está conectado. Salvando notificação em pending_messages.")
                    save_pending_message("0000000000000", dst_id, timestamp, message)

            elif data.startswith('10'):
                handle_group_creation(data)

    except ConnectionResetError as e:
        print(f"Erro de conexão: {e}")
    finally:
        if client_socket:
            client_socket.close()
            print("Soquete fechado.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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