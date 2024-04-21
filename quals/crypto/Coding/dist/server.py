#!/usr/local/bin/python

from secrets import randbelow
from numpy.linalg import matrix_rank
import numpy as np

FLAG = 'REDACTED'

n = 100
k = int(n * 2)
threshold = 0.05

M = []

def matrix_to_bits(G):
    return "".join([str(x) for x in G.flatten()])

def bits_to_matrix(s):
    assert len(s) == n * k
    return np.array([[int(s[i * k + j]) for j in range(k)] for i in range(n)]) % 2

def setupMatrix(G):
    assert G.shape == (n, k)
    global M

    perm = np.array([i for i in range(k)])
    np.random.shuffle(perm)
    PermMatrix = []
    for i in range(k):
        row = [0 for _ in range(k)]
        row[perm[i]] = 1
        PermMatrix.append(row)
    PermMatrix = np.array(PermMatrix)

    while True:
        S = np.array([[randbelow(2) for _ in range(n)] for i in range(n)])        
        if matrix_rank(S) == n:
            break

    M = (S @ G @ PermMatrix) % 2

def initialize():
    G = np.array([[randbelow(2) for _ in range(k)] for i in range(n)])
    setupMatrix(G)

def encrypt(m):
    original = (m @ M) % 2

    noise = [0 for _ in range(k)]
    for i in range(k):
        if randbelow(1000) < threshold * 1000:
            noise[i] = 1
    noise = np.array(noise)

    ciphertext = (original + noise) % 2
    return ciphertext

initialize()
print("M:", matrix_to_bits(M))

while True:
    '''
    0. Exit
    1. Set Matrix
    2. Encrypt (You can do this yourself honestly)
    3. Challenge
    '''
    option = int(input("Option: "))
    if (option == 0):
        exit(0)
    elif (option == 1):
        G = bits_to_matrix(input("G: ").strip()) % 2
        setupMatrix(G)
        print("M:", matrix_to_bits(M))
    elif (option == 2):
        m = np.array([randbelow(2) for _ in range(n)])
        print("m:", matrix_to_bits(m))
        print("c:", matrix_to_bits(encrypt(m)))
    elif (option == 3):
        count = 0
        for _ in range(200):
            print("Attempt:", _)
            challenge = np.array([randbelow(2) for _ in range(n)])
            check_arr = []
            print("c:", matrix_to_bits(encrypt(challenge)))
            for i in range(20):
                check = input("challenge: ").strip()
                check_arr.append(check)
            if matrix_to_bits(challenge) in check_arr:
                count += 1
                print("Correct!")
            else:
                print("Incorrect!")
        print(f"You got {count} out of 200")
        if (count >= 120):
            print("flag:", FLAG)
        else:
            print("Failed")
        exit(0)
    else:
        print("Invalid option")

