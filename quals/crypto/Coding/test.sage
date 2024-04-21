from secrets import randbelow
import numpy as np
from ldpc import bp_decoder, code_util
from sage.coding.information_set_decoder import LeeBrickellISDAlgorithm
import random

n = 100
k = int(n * 2)
threshold = 0.05
tt = 6
arr = [1] * tt + [0] * (k - tt)

H = []

for i in range(k - n):
    temp = []
    random.shuffle(arr)
    H.append(arr.copy())

H = np.array(H)
G = code_util.construct_generator_matrix(H)

G = G.transpose()
np.random.shuffle(G)
G = G.transpose()

np.random.shuffle(G)

C = LinearCode(Matrix(GF(2), G))
H = C.parity_check_matrix().change_ring(ZZ).LLL().change_ring(GF(2)).numpy(dtype=int)

bpd=bp_decoder(
    H, #the parity check matrix
    error_rate=threshold, # the error rate on each bit
    max_iter=100000, #the maximum iteration depth for BP
    bp_method="product_sum", #BP method. The other option is `minimum_sum'
    channel_probs=[None] #channel probability probabilities. Will overide error rate.
)

# Weight 1

dic = {}

error = np.zeros(k,dtype=int)
key = tuple(list(H @ error.transpose() % 2))
dic[key] = [error]

for i in range(k):
    error = np.zeros(k,dtype=int)
    error[i] = 1
    key = tuple(list(H @ error.transpose() % 2))
    if (key not in dic):
        dic[key] = []
    dic[key].append(error)

# Weight 2

for i in range(k):
    for j in range(i + 1, k):
        error = np.zeros(k,dtype=int)
        error[i] = 1
        error[j] = 1
        key = tuple(list(H @ error.transpose() % 2))
        if (key not in dic):
            dic[key] = []
        dic[key].append(error)

# Weight 3

for i in range(k):
    for j in range(i + 1, k):
        for l in range(j + 1, k):
            error = np.zeros(k,dtype=int)
            error[i] = 1
            error[j] = 1
            error[l] = 1
            key = tuple(list(H @ error.transpose() % 2))
            if (key not in dic):
                dic[key] = []
            dic[key].append(error)

count = 0
for _ in range(100):

    m = [randbelow(2) for _ in range(n)]
    m = np.array(m)

    original = m @ G % 2

    noise = [0 for _ in range(k)]

    for i in range(k):
        if (randbelow(1000) / 1000) < threshold:
            noise[i] = 1

    noise = np.array(noise)

    print(sum(noise))

    encoded = (original + noise) % 2

    decoded_codeword = bpd.decode(encoded)

    print(sum(decoded_codeword != original))

    key = tuple(list(H @ decoded_codeword.transpose() % 2))

    if (key in dic):
        ttt = 0
        for i in range(len(dic[key])):
            temp = (decoded_codeword + dic[key][i]) % 2
            try:
                guess = Matrix(GF(2), G).solve_left(vector(GF(2), temp))
                ttt += 1
                if (vector(GF(2), m) == guess):
                    count += 1
                    print("Success", ttt)
                    break
            except KeyboardInterrupt:
                exit()
            except:
                pass
            
        else:
            print("Failure")
    else:
        print("Failure")
    
print(count/100)
