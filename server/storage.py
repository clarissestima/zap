import random
import json
import os

PENDING_MESSAGES_FILE = 'pending_messages.json'
CLIENTS_FILE = 'clients.json'
GROUPS_FILE = 'groups.json'

def generate_unique_id():
    return ''.join([str(random.randint(0, 9)) for _ in range(13)])

def ensure_file_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(json.dumps({}))

def save_client_id(client_id):
    if os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, 'r') as file:
            clients_data = json.load(file)
    else:
        clients_data = {}

    clients_data[client_id] = {}
    
    with open(CLIENTS_FILE, 'w') as file:
        json.dump(clients_data, file)

def save_group(group_data):
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, 'r') as file:
            groups_data = json.load(file)
    else:
        groups_data = {}

    groups_data[group_data["group_id"]] = group_data
    
    with open(GROUPS_FILE, 'w') as file:
        json.dump(groups_data, file)

def load_clients():
    ensure_file_exists(CLIENTS_FILE)
    with open(CLIENTS_FILE, 'r') as file:
        return json.load(file)

def client_exists(client_id):
    clients = load_clients()
    return client_id in clients

def load_pending_messages():
    ensure_file_exists(PENDING_MESSAGES_FILE)
    with open(PENDING_MESSAGES_FILE, 'r') as file:
        return json.load(file)

def save_pending_message(src_id, dst_id, timestamp, message):
    pending_messages = load_pending_messages()

    if dst_id not in pending_messages:
        pending_messages[dst_id] = []

    pending_messages[dst_id].append(message)
    
    with open(PENDING_MESSAGES_FILE, 'w') as file:
        json.dump(pending_messages, file)

def get_pending_messages(client_id):
    pending_messages = load_pending_messages()
    return pending_messages.get(client_id, [])