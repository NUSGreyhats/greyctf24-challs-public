#### FROM CHALLENGE ####

n = 500
qbits = 32
mbits = 4
q = 2**qbits
F = GF(q)
x = F.gen()

def int_to_F(n):
    return sum(b*x**i for i,b in enumerate(map(int, bin(n)[2:][::-1])))

def F_to_int(f):
    return f.integer_representation()

def gen_key():
    return np.array([b for b in map(int, format(randbits(n), "0500b"))], dtype=object)

def gen_a():
    return np.array([int_to_F(randbits(qbits)) for _ in range(n)], dtype=object)

def gen_noise():
    return int_to_F(randbits(qbits - mbits))

def encrypt_mbits(m, s):
    a = gen_a()
    f = np.vectorize(F_to_int)
    m = int_to_F(m << (qbits - mbits))
    return (f(a), F_to_int(np.dot(a, s) + m + gen_noise()))

def decrypt_mbits(c, s):
    a,b = c
    f = np.vectorize(int_to_F)
    a,b = f(a), int_to_F(b)
    return F_to_int(b - np.dot(a,s)) >> (qbits - mbits)

def encrypt_m(m, s):
    m = bytes_to_long(m)
    c = []
    while m != 0:
        mb = m & 0b1111
        c.append(encrypt_mbits(mb, s))
        m >>= 4
    return c[::-1]

def decrypt_m(c, s):
    m = 0
    for cb in c:
        m <<= 4
        mb = decrypt_mbits(cb, s)
        m += int(mb)
    return long_to_bytes(m)

#### END FROM CHALLENGE ####

from fromchal import *

def split_m_into_mb(m):
    m = bytes_to_long(m)
    mbs = []
    while m != 0:
        mbs.append(m & 0b1111)
        m >>= 4
    return mbs[::-1]

def eqns_from_ctbits(cb, mb):
    a,b = cb
    m_bitarr = [*map(int, format(mb, "04b"))]
    m = vector(GF(2), [*map(int, format(mb, "04b"))])
    A = matrix(GF(2), [[*map(int, format(l, "032b")[:mbits])] for l in a]).T
    b = vector(GF(2), [*map(int, format(b, "032b")[:mbits])])
    
    # A * vector(GF(2), [*key]) + m - b = 0
    return A, b - m
    
def matq_solve_right_all(mat, vec, q):
    """
    Solves for all vectors u such that
    `mat * u = vec`, where we are working
    in ZZ/`q`ZZ.
    """
    v = mat.solve_right(vec)
    if is_prime(q):
        return [v + k for k in mat.right_kernel()]
    kernel = modq_kernel(mat, q)
    if kernel.nrows() > 16: raise Exception("Too many solutions, regen challenge")
    unique_v = set(tuple(v + k) for k in FiniteZZsubmodule_iterator([*kernel]))
    return list(vector(Zmod(q), v) for v in unique_v)

mbs = split_m_into_mb(message)
eqns = [eqns_from_ctbits(*x) for x in zip(ciphertext, mbs)]
A = block_matrix([[a] for a,_ in eqns])
m_b = [list(b) for _,b in eqns]
m_b = vector(GF(2), [b for a in m_b for b in a])
for pos_key in matq_solve_right_all(A, m_b, 2):
    xor_stream = sha512(long_to_bytes(int(''.join(map(str, pos_key)), 2))).digest()
    print(bytes([a^^b for a,b in zip(bytes.fromhex(flag_xored), xor_stream)]).decode())
