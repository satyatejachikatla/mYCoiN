from .__init__ import *


def calculateHash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def debug_print(*args, **kwargs):
    if DEBUG_ENABLE:
        print(*args, **kwargs)

def print_json(data:str)->str:
    print(json.dumps(json.loads(data),indent=4))
