import json

def get_config():
    handle = open("config.json", "r")
    raw_json = handle.read()
    handle.close()
    return json.loads(raw_json)

config = get_config()
API_TOKEN = config["api_key"]
