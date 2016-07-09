
"""
Problem 66: Diophantine equation
Consider quadratic Diophantine equations of the form:
x^2 - Dy^2 = 1

Find the value of D <= 1000 in minimal solutions of x
for which the largest value of x is obtained.

(D positive integer)

Some Sources:
http://www.ams.org/notices/200202/fea-lenstra.pdf
http://www.cs.umb.edu/~eb/458/final/KoffiPresentation.pdf
http://math.stackexchange.com/questions/90406/

Goal:
Find fundamental solution to Pell's equation.

[See representation of continued fractions,
 if confused about notation.]

Continued Fractions Method:
* Rewrite Pell's equation as: (difference of two squares)
  (x + y*sqrt(D)) * (x - y*sqrt(D)) = 1

* "Find nontrivial unit of the ring Z[sqrt(D)] of norm 1"

* Find continued fraction expansion of sqrt(D),
  truncating at the end of the first period.
  * Note: for (irrational?) square roots, the end of the period is
    when a partial quotient is twice the integer part.
  * For (d > 1, rational number, not a square of another rational num):
    sqrt(D) = [a_0; {a_1, a_2, ... a_2, a_1, 2a_0}]
    (numbers enclosed in brackets is the periodic block)

* Use the continued fraction to obtain (reduced?) improper fraction (x/y),
  where x and y are the solutions to the equation.
  * If r is the length of the period:
    * Solution may be at convergent# r, r-1, or 2r-1 (always odd)
    * Ex: [a_0; a_1, a_2, ..., a_r]
    * Convergent# must be odd?
"""

from math import floor, sqrt

def gcd(x, y):
    """
    Euclidean algorithm for GCD.
    (Is this necessary?)
    """
    while y != 0:
        (x, y) = (y, x % y)
    return int(x)

def is_pell_solution(x, y, D):
    """
    Check if actual solution to Pell equation.
    """
    return ((x**2 - D*y**2) == 1)


""" FAILS w/ 139, etc.
def sqrtcf_solver(D):
    a0 = int(floor(sqrt(D)))
    period = []
    rnum = sqrt(D)
    while True:
        rnum = 1.0/(rnum - floor(rnum))
        ax = int(floor(rnum))
        print rnum, ax
        period.append(ax)
        if (ax == 2*a0):
            break
    return [a0] + period
"""
# NEW!: Using manipulations and substitutions
def sqrtcf_solver(D):
    """
    Gets continued fraction representation of sqrt(D).
    [a0; period], where period [a1, a2, ... a2, a1, 2_a0]
    CAREFUL!: Floating point calculations can fail -> See sqrt(139), etc.
    Resolve by limiting such calculations.
    Returns: [a0, period]
    """
    D = int(D) # just in case?
    a0 = int(floor(sqrt(D)))
    x, y = 1, a0
    cf = [a0]
    while True:
        # x_n = (D - y_{n-1}^2) / x_{n-1}
        x = (D - y*y) / x
        # a_n = (sqrt(D) + y_{n-1} \ x_n)
        an = (a0 + y) / x
        cf.append(an)
        # y_n = a_n*x_n - y_{n-1}
        y = an*x - y

        if (an == 2*a0): break
    return cf

def imf_from_cf(cf):
    """
    Gets improper fraction representation from
    continued fraction representation. (x/y)
    Returns: [x, y]
    """
    # r + (x/y)
    x, y = cf[-1], 1
    for ax in reversed(cf[:-1]):
        # ax + (1/(x/y))
        # (ax*x/x) + (y/x)
        # (ax*x + y)/x
        x, y = ax*x + y, x
    return x, y

def pell_solver(D): # not the greatest solution
    """
    Finds fundamental solution to x^2 - Dy^2 = 1.
    Where D positive int, not perfect square, please.
    Returns: [x, y]
    """
    cf = sqrtcf_solver(D)
    cfx = cf
    if (len(cf) & 1): cfx = cfx[:-1] # if period (len(cf)-1) even, use one less
    x, y = imf_from_cf(cfx)
    if not is_pell_solution(x, y, D): # try (2r-1)
        cfx = cf + cf[1:-1]
        x, y = imf_from_cf(cfx)
    return x, y

def nonsq(n):
    """
    Get nth non-square positive integer.
    F(n) = n + floor(0.5 + sqrt(n))
    See: http://oeis.org/A000037
    """
    return int(n + floor(0.5 + sqrt(n)))

def p66(dmax=1000):
    """
    Solves problem 66.
    Iterate through non-squares <= 1000.
    Some values saved for diagnostic purposes.
    """
    x, y = 0, 0
    n = 1
    nsq = nonsq(n)
    dret = 0
    while (nsq <= dmax):
        xn, yn = pell_solver(nsq)
        if (xn > x):
            x, y = xn, yn
            dret = nsq
        #print nsq, int(xn), int(yn)#, sqrtcf_solver(nsq)
        n += 1
        nsq = nonsq(n)
    return dret


if __name__ == "__main__":
    print(p66())

