import os
import json
def prefix():
    with open(os.path.join("json","prefix.json"),"r") as f:
        prefix = json.loads(f.read())
    return prefix