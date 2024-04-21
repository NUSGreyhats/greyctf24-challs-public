from sage.libs.libecm import ecmfactor

class BN(object):
    @staticmethod
    def generate_prime_order(zbits):
        while True:
            z = randint(2^(zbits - 1), 2^zbits)
            pz = int(BN.p(z))
            if not is_prime(pz):
                continue
            rz = int(BN.r(z))
            if not is_prime(rz):
                continue
            break
        K = GF(pz)
        b = 1
        while True:
            curve = EllipticCurve(K, [0, b])
            card = curve.cardinality()
            if card % rz == 0:
                print(rz)
                break
            b += 1
        return curve

    @staticmethod
    def p(z):
        return 36 * z^4 + 36 * z^3 + 24 * z^2 + 6 * z + 1
    @staticmethod
    def r(z):
        return 36 * z^4 + 36 * z^3 + 18 * z^2 + 6 * z + 1
    @staticmethod
    def t(z):
        return 6 * z^2 + 1
    @staticmethod
    def s(z):
        return 6 * z^2 + 6 * z + 1


print(BN.generate_prime_order(128))