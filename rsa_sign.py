import hashlib

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(a, m):
    return pow(a, -1, m)  # Cleaned up using Python 3.8+

# Key generation
def generate_keys(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    return (e, n), (d, n)

# Sign message
def sign(message, d, n):
    h = int(hashlib.sha1(message.encode()).hexdigest(), 16)
    return pow(h, d, n)

# Verify signature
def verify(message, signature, e, n):
    h = int(hashlib.sha1(message.encode()).hexdigest(), 16)
    h_from_signature = pow(signature, e, n)
    return h == h_from_signature

# === Main ===
message = input("Enter message: ")
p = int(input("Enter prime p: "))
q = int(input("Enter prime q: "))
e = int(input("Enter public exponent e: "))

pub, priv = generate_keys(p, q, e)
signature = sign(message, priv[0], priv[1])
print(f"\nSignature: {signature}")

valid = verify(message, signature, pub[0], pub[1])
print("Signature valid?", valid)
