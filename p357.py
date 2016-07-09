"""
Problem 357: Prime generating integers
Find the sum of all positive integers n not exceeding 100 000 000
such that for every divisor d of n, d+n/d is prime.

Goal:
Find pairs of divisors that sum to a prime number.

Simple limits on possible n:
* Because n+1 must always be considered (every n has a d=1),
  n must be even, except for 1.
  (Primes except for 2 are odd.)
* Notice also that n must be one less than a prime.
* Aside from 1, if n is even, then it will have a d=2.
  So, for 2+(d/2) to be odd, (d/2) must be odd.
  For (d/2) to be odd, n cannot be divisible by 4. (meh)
* Aside from 1, n cannot be a perfect square. (n/d = d)
  d+d cannot be prime, except for n, d = 1.
"""

import time
from math import sqrt

def generate_divisors(lim=1000):
    """
    Generate list of divisors.
    Not recommended for lim much greater than 10000000. (Too big!)
    """
    divlist = [[1] for i in xrange(lim+1)]
    div = 2
    while (div <= lim):
        mult = div
        while (mult <= lim):
            divlist[mult].append(div)
            mult += div
        div += 1
    return divlist

def get_divisors(n):
    """
    Simple way to get divisor pairs in order. (Unused.)
    """
    lim = int(sqrt(n))
    dpairs = [(1, n)]
    for i in xrange(2, lim+1):
        if (n % i == 0):
            dpairs.append((i, n/i))
    return dpairs

def sieve_erato(n):
    """
    Set implementation of Sieve of Eratosthenes.
    Save all multiples of primes in set for lookup.
    """
    mult = set()
    if n >= 2: # No need to store evens
        yield 2
    for i in xrange(3, n+1, 2): # Skip evens
        if i not in mult: # It's a prime!
            yield i
            mult.update(xrange(i*i, n+1, i))

def p357(nx=100000000):
    """
    Solves problem 357. (~60s)
    """
    primes = set(sieve_erato(nx))
    #pglist = [1]
    pgsum = 1
    for p in primes:
        n = p-1
        if (n % 4 == 0):
            continue

        # Get divisor routine
        lim = int(sqrt(n))
        if lim == sqrt(n):
            continue
        pg = True
        for i in xrange(2, lim+1):
            if (n % i == 0) and (i + n/i) not in primes:
                pg = False
                break
        if pg:
            #pglist.append(n)
            pgsum += n
    return pgsum #sum(pglist)


if __name__ == "__main__":
    time1 = time.time()
    print(p357())
    time2 = time.time()
    print("Runtime (s): {:.8}".format(time2-time1))
