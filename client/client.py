import socket
import time
from datetime import datetime
import threading
from config import SERVER_HOST, SERVER_PORT
from storage import *

def register_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = '01'
        client_socket.sendall(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        if response.startswith('02'):
            client_id = response[2:]
            save_client_id(client_id)
            print(f'Registrado com sucesso. ID do cliente: {client_id}')
        else:
            print('Falha ao registrar o cliente.')

def connect_client():
    client_data = load_client_data()
    client_id = input("Digite seu ID para se conectar: ")
    if client_id not in client_data:
        print("Cliente não registrado. Registre-se primeiro.")
        return

    print(f"Conectado como: {client_id}")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    message = f'03{client_id}'
    client_socket.sendall(message.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_id))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        print("\nMenu:")
        print("1. Enviar mensagem")
        print("2. Adicionar contato")
        print("3. Criar grupo")
        print("4. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            dst_id = input("ID do destinatário: ")
            message = input("Digite sua mensagem: ")
            send_message(client_socket, client_id, dst_id, message)
        elif choice == '2':
            add_contact(client_id)
        elif choice == '3':
            create_group(client_id)
        elif choice == '4':
            client_socket.close()
            break
        else:
            print("Opção inválida.")

def send_message(client_socket, src_id, dst_id, data):
    timestamp = str(datetime.now().strftime("%d/%m/%Y;%H:%M"))
    message = f'05{src_id}{dst_id}{timestamp}{data}'
    client_socket.sendall(message.encode('utf-8'))
    print('Mensagem enviada com sucesso.')

def receive_messages(client_socket, client_id):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Conexão com o servidor perdida.")
                break
            print(f'Mensagem recebida: {message}')
            save_message_to_history(client_id, message)
        except socket.error as e:
            print(f"Erro ao receber mensagem: {e}")
            break

def confirm_read(client_id, timestamp):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = f'08{client_id}{timestamp}'
        client_socket.sendall(message.encode('utf-8'))
        print('Confirmação de leitura enviada.')

def handle_message(message, client_id):
    print(f"Nova mensagem: {message}")

    src_id = message[2:15]
    timestamp = message[28:38]
    confirm_read(client_id, timestamp)

def add_contact(client_id):
    contact_id = input("Id do usuário que você gostaria de adicionar aos seus contatos: ")
    save_client_contacts(client_id, contact_id)

def create_group(client_id):
    members = [client_id]
    for _ in range(7):
        member_id = input("Digite o ID de um membro: ")
        if member_id:
            members.append(member_id)
        else:
            break
    
    save_client_groups(client_id, members)

    timestamp = str(int(time.time()))
    group_message = f'10{client_id}{timestamp}{"".join(members)}'
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.sendall(group_message.encode('utf-8'))
        print('Solicitação de criação de grupo enviada.')

def main():
    while True:
        print("\nMenu:")
        print("1. Registrar cliente")
        print("2. Conectar cliente")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            register_client()
        elif choice == '2':
            connect_client()
        elif choice == '3':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()