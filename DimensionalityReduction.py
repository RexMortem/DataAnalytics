import math
from OutputManager import Output

sF = 1/math.sqrt(2) # 1/(scaling factor for DWT)

def PAA(X):
    return X

def DWT(X, N, nextPowerOfTwo, working:Output = None):
    global sF

    averageTree = [None] * (nextPowerOfTwo + 1)
    averageTree[0] = X

    # be careful: differencesTree has one less layer, so indexing must be shifted!!!
    differencesTree = [None] * nextPowerOfTwo

    for i in range(1, len(averageTree)):
        # create a new level to the tree
        averageTree[i] = [None] * (len(averageTree[i-1]) // 2)
        differencesTree[i-1] = [None] * (len(averageTree[i-1]) // 2)
        
        for j in range(len(averageTree[i])): # compute averages
            averageTree[i][j] = (averageTree[i-1][2*j] + averageTree[i-1][(2*j) + 1])/2
            differencesTree[i-1][j] = (averageTree[i-1][2*j] - averageTree[i-1][(2*j) + 1])/2
    
    # now let's read the unnormalised DWT Coefficients 
    unnormalisedDWTCoeffs = [None] * len(X)
    unnormalisedDWTCoeffs[0] = averageTree[len(averageTree)-1][0] # bottom of the tree

    aP = 1

    for i in range(len(differencesTree)-1, -1, -1):
        for j in range(len(differencesTree[i])):
            unnormalisedDWTCoeffs[aP] = differencesTree[i][j]
            aP += 1

    print("Unnormalised DWT Coefficients: ", unnormalisedDWTCoeffs)

    # now let's apply dividing by sqrt(2)
    normalisedDWTCoeffs = [x for x in unnormalisedDWTCoeffs]

    nLayer = 0 # number currently on layer
    maxOnLayer = 2 # max elements on the layer
    layerI = 1 # the (layerI)th layer

    for i in range(2, len(normalisedDWTCoeffs)):
        if nLayer == maxOnLayer: # reset (next layer time)
            nLayer = 0
            maxOnLayer *= 2
            layerI += 1
        
        normalisedDWTCoeffs[i] = normalisedDWTCoeffs[i] * math.pow(sF, layerI)

        nLayer += 1
    
    print("Normalised DWT Coefficients: ", normalisedDWTCoeffs)

    # okay now let's find the top N coefficients, and zero the rest 
    indicesThatKeep = {}

    # we'll use tombstones which aren't massively efficient but it's fine for this
    for _ in range(N):
        maxValue = None 
        maxIndex = -1

        for i in range(len(normalisedDWTCoeffs)):
            if normalisedDWTCoeffs[i] == None: # found a tombstone value; let's skip
                continue 
            
            if (maxValue is None) or (abs(normalisedDWTCoeffs[i]) > maxValue):
                maxValue = abs(normalisedDWTCoeffs[i])
                maxIndex = i

        # lay tombstone and add index
        normalisedDWTCoeffs[maxIndex] = None 
        indicesThatKeep[maxIndex] = True
    
    truncatedDWTCoeffs = unnormalisedDWTCoeffs

    for i in range(len(truncatedDWTCoeffs)):
        if not (i in indicesThatKeep):
            truncatedDWTCoeffs[i] = 0
    
    print("Truncated DWT Coeffs: ", truncatedDWTCoeffs)

    return truncatedDWTCoeffs

def InverseDWT(X, nextPowerOfTwo):
    averageTree = [None] * (nextPowerOfTwo + 1) # this will be of inverse shape to the DWT averageTree
    averageTree[0] = [X[0]]

    xP = 1

    for i in range(0, len(averageTree)-1): # each iteration generates the next layer of the tree
        averageTree[i+1] = [None] * len(averageTree[i]) * 2

        for j in range(len(averageTree[i])): # must generate two values in above layer
            averageTree[i+1][2*j] = averageTree[i][j] + X[xP]
            averageTree[i+1][(2*j) + 1] = averageTree[i][j] - X[xP] 
            xP += 1
        
    return averageTree[len(averageTree)-1]

def replaceWithExactAverage(X, origX):
    # replace with exact mean values
    segValue = X[0]
    segStart = 0

    APCADescription = []

    for i in range(1, len(X)):
        if X[i] == segValue: # segment is continuing...
            continue
        
        # segment has been completed
        total = 0

        # the segment is from segStart <= j < i
        for j in range(segStart, i):
            total += origX[j]
        
        avg = total/(i - segStart)

        for j in range(segStart, i):
            X[j] = avg
        
        # add to APCADescription
        APCADescription.append((avg, i))

        # reset for next segment
        segStart = i
        segValue = X[i]
        

    # the segment is from segStart <= j < len(X)
    total = 0

    for j in range(segStart, len(X)):
        total += origX[j]
    
    avg = total/(len(X) - segStart)

    for j in range(segStart, len(X)):
        X[j] = avg
    
    # add last segment to APCADescription 
    APCADescription.append((avg, len(X)))
        
    return X, APCADescription

def mergeLeastDerivation(Y):
    leastDerivation = abs(Y[1][0] - Y[0][0]) # remember 0 is for values, for each interval thing
    firstIndex = 0

    for i in range(2, len(Y)):
        derivation = abs(Y[i][0] - Y[i - 1][0])

        if derivation < leastDerivation:
            leastDerivation = derivation 
            firstIndex = i-1
        
    # merge interval from firstIndex to firstIndex+1
    mergeAverage = (Y[firstIndex][0] + Y[firstIndex+1][0])/2
    mergedInterval = (mergeAverage, Y[firstIndex+1][1])

    # remove old intervals
    Y.pop(firstIndex)
    Y.pop(firstIndex)
    Y.insert(firstIndex, mergedInterval)

def mergeUntilNSegments(Y, N):
    while len(Y) > N:
        mergeLeastDerivation(Y)
    
    return Y

def timeSeriesFromAPCA(Y):
    X = []
    startIndex = 0

    for i in range(len(Y)):
        val, endIndex = Y[i]
        
        for j in range(startIndex, endIndex):
            X.append(val)
        
        startIndex = endIndex

    return X
# Ah yes, the Adaptive Piecewise Constant Approximation
# Do I know what that means? Nope! 
# But here's an implementation
def APCA(X, N=1, working:Output = None):
    if len(X) < 1: 
        print("please provide a non-empty time-series!")
        return None 
    
    # keep track of original for later :)
    origX = [X[i] for i in range(len(X))]

    # do padding step (if necessary)
    nextPowerOfTwo = math.ceil(math.log(len(X), 2))
    elementsToPad = int(math.pow(2, nextPowerOfTwo)) - len(X)

    X.extend(0 for i in range(elementsToPad))
    print("Extended: ", X)

    X = DWT(X, N, nextPowerOfTwo, working)

    X = InverseDWT(X, nextPowerOfTwo) # at this point, X is the reconstructed DWT
    print("Reconstructed DWT: ", X)

    # do un-padding step (if necessary)
    originalLength = len(X) - elementsToPad
    X = [X[i] for i in range(originalLength)]

    X, Y = replaceWithExactAverage(X, origX)

    print("Reconstructed APCA: ", X, Y)

    # let's do merging stuff
    mergeUntilNSegments(Y, N)

    # create time series, in case that's what weiren wants idk
    X = timeSeriesFromAPCA(Y)
    print("APCA Answer: ", X, Y)

    return X,Y
