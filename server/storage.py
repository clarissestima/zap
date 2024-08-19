import random
import json
import os

PENDING_MESSAGES_FILE = 'pending_messages.json'
CLIENTS_FILE = 'clients.json'

def generate_unique_id():
    """Gera um ID único com 13 dígitos."""
    return ''.join([str(random.randint(0, 9)) for _ in range(13)])

def ensure_file_exists(filename):
    """Cria um arquivo vazio se ele não existir."""
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(json.dumps({}))

# Função para armazenar o identificador do cliente em um arquivo
def save_client_id(client_id):
    if os.path.exists('clients.json'):
        with open('clients.json', 'r') as file:
            clients_data = json.load(file)
    else:
        clients_data = {}

    clients_data[client_id] = {}
    
    with open('clients.json', 'w') as file:
        json.dump(clients_data, file)

def load_clients():
    """Carrega todos os IDs de clientes do arquivo JSON."""
    ensure_file_exists(CLIENTS_FILE)
    with open(CLIENTS_FILE, 'r') as file:
        return json.load(file)

def client_exists(client_id):
    """Verifica se o cliente já está registrado."""
    clients = load_clients()
    return client_id in clients

def load_pending_messages():
    """Carrega mensagens pendentes do arquivo JSON."""
    ensure_file_exists(PENDING_MESSAGES_FILE)
    with open(PENDING_MESSAGES_FILE, 'r') as file:
        return json.load(file)

def save_pending_message(src_id, dst_id, message):
    """Salva uma mensagem pendente no arquivo JSON."""
    pending_messages = load_pending_messages()

    if dst_id not in pending_messages:
        pending_messages[dst_id] = []

    pending_messages[dst_id].append(message)

    with open(PENDING_MESSAGES_FILE, 'w') as file:
        json.dump(pending_messages, file)

def get_pending_messages(client_id):
    """Obtém mensagens pendentes para um cliente específico."""
    pending_messages = load_pending_messages()
    return pending_messages.get(client_id, [])