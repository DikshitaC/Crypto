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

def point_negate(P, p):
    if P is None:
        return None
    x, y = P
    return (x, (-y) % p)

# ---------- USER INPUT ----------
try:
    p = int(input("Enter prime p: "))
    a = int(input("Enter curve parameter a: "))
    b = int(input("Enter curve parameter b: "))
    Gx = int(input("Enter base point Gx: "))
    Gy = int(input("Enter base point Gy: "))
    G = (Gx, Gy)
    b_priv = int(input("Enter receiver's private key b: "))
    k = int(input("Enter random key k for encryption: "))
    Pm_x = int(input("Enter message point Px: "))
    Pm_y = int(input("Enter message point Py: "))
    Pm = (Pm_x, Pm_y)
    
    # ---------- ENCRYPTION ----------
    # Calculate receiver's public key
    Pb = scalar_mult(b_priv, G, a, p)
    print("\nReceiver's public key Pb:", Pb)
    
    # Calculate shared secret
    S = scalar_mult(k, Pb, a, p)
    print("Shared secret S:", S)
    
    # Calculate ciphertext points
    C1 = scalar_mult(k, G, a, p)
    C2 = point_add(Pm, S, a, p)
    
    print("\n--- Encrypted Message ---")
    print("C1:", C1)
    print("C2:", C2)
    
    # ---------- DECRYPTION ----------
    # Recover shared secret
    S_prime = scalar_mult(b_priv, C1, a, p)
    print("\nRecovered shared secret:", S_prime)
    
    # Recover message point by subtracting the shared secret
    S_neg = point_negate(S_prime, p)
    Pm_decrypted = point_add(C2, S_neg, a, p)
    
    print("\n--- Decryption Results ---")
    print("Original message point:", Pm)
    print("Decrypted message point:", Pm_decrypted)
    print("Decryption " + ("successful!" if Pm == Pm_decrypted else "failed!"))
    
except ValueError as e:
    print(f"Error: {e}")
    print("Please check that your inputs are valid for the curve equation y² = x³ + ax + b (mod p)")
