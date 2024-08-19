import socket
import time
import threading
from config import SERVER_HOST, SERVER_PORT
from storage import *

# Função para registrar o cliente no servidor
def register_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = '01'  # Código de registro
        client_socket.sendall(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        if response.startswith('02'):
            client_id = response[2:]
            save_client_id(client_id)
            print(f'Registrado com sucesso. ID do cliente: {client_id}')
        else:
            print('Falha ao registrar o cliente.')

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if not response:
                print("Conexão com o servidor perdida.")
                break
            print(f'Mensagem recebida: {response}')
            save_message_to_history(response)
        except socket.error as e:
            print(f"Erro ao receber mensagem: {e}")
            break
    client_socket.close()

# Função para conectar o cliente ao servidor
def connect_client():
    client_data = load_client_data()
    client_id = client_data.get("client_id")
    if not client_id:
        print("Cliente não registrado. Registre-se primeiro.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = f'03{client_id}'  # Código de conexão
        client_socket.sendall(message.encode('utf-8'))

        # Iniciar uma thread para receber mensagens
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

        # Interagir com o menu enquanto recebe mensagens
        while True:
            print("\nMenu:")
            print("1. Enviar mensagem")
            print("2. Sair")
            choice = input("Escolha uma opção: ")

            if choice == '1':
                dst_id = input("ID do destinatário: ")
                message = input("Digite sua mensagem: ")
                send_message(dst_id, message)
            elif choice == '2':
                break
            else:
                print("Opção inválida.")

# Função para enviar uma mensagem para outro cliente
def send_message(dst_id, data):
    client_data = load_client_data()
    src_id = client_data.get("client_id")
    if not src_id:
        print("Cliente não registrado. Registre-se primeiro.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        timestamp = str(int(time.time()))
        message = f'05{src_id}{dst_id}{timestamp}{data}'
        client_socket.sendall(message.encode('utf-8'))
        print('Mensagem enviada com sucesso.')

# Função principal para interação do cliente
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