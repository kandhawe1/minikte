import json

def load_credentials(broker_name):
    with open("config/credentials.json") as f:
        data = json.load(f)

    return data.get(broker_name)