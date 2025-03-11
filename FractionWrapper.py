from fractions import Fraction

def valToFraction(x):
    return Fraction(x, 1)

def valsToFractions(X):
    return list(map(valToFraction, X))