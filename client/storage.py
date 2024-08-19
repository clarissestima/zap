import json
import os

def load_client_data():
    if os.path.exists('client_data.json'):
        with open('client_data.json', 'r') as file:
            return json.load(file)
    return {
        "client_id": None,
        "contacts": [],
        "groups": [],
        "messages": []
    }

def save_client_data(data):
    with open('client_data.json', 'w') as file:
        json.dump(data, file)

def save_client_id(client_id):
    data = load_client_data()
    data["client_id"] = client_id
    save_client_data(data)

def save_client_contacts(new_contact):
    data = load_client_data()
    data["contacts"].append(new_contact)
    save_client_data(data)

def save_client_groups(new_group):
    data = load_client_data()
    data["groups"].append(new_group)
    save_client_data(data)

def save_message_to_history(message):
    data = load_client_data()
    data["messages"].append(message)
    save_client_data(data)