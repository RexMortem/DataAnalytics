def adjustLength(X, Y):
    if len(X) != len(Y):
        print("WARNING: Not the same length!")
        
        if len(X) > len(Y):
            Y.extend([0] * (len(X) - len(Y)))
        else:
            X.extend([0] * (len(Y) - len(X)))

def sumSquaredError(X, Y):
    adjustLength(X, Y)

    # actual function time
    toReturn = 0

    for i in range(len(X)):
        toReturn += (X[i]-Y[i])*(X[i]-Y[i])

    return toReturn

def sumAbsoluteError(X, Y):
    adjustLength(X, Y)

    # actual function time
    toReturn = 0

    for i in range(len(X)):
        toReturn += abs(X[i] - Y[i])
    
    return toReturn