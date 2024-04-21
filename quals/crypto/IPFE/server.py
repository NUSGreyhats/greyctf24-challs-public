from IPFE import IPFE, _FeDDH_C
from secrets import randbits

FLAG = 'grey{catostrophic_failure_7eE37WLLdYgg}'

# Prime from generate_prime()
# To save server resource, we use a fix prime
p = 16288504871510480794324762135579703649765856535591342922567026227471362965149586884658054200933438380903297812918052138867605188042574409051996196359653039
q = (p - 1) // 2

n = 5
key = IPFE.generate(n, (p, q))
print("p:", key.p)
print("g:", key.g)
print("mpk:", list(map(int, key.mpk)))

while True:
    '''
    0. Exit
    1. Encrypt (You can do this yourself honestly)
    2. Generate Decryption Key
    3. Challenge
    '''
    option = int(input("Option: "))
    if (option == 0):
        exit(0)
    elif (option == 1):
        x = list(map(int, input("x: ").split()))
        c = IPFE.encrypt(x, key)
        print("g_r:", c.g_r)
        print("c:", list(map(int, c.c)))
    elif (option == 2):
        y = list(map(int, input("y: ").split()))
        g_r = int(input("g_r: "))
        dummy_c = _FeDDH_C(g_r, [])
        dk = IPFE.keygen(y, key, dummy_c)
        print("s_k:", int(dk.sk))
    elif (option == 3):
        challenge = [randbits(40) for _ in range(n)]
        c = IPFE.encrypt(challenge, key)
        print("g_r:", c.g_r)
        print("c:", list(map(int, c.c)))
        check = list(map(int, input("challenge: ").split()))
        if (len(check) == n and all([x == y for x, y in zip(challenge, check)])):
            print("flag:", FLAG)
        exit(0)