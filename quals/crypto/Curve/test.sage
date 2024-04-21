from param import p, b, n # bn curve

F1 = GF(p)
F2.<u> = GF(p^2)

while True:
    t = F2.random_element()
    if (t^((p^2 - 1)/3) != 1 and t^((p^2 - 1)/2) != 1):
        break

E1 = EllipticCurve(GF(p), [0, b])
E2 = EllipticCurve(F2, [0, b / t])

h = 2 * p - n

P = E1.random_point()
Q = h * E2.random_point()

G.<x> = F2[]
F3.<v> = F2.extension(x^6 - t)

print(E2.cardinality() == h * n)

print(n * P)
print(n * Q)
print(E2.cardinality() * Q)

E3 = EllipticCurve(F3, [0, b])

P = E3(P)
Q = E3(v^2 * Q[0] , v^3 * Q[1])


print((P).tate_pairing(6 * Q, Integer(n), 6) == (3 * P).tate_pairing(2 * Q, Integer(n), 6))
