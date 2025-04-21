import random
from hashlib import sha1

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Key Generation
def generate_keys(p, g):
    x = random.randint(1, p - 2)        # Private key
    y = pow(g, x, p)                    # Public key
    return (p, g, y), x

# Signature Generation
def sign(message, p, g, x):
    h = int(sha1(message.encode()).hexdigest(), 16)
    while True:
        k = random.randint(1, p - 2)
        if gcd(k, p - 1) == 1:
            break
    r = pow(g, k, p)
    k_inv = pow(k, -1, p - 1)
    s = (k_inv * (h - x * r)) % (p - 1)
    return r, s

# Signature Verification
def verify(message, r, s, p, g, y):
    h = int(sha1(message.encode()).hexdigest(), 16)
    v1 = pow(y, r, p) * pow(r, s, p) % p
    v2 = pow(g, h, p)
    return v1 == v2

# === Main ===
message = input("Enter message: ")
p = int(input("Enter a prime number p: "))
g = int(input("Enter a generator g: "))

public_key, private_key = generate_keys(p, g)
r, s = sign(message, p, g, private_key)

print(f"\nSignature: (r={r}, s={s})")
print("Verifying...")

is_valid = verify(message, r, s, p, g, public_key[2])
print("Signature valid?" , is_valid)
