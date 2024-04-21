#!/usr/local/bin/python

from secrets import token_bytes
from aes import AES

FLAG = 'grey{mix_column_is_important_in_AES_ExB3Hf9q9I3m}'
password = token_bytes(16)
key = token_bytes(16)

AES = AES(key)
m = bytes.fromhex(input("m: "))
if (len(m) > 4096): exit(0)
print("c:", AES.encrypt(m).hex())

print("c_p:", AES.encrypt(password).hex())
check = input("password: ")
if check == password.hex():
    print('flag:', FLAG)