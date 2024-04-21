from param import p, n, b
from hashlib import shake_128

load('output.sage')

A = []
vec = []

for i in range(len(factors)):
    g = output[i][0]
    h = output[i][4]
    b1 = F1(b)
    b2 = F2(output[i][4][1])^2 - F2(output[i][4][0])^3

    E1 = EllipticCurve(GF(p), [0, b1])
    E2 = EllipticCurve(F2, [0, b2])

    t = b1 / b2

    if (t^((p^2 - 1)/3) == 1 or t^((p^2 - 1)/2) == 1):
        print(i)
        continue

    if (E2.cardinality() % n != 0):
        print(i)
        continue

    h = E2.cardinality() // n

    P = E1(output[i][2][0], output[i][2][1])
    Q = h * E2(output[i][5][0], output[i][5][1])

    R = E1(output[i][3][0], output[i][3][1])
    S = h * E2(output[i][4][0], output[i][4][1])

    G.<x> = F2[]
    F3.<v> = F2.extension(x^6 - t)

    E3 = EllipticCurve(F3, [0, b])

    P = E3(P)
    Q = E3(v^2 * Q[0] , v^3 * Q[1])

    R = E3(R)
    S = E3(v^2 * S[0] , v^3 * S[1])

    A.append(factors[i])
    if (P.tate_pairing(Q, Integer(n), 6) == R.tate_pairing(S, Integer(n), 6)):
        print(0)
        vec.append(0)
    else:
        print(1)
        vec.append(1)

def decrypt(msg, key):
    y = shake_128("".join(map(str, key)).encode()).digest(len(msg))
    return bytes([msg[i] ^^ y[i] for i in range(len(msg))])

print(len(A))
key = map(int, Matrix(GF(2), A).solve_right(vector(GF(2), vec)))

print(decrypt(bytes.fromhex(c), key))

