from secrets import randbelow
import numpy as np
from ldpc import bp_decoder, code_util
import random

n = 100
k = int(n * 2)

print(n, k)
threshold = 0.1

G = [[randbelow(2) for _ in range(k)] for i in range(n)]
G = Matrix(GF(2), G)
C = LinearCode(G)

m = [randbelow(2) for _ in range(n)]
m = vector(GF(2), m)

original = m * G 

noise = [0 for _ in range(k)]

for i in range(k):
    if (randbelow(100) / 100) < threshold:
        noise[i] = 1

print(sum(noise))
noise = vector(GF(2), noise)

encoded = original + noise

bpd=bp_decoder(
    C.parity_check_matrix().change_ring(ZZ).LLL().change_ring(GF(2)).numpy(dtype=int), #the parity check matrix
    error_rate=0.1, # the error rate on each bit
    max_iter=1000, #the maximum iteration depth for BP
    bp_method="product_sum", #BP method. The other option is `minimum_sum'
    channel_probs=[None] #channel probability probabilities. Will overide error rate.
)

decoded_codeword=bpd.decode(encoded.numpy(dtype=int))
print(k - sum(original == decoded_codeword))