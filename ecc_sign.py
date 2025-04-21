import hashlib
import random

# ECC over a prime field
def inverse_mod(k, p):
    return pow(k, -1, p)

def point_add(P, Q, a, p):
    # Handle special cases
    if P is None:
        return Q
    if Q is None:
        return P
    
    x1, y1 = P
    x2, y2 = Q
    
    # Point doubling
    if P == Q:
        # Handle vertical tangent
        if y1 == 0:
            return None
        l = ((3 * x1 * x1 + a) * inverse_mod(2 * y1, p)) % p
    # Point addition
    else:
        # Handle points that sum to infinity
        if x1 == x2:
            return None
        l = ((y2 - y1) * inverse_mod(x2 - x1, p)) % p
    
    x3 = (l * l - x1 - x2) % p
    y3 = (l * (x1 - x3) - y1) % p
    
    return (x3, y3)

def scalar_mult(k, P, a, p):
    # Double-and-add algorithm for efficient scalar multiplication
    if k == 0 or P is None:
        return None
    
    result = None
    addend = P
    
    while k:
        if k & 1:  # Equivalent to k % 2 == 1
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1  # Equivalent to k //= 2
    
    return result

def hash_message(message):
    """Hash the message and convert to integer"""
    h = hashlib.sha256(message.encode()).hexdigest()
    return int(h, 16)

# -------------- ECDSA Implementation --------------

def generate_keypair(a, p, n, G):
    """Generate private and public key pair"""
    private_key = random.randint(1, n-1)
    public_key = scalar_mult(private_key, G, a, p)
    return private_key, public_key

def sign_message(message, private_key, a, p, n, G):
    """Sign a message using ECDSA"""
    z = hash_message(message)
    
    r, s = 0, 0
    while r == 0 or s == 0:
        # Generate random k (per signature)
        k = random.randint(1, n-1)
        
        # Calculate point K = k*G
        K = scalar_mult(k, G, a, p)
        if K is None:
            continue
        
        # r = x coordinate of K (mod n)
        r = K[0] % n
        if r == 0:
            continue
        
        # s = k^-1 * (z + r*private_key) mod n
        k_inv = inverse_mod(k, n)
        s = (k_inv * (z + r * private_key) % n) % n
        
    return (r, s)

def verify_signature(message, signature, public_key, a, p, n, G):
    """Verify an ECDSA signature"""
    r, s = signature
    
    # Check if r and s are in [1, n-1]
    if not (1 <= r < n and 1 <= s < n):
        return False
    
    z = hash_message(message)
    
    # Calculate w = s^-1 mod n
    w = inverse_mod(s, n)
    
    # Calculate u1 = z*w mod n and u2 = r*w mod n
    u1 = (z * w) % n
    u2 = (r * w) % n
    
    # Calculate point X = u1*G + u2*public_key
    point1 = scalar_mult(u1, G, a, p)
    point2 = scalar_mult(u2, public_key, a, p)
    X = point_add(point1, point2, a, p)
    
    # If X is the point at infinity, the signature is invalid
    if X is None:
        return False
    
    # Verification: r == X[0] mod n
    return r == (X[0] % n)

# -------------- Main Program --------------

if __name__ == "__main__":
    try:
        # Curve parameters
        p = int(input("Enter prime field size p: "))
        a = int(input("Enter curve parameter a: "))
        b = int(input("Enter curve parameter b: "))
        Gx = int(input("Enter base point Gx: "))
        Gy = int(input("Enter base point Gy: "))
        n = int(input("Enter curve order n: "))
        G = (Gx, Gy)
        
        # Generate keys
        print("\nGenerating key pair...")
        private_key, public_key = generate_keypair(a, p, n, G)
        print(f"Private key: {private_key}")
        print(f"Public key: {public_key}")
        
        # Sign a message
        message = input("\nEnter a message to sign: ")
        print("Signing message...")
        signature = sign_message(message, private_key, a, p, n, G)
        print(f"Signature (r, s): {signature}")
        
        # Verify the signature
        print("\nVerifying signature...")
        valid = verify_signature(message, signature, public_key, a, p, n, G)
        print(f"Signature verification: {'Success' if valid else 'Failed'}")
        
        # Demo with tampered message
        tampered_message = message + " (tampered)"
        print(f"\nVerifying with tampered message: '{tampered_message}'")
        valid = verify_signature(tampered_message, signature, public_key, a, p, n, G)
        print(f"Tampered message verification: {'Success' if valid else 'Failed - tampering detected'}")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Please check that your inputs are valid for the curve equation y² = x³ + ax + b (mod p)")
