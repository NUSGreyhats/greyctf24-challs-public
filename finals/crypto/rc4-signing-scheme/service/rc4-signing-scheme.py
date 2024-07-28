import os

with open("flag.txt", "r") as f:
    flag = f.read().encode()

def keyschedule(key):
    S = list(range(256))
    j = 0
    for i in range(256):
         j = (j + S[i] + key[i%len(key)])%256
         t = S[i]
         S[i] = S[j]
         S[j] = t
    return S

def encrypt(S, pt):
    ct = bytes([])
    i = 0
    j = 0
    for x in pt:
        i = (i+1)%256
        j = (j+S[i])%256
        t = S[i]
        S[i] = S[j]
        S[j] = t
        t = (S[i] + S[j])%256
        ct += bytes([S[t] ^ x])
    return ct

def sign(msg):

    global num_encryptions
    num_encryptions += 1
    if (num_encryptions > 20):
        # no more for you...
        return b""
    
    iv = os.urandom(128)
    USED_IVS.append(iv)
    key = iv + priv_key
    S = keyschedule(key)
    ct = encrypt(S, msg)
    return iv + ct

def verify(msg, sig):

    iv, ct = sig[:128], sig[128:]
    
    if iv in USED_IVS:
        # thats too easy...
        return False

    key = iv + priv_key
    S = keyschedule(key)
    pt = encrypt(S, ct)
    return msg == pt

menu = """
Enter an option:
[1] Sign secret
[2] Submit signature
[3] Exit
> """

num_encryptions = 0
USED_IVS = []
priv_key = os.urandom(128)
secret_msg = os.urandom(256)

while True:
    option = input(menu).strip()

    if option == "1":

        sig = sign(secret_msg)
        
        print(sig.hex())
                    
    elif option == "2":

        sig = bytes.fromhex(input("Signature (hex): "))
        
        if verify(secret_msg, sig):
            print(f"Wow! Here's the flag: {flag}")
            
        else:
            print("Wrong...")
            
    else:
        exit(0)




    
