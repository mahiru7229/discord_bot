import os
import json
def prefix():
    """Return the prefix of the bot."""
    with open(os.path.join("code","commands","json","prefix.json"),"r") as f:
        prefix = json.loads(f.read())
    return prefix["prefix"]