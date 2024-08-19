import socket
import json
from config import HOST, PORT
from storage import generate_unique_id, save_client_id, get_pending_messages, save_pending_message

clients = {}

# Função para lidar com o registro de clientes
def handle_registration(client_socket):
    client_id = generate_unique_id()
    clients[client_id] = client_socket
    response = f"02{client_id}"
    client_socket.sendall(response.encode('utf-8'))
    print(f"Cliente registrado com ID: {client_id}")

# Função para enviar mensagens pendentes a um cliente
def send_pending_messages(client_id, client_socket):
    messages = get_pending_messages(client_id)
    for message in messages:
        client_socket.sendall(message.encode('utf-8'))
    # Limpar mensagens pendentes após o envio
    with open('pending_messages.json', 'r') as file:
        pending_messages = json.load(file)
    if client_id in pending_messages:
        del pending_messages[client_id]
    with open('pending_messages.json', 'w') as file:
        json.dump(pending_messages, file)

# Função para lidar com mensagens recebidas de clientes
def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode('utf-8')
        
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
        
        # Adicione tratamento para outros tipos de mensagens...
    
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
        handle_client(client_socket)

if __name__ == "__main__":
    main()