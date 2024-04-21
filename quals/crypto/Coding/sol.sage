from pwn import *
import numpy as np
from ldpc import bp_decoder, code_util


def matrix_to_bits(G):
    return "".join([str(x) for x in G.flatten()])

def bits_to_matrix(s):
    return np.array([[int(s[i * k + j]) for j in range(k)] for i in range(n)]) % 2

def bits_to_vector(s):
    return np.array([int(x) for x in s])

r = remote("localhost", int(9999))

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

r.recvuntil("Option:")
r.sendline("1")
r.sendline(matrix_to_bits(G))

r.recvuntil("M:")
M = bits_to_matrix(r.recvline().strip().decode())

C = LinearCode(Matrix(GF(2), M))
H = C.parity_check_matrix().change_ring(ZZ).LLL().change_ring(GF(2)).numpy(dtype=int)

bpd=bp_decoder(
    H, #the parity check matrix
    error_rate=threshold, # the error rate on each bit
    max_iter=10000, #the maximum iteration depth for BP
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

r.sendline("3")
for i in range(200):
    r.recvuntil("c:")
    encoded = bits_to_vector(r.recvline().strip().decode())
    decoded_codeword = bpd.decode(encoded)

    key = tuple(list(H @ decoded_codeword.transpose() % 2))

    if (key in dic):
        ttt = 0
        for i in range(len(dic[key])):
            if (ttt >= 20):
                break
            temp = (decoded_codeword + dic[key][i]) % 2
            try:
                guess = Matrix(GF(2), M).solve_left(vector(GF(2), temp))
                ttt += 1
                r.sendline(matrix_to_bits(guess.numpy(dtype=int)))
            except KeyboardInterrupt:
                exit()
            except e:
                print(e)
                pass
        for _ in range(20 - ttt):
            r.sendline(matrix_to_bits(decoded_codeword))
    else:
        for _ in range(20):
            r.sendline(matrix_to_bits(decoded_codeword))
    

r.interactive()

