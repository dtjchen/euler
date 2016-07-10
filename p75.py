"""
Problem 357: Singular integer right triangles
Given that L is the length of the wire,
for how many values of L <= 1,500,000 can exactly one
integer sided right angle triangle be formed?

(Secondary) Goal:
Find Pythagorean triplets.

Use:
* Euclid's formula
  * Given positive integers m and n, where
    m > n, m - n is odd and m, n are coprimes,
    primitive triplets can be generated.
    (One where a, b, c are coprime)

    a0 = (m*m - n*n)
    b0 = (2*m*n)
    c0 = (m*m + n*n)

  * The other triplets are "multiples" of these triplets.
    (k*a0, k*b0, k*c0)

  * To get an upper bound on m, we can sum (a0+b0+c0)
    to obtain 2*m*(m+n).
    Since n < m, to maximize n, we can essentially set it to 0. (or 1)
    So for the wire length to be <= 1500000,
    2*m^2 = 1500000,
    m = int(sqrt(1500000/2)) ~ 866
"""

import time
from math import sqrt

def gcd(x, y):
    """
    Euclidean algorithm for GCD.
    """
    while y != 0:
        (x, y) = (y, x % y)
    return int(x)

def farey(n):
    """
    Capture the nth Farey sequence.
    (Intended to generate coprimes, but too slow/too many generated)
    [https://en.wikipedia.org/wiki/Farey_sequence#Next_term]
    """
    # First two terms are 0/1 and 1/n
    a, b, c, d = 0, 1, 1, n
    yield (a, b)

    while (c <= n): # cannot be more than n/n
        # Calculate k
        k = int((n + b)/d)
        # a/b is this term, c/d is next term
        a, b, c, d = c, d, k*c - a, k*d - b
        yield (a, b)

def p75(lim=1500000):
    """
    Solves problem 75.
    """
    tcount = [0] * (lim+1)
    mlim = int(sqrt(lim/2))

    # Keep it simple, just use for loops
    for m in xrange(2, mlim+1):
        for n in xrange(1, m):
            if ((m-n) & 1) and gcd(m, n) == 1:
                # Summed up a+b+c
                psum0 = 2*m*(m+n)
                psum = psum0
                while True:
                    if (psum > lim):
                        break
                    tcount[psum] += 1
                    psum += psum0

    # Find hot singles in your wire lengths
    singles = 0
    for tc in tcount[1:]:
        if tc == 1:
            singles += 1
    return singles


if __name__ == "__main__":
    time0 = time.time()
    print(p75())
    time1 = time.time()
    print("Runtime (s): {:.8}".format(time1-time0))
