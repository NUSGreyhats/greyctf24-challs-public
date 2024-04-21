

# This file was *autogenerated* from the file main.sage
from sage.all_cmdline import *   # import sage library

_sage_const_150 = Integer(150); _sage_const_2 = Integer(2); _sage_const_900 = Integer(900); _sage_const_0 = Integer(0); _sage_const_3 = Integer(3); _sage_const_1 = Integer(1)
from param import p, b, n
from secrets import randbelow
from hashlib import shake_128

def encrypt(msg, key):
    y = shake_128("".join(map(str, key)).encode()).digest(len(msg))
    return bytes([msg[i] ^ y[i] for i in range(len(msg))])
    
FLAG = b'grey{tate_ate_weil_VfWZTKzMmgYhpEL7xvRwFu}'
m = _sage_const_150 

F1 = GF(p)
F2 = GF(p**_sage_const_2 , names=('u',)); (u,) = F2._first_ngens(1)

hidden = [randbelow(_sage_const_2 ) for _ in range(m)]
factors = []
output = []

for _ in range(_sage_const_900 ):
    E1 = EllipticCurve(GF(p), [_sage_const_0 , b])
    E2 = EllipticCurve(F2, [_sage_const_0 , F2.random_element()])

    g = E1.random_point()
    h = E2.random_point()

    factor = [randbelow(_sage_const_2 ) for _ in range(m)]
    k = sum([hidden[i] * factor[i] for i in range(m)]) % _sage_const_2 
    factors.append(factor)
    
    if (k):
        x, y, z = [randbelow(n) for _ in range(_sage_const_3 )]
    else:
        x, y = [randbelow(n) for _ in range(_sage_const_2 )]
        z = x * y

    output.append([g, x * g, y * g, z * g, h, x * h])

output = [[(point[_sage_const_0 ], point[_sage_const_1 ]) for point in row] for row in output]

f = open("output.txt", "w")
f.write(f"c='{encrypt(FLAG, hidden).hex()}'\n")
f.write(f"{factors=}\n")
f.write(f"{output=}\n")
