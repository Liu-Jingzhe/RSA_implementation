import random


def gcd(a, b):
    while a % b != 0:
        temp = b
        b = a % b
        a = temp
    return b


def inverse(a, b):    # find b's inverse mod a
    if a == 0:
        return 0
    r0 = b
    r1 = a
    s0 = 0
    s1 = 1
    t0 = 1
    t1 = 0
    while r0 != 0:
        q = r1//r0
        temp = r0
        r0 = r1-q*r0
        r1 = temp
        temp = t0
        t0 = t1-q*t0
        t1 = temp
        temp = s0
        s0 = s1-q*s0
        s1 = temp
    return t1


def square_multiply(m, d, n):
    d_binary_bits = []
    while d > 0:
        d_binary_bits.append(d % 2)
        d = d // 2                       #d_binary_bits is now [d0, d1, ... , d_k-1]
    power = 1
    for i in range(len(d_binary_bits)-1, -1, -1):
        power = (power*power) % n
        if d_binary_bits[i] == 1:
            power = (m*power) % n
    return power


def is_prime(n, test_times):
    if n % 2 == 0:
        return False
    m = (n-1)//2
    s = 1
    while m % 2 == 0:
        m = m // 2
        s = s+1
    b = 0
    for i in range(test_times):
        a = random.randint(2, n-2)
        if gcd(a, n) != 1:
            return False
        a = square_multiply(a, m, n)
        if a % n == 1 or a % n == n-1:
            continue
        for j in range(1, s):
            a = square_multiply(a, 2, n)
            if a % n == 1:
                return False
            if a % n == n-1:
                b = 1
                break
        if b == 1:
            continue
        else:
            return False
    return True


secure_dic = {80: 1024, 112: 2048, 128: 3072, 192: 7680, 256: 15360, 1: 16}


def generate(security_level):
    modulus = secure_dic[security_level]
    result = []
    while 1:
        if len(result) < 2:
            p = random.randrange(2**(int(modulus/2)), 2**(int(modulus/2)+1), 1)
            if is_prime(p, 40):
                if len(result) == 0 or result[0] != p:
                    result.append(p)
        else:
            return result[0], result[1]


def get_keys(p, q):
    n = p*q
    euler_n = (p-1)*(q-1)
    while 1:
        d = random.randint(n//4, n//2)
        if gcd(d, euler_n) == 1:
            e = inverse(euler_n, d) % euler_n
            if e > (n//4):
                return n, e, d


def encrypt(p, e, n):
    return square_multiply(p, e, n)


def decrypt(c, d, n):
    return square_multiply(c, d, n)


def fast_power(base, power, n):
    result = 1
    tmp = base
    while power > 0:
        if power & 1 == 1:
            result = (result * tmp) % n
        tmp = (tmp * tmp) % n
        power = power >> 1
    return result


# MillerRabin
def MillerRabin(n, iter_num):
    # 2 is prime
    if n == 2:
        return True
    # if n is even or less than 2, then n is not a prime
    if n & 1 == 0 or n < 2:
        return False
    # n-1 = (2^s)m
    m, s = n - 1, 0
    while m&1 == 0:
        m = m >> 1
        s += 1
    # M-R test
    for _ in range(iter_num):
        b = square_multiply(random.randint(2,n-1), m, n)
        if b == 1 or b == n-1:
            continue
        for __ in range(s-1):
            b = square_multiply(b, 2, n)
            if b == n-1:
                break
        else:
            return False
    return True


if __name__ == "__main__":
    p, q = generate(128)
    n, e, d = get_keys(p, q)
    #print(e)
    plain = 7
    c = encrypt(plain, e, n)
    m = decrypt(c, d, n)
    print(m)