from random import randrange, getrandbits

def is_prime(n, k=128):
    # To test if a number is prime
    """
        Args: n = Number to be tested
            : k = Number of tests
    """
    if n == 2 or n == 3:
        return True
    
    if n <= 1 or n % 2 == 0:
        return False

    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True
def generate_prime_candidate(length):
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p
def generate_prime_number(length=128):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in          bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p


def genp(l):
    return generate_prime_number(int(l))

def geng(p):
    binary = bin(int(p))[2:]
    return generate_prime_number(len(binary)-1)

def genpk(p):
    return randrange(1,int(p))

def calg(g,x,p):
    return pow(int(g),int(x),int(p))

"""
try:
    p = input("Enter a prime number (leave blank to auto generate): ")
except:
    p = generate_prime_number(l)
print("Prime: " + str(p))
print('')
try:
    g = input("Enter a generator (leave blank to auto generate): ")
except: 
    g=generate_prime_number(l-1)
print("Generator: "+ str(g))
print('')
try:
    a = input("Enter Alice's Private key (leave blank to auto generate): ")
except: 
    a=randrange(1,p)
print("Alice's private key: " + str(a))
print('')
try:
    b = input("Enter Bob's Private key (leave blank to auto generate): ")
except: 
    b=randrange(1,p)
print("Bob's private key: " + str(b))
print('')
Ga = pow(int(g),int(a),int(p))
Gb = pow(int(g),int(b),int(p))
print("Ga: " + str(Ga))
print("Gb: " + str(Gb))
print('')
Gab = pow(int(Gb),int(a),int(p))
Gba = pow(int(Ga),int(b),int(p))
print("Alice's secret key (Gab): " + str(Gab))
print("Bob's secret key (Gba): " + str(Gba))
print('')
print("As both of them match, a Diffie Hellman Key was successfully established!")
"""