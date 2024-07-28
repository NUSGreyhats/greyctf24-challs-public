from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from binascii import crc32
import os

with open("flag.txt", "r") as f:
    flag = f.read().encode()

def CRC32(x):
    return int.to_bytes(crc32(x), 4, 'big')

key = os.urandom(16)
iv = os.urandom(8)
num_encryptions = 0

def encrypt(pt):
    global num_encryptions
    num_encryptions += 1
    if (num_encryptions > 200):
        # no more for you...
        return b""

    cipher = AES.new(key, mode=AES.MODE_CTR, nonce=iv)
    hmac = CRC32(key + pt + key)
    ct = cipher.encrypt(pad(pt + hmac, 16))
    return ct

def decrypt(ct):
    cipher = AES.new(key, mode=AES.MODE_CTR, nonce=iv)
    tmp = unpad(cipher.decrypt(ct), 16)
    pt, hmac_check = tmp[:-4], tmp[-4:]

    hmac = CRC32(key + pt + key)
    if (hmac_check == hmac):
        return pt

    return None

menu = """
Enter an option:
[1] Encrypt message
[2] Challenge
[3] Exit
> """

while True:
    option = input(menu).strip()
    
    if option == "1":

        message = input("Enter a message (in hex): ")
        try:
            message = bytes.fromhex(message)
            enc = encrypt(message)
            print(enc.hex())
            
        except Exception as e:
            print("Error!", e)
            exit(0)
        
        
    elif option == "2":

        for i in range(10):
            test = os.urandom(16)
            print(f"Encrypt {test.hex()}")

            enc = input("Answer (in hex): ")
            enc = bytes.fromhex(enc)
            
            if test != decrypt(enc):
                print("You failed!")
                exit(0)

        print(f"Wow! Here's the flag: {flag}")
            

    else:
        exit(0)
        
                      
