from pwn import *
import time
import random

p = remote("localhost", 31111)
random.seed(int(time.time()))

n = random.randint(1000000000000000, 10000000000000000-1)
p.sendline(str(n).encode())

p.interactive()
