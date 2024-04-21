from pwn import *
import base64


r = remote("localhost", 31114)
# r = process(["python3", "run.py"])

r.sendline(base64.b64encode(open("solve.v", "rb").read()))

r.interactive()
