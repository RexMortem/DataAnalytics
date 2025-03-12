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
            print("\n===LANGRANGIAN CREATION===")
            sys.stdout.write("y(x) = ")

            for i in range(len(XPoints)):
                sys.stdout.write(f"y_{{{i}}}L_{{{i}}}(x)")

                if (i != (len(XPoints)-1)):
                    sys.stdout.write(" + ")

            sys.stdout.write("\n = ")

            for i in range(len(XPoints)):
                sys.stdout.write(f"{YPoints[i]}L_{{{i}}}")

                if (i != (len(XPoints)-1)):
                    sys.stdout.write(" + ")

            sys.stdout.write(".\n\n\n")

            # will have to do some redundant work to output the bases
            for i in range(len(self.X)):
                sys.stdout.write(f"L_{{{i}}}(x) = ")

                genNominator = "" # general form 
                genDenominator = ""

                spNominator = "" # specific form (substituting in x_{1} for the actual x_{1} value for example)
                spDenominator = "" 

                parDenominator = "" # partially evaluated denominator
                fulDenominator = 1 # fully evaluated denominator

                for j in range(len(self.X)):
                    if i == j: continue # skip the same index (avoid nominator being 0)
                    
                    genNominator += f"(x - x_{{{j}}})"
                    spNominator += f"(x - {XPoints[j]})"

                    # do denoms
                    genDenominator += f"(x_{{{i}}} - x_{{{j}}})" 
                    spDenominator += f"({XPoints[i]} - {XPoints[j]})"
                    
                    # some horrible checks for if it's the last one added
                    if (j == (len(self.X) - 1)) or ((j == (len(self.X) - 2)) and (i == (len(self.X) -1))):
                        parDenominator += f"({XPoints[i] - XPoints[j]})"
                    else:
                        parDenominator += f"({XPoints[i] - XPoints[j]})" + " * "

                    fulDenominator *= XPoints[i] - XPoints[j]

                sys.stdout.write(f"\\frac{{{genNominator}}}{{{genDenominator}}}\n")
                sys.stdout.write(f"=\\frac{{{spNominator}}}{{{spDenominator}}}\n")
                sys.stdout.write(f"=\\frac{{{spNominator}}}{{{parDenominator}}}\n")
                sys.stdout.write(f"=\\frac{{{spNominator}}}{{{fulDenominator}}}.\n\n\n")

    def createBasis(self, i, XPoints):
        denom = math.prod(XPoints[i] - XPoints[j] if i != j else 1 for j in range(len(XPoints))) # relies on XPoints being distinct btw
        return lambda x: math.prod([x - XPoints[j] if i != j else 1 for j in range(len(XPoints))])/denom

    def evaluate(self, x, working=True):
        solution = sum(self.Y[i] * self.bases[i](x) for i in range(len(self.X)))

        if working: # for this, we will have to redo some basis work to output them
            print("\n===LAGRANGIAN EVALUATION===")
            
            sys.stdout.write(f"y({x}) = ")

            for i in range(len(self.X)):
                sys.stdout.write(f"{self.Y[i]}L_{{{i}}}({x})")

                if (i != (len(self.X)-1)):
                    sys.stdout.write(" + ")
                
            sys.stdout.write(".\n\n\n")

            baseEvaluations = [None] * len(self.X)

            for i in range(len(self.X)):
                sys.stdout.write(f"L_{{{i}}}({x}) = ")

                fstNominator = "" # first nominator
                denominator = 1 # we just use the evaluated denom (constructing the lagrangian prints out the denom steps)

                parNominator = "" # partially evaluated nominator
                fulNominator = 1 # fully evaluated nominator

                for j in range(len(self.X)):
                    if i == j: continue # skip the same index (avoid nominator being 0)
                    
                    fstNominator += f"({x} - {self.X[j]})"
                    
                    # some horrible checks for if it's the last one added
                    if (j == (len(self.X) - 1)) or ((j == (len(self.X) - 2)) and (i == (len(self.X) -1))):
                        parNominator += f"({x - self.X[j]})"
                    else:
                        parNominator += f"({x - self.X[j]})" + " * "

                    fulNominator *= x - self.X[j]
                    denominator *= self.X[i] - self.X[j]

                sys.stdout.write(f"\\frac{{{fstNominator}}}{{{denominator}}}\n")
                sys.stdout.write(f"=\\frac{{{parNominator}}}{{{denominator}}}\n")
                sys.stdout.write(f"=\\frac{{{fulNominator}}}{{{denominator}}}\n")
                sys.stdout.write(f"={fulNominator/denominator}.\n\n\n")

                baseEvaluations[i] = fulNominator/denominator
            
        # final solution
        sys.stdout.write(f"y({x}) = ")

        for i in range(len(self.X)):
            sys.stdout.write(f"{self.Y[i]}({baseEvaluations[i]})")

            if (i != (len(self.X)-1)):
                sys.stdout.write(" + ")

        sys.stdout.write(f"\n= {solution}.\n\n\n")

        return solution