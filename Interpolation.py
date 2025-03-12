import math
import sys

class Lagrangian():
    def __init__(self, XPoints, YPoints, working=True):
        self.X = XPoints
        self.Y = YPoints

        # do some computation (remember Lagrangian must be reconstructed from scratch if you want to add/remove new points)
        self.bases = [self.createBasis(i, XPoints) for i in range(len(XPoints))]

        # if working out is enabled, then print out the working out
        if working:
            print("===LANGRANGIAN CREATION===")
            sys.stdout.write("y = ")

            for i in range(len(XPoints)):
                sys.stdout.write(f"y{i} ")

            sys.stdout.write("\n = ")


    def createBasis(self, i, XPoints):
        denom = math.prod(XPoints[i] - XPoints[j] if i != j else 1 for j in range(len(XPoints))) # relies on XPoints being distinct btw
        return lambda x: math.prod([x - XPoints[j] if i != j else 1 for j in range(len(XPoints))])/denom

    def evaluate(self, x):
        return sum(self.Y[i] * self.bases[i](x) for i in range(len(self.X)))