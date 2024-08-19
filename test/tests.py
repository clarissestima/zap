import socket
import time

def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 65432))  # Substitua pelo IP e porta corretos
    return sock

def send_message(sock, message):
    sock.sendall(message.encode('utf-8'))
    print(f"Mensagem enviada: {message}")

if __name__ == "__main__":
    sock = create_socket()
    try:
        send_message(sock, "01")  # Envia uma mensagem de registro
        time.sleep(1)  # Aguarda um pouco para garantir que a mensagem foi processada
    finally:
        sock.close()