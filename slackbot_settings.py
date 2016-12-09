import json

def get_config():
    """
    Returns the config, parsed from /config.json.
    """
    handle = open("config.json", "r")
    raw_json = handle.read()
    handle.close()
    return json.loads(raw_json)

# Set up initial config, mostly for the slackbot library.
config = get_config()
API_TOKEN = config["api_key"]
