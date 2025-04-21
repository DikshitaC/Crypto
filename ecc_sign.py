def modinv(a, m):
    return pow(a, -1, m)

def point_add(P, Q, a, p):
    if P == (None, None):
        return Q
    if Q == (None, None):
        return P
    if P == Q:
        return point_double(P, a, p)
    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
        return (None, None)

    x1, y1 = P
    x2, y2 = Q
    s = ((y2 - y1) * modinv(x2 - x1, p)) % p
    x3 = (s**2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)

def point_double(P, a, p):
    if P == (None, None):
        return P

    x, y = P
    s = ((3 * x**2 + a) * modinv(2 * y, p)) % p
    x3 = (s**2 - 2 * x) % p
    y3 = (s * (x - x3) - y) % p
    return (x3, y3)

def scalar_mult(k, P, a, p):
    R = (None, None)
    Q = P
    while k > 0:
        if k % 2 == 1:
            R = point_add(R, Q, a, p)
        Q = point_double(Q, a, p)
        k //= 2
    return R

# ===== USER INPUT =====
G = (5, 1)
n = 19
d = 2
mu = 10  # message hash value
a = 2
b = 2
p = 17

# ===== KEY GENERATION =====
P = scalar_mult(d, G, a, p)  # public key

# ===== SIGNATURE GENERATION =====
k = 3  # Random number (should be random in real cases)
K = scalar_mult(k, G, a, p)
r = K[0] % n
s = (modinv(k, n) * (mu + d * r)) % n
signature = (r, s)

# ===== SIGNATURE VERIFICATION =====
w = modinv(s, n)
u1 = (mu * w) % n
u2 = (r * w) % n
X = point_add(scalar_mult(u1, G, a, p), scalar_mult(u2, P, a, p), a, p)

valid = (X[0] % n) == r

# ===== OUTPUT =====
print(f"Public Key P = {P}")
print(f"Signature = (r={r}, s={s})")
print(f"Verification Point = {X}")
print("Signature is", "VALID ✅" if valid else "INVALID ❌")
