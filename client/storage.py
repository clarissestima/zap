import json
import os

# Função para carregar dados persistentes do cliente
def load_client_data():
    if os.path.exists('client_data.json'):
        with open('client_data.json', 'r') as file:
            return json.load(file)
    return {
        "client_id": None,
        "contacts": {},
        "groups": {},
        "messages": []
    }

# Função para salvar dados do cliente
def save_client_data(data):
    with open('client_data.json', 'w') as file:
        json.dump(data, file)

# Função para armazenar o identificador do cliente
def save_client_id(client_id):
    data = load_client_data()
    data["client_id"] = client_id
    save_client_data(data)

# Função para adicionar mensagem ao histórico
def save_message_to_history(message):
    data = load_client_data()
    data["messages"].append(message)
    save_client_data(data)