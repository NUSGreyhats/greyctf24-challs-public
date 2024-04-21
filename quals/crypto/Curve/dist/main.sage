from param import p, b, n
from secrets import randbelow
from hashlib import shake_128

def encrypt(msg, key):
    y = shake_128("".join(map(str, key)).encode()).digest(len(msg))
    return bytes([msg[i] ^^ y[i] for i in range(len(msg))])
    
FLAG = b'REDACTED'
m = 150

F1 = GF(p)
F2.<u> = GF(p^2)

hidden = [randbelow(2) for _ in range(m)]
factors = []
output = []

for _ in range(900):
    E1 = EllipticCurve(GF(p), [0, b])
    E2 = EllipticCurve(F2, [0, F2.random_element()])

    g = E1.random_point()
    h = E2.random_point()

    factor = [randbelow(2) for _ in range(m)]
    k = sum([hidden[i] * factor[i] for i in range(m)]) % 2
    factors.append(factor)
    
    if (k):
        x, y, z = [randbelow(n) for _ in range(3)]
    else:
        x, y = [randbelow(n) for _ in range(2)]
        z = x * y

    output.append([g, x * g, y * g, z * g, h, x * h])

output = [[(point[0], point[1]) for point in row] for row in output]

f = open("output.txt", "w")
f.write(f"c='{encrypt(FLAG, hidden).hex()}'\n")
f.write(f"{factors=}\n")
f.write(f"{output=}\n")
