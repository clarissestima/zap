import json
import os

CLIENT_DATA_FILE = 'client_data.json'

def load_client_data():
    if os.path.exists(CLIENT_DATA_FILE):
        with open(CLIENT_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}
    
def save_client_data(data):
    with open(CLIENT_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def save_client_id(client_id):
    data = load_client_data()
    if client_id not in data:
        data[client_id] = {
            "contacts": [],
            "groups": [],
            "messages": []
        }
    save_client_data(data)

def save_client_contacts(client_id, new_contact):
    data = load_client_data()
    if client_id in data:
        data[client_id]["contacts"].append(new_contact)
        save_client_data(data)

def save_client_groups(client_id, new_group):
    data = load_client_data()
    if client_id in data:
        data[client_id]["groups"].append(new_group)
        save_client_data(data)

def save_message_to_history(client_id, message):
    data = load_client_data()
    if client_id in data:
        data[client_id]["messages"].append(message)
        save_client_data(data)