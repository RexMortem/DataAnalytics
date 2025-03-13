import math
import sys
from OutputManager import Output

# The strength of Lagrangian Interpolation is that it takes O(n^{2}) time
# However, you must recompute if you want to add a point (or remove a point)
class Lagrangian():
    def __init__(self, XPoints, YPoints, working:Output = None):
        self.X = XPoints
        self.Y = YPoints

        # do some computation (remember Lagrangian must be reconstructed from scratch if you want to add/remove new points)
        self.bases = [self.createBasis(i, XPoints) for i in range(len(XPoints))]

        # if working out is enabled, then print out the working out (wO for "working output")
        if working is not None:
            wO = "\n===LANGRANGIAN CREATION===\n"

            wO += "y(x) = "

            for i in range(len(XPoints)):
                wO += f"y_{{{i}}}L_{{{i}}}(x)"

                if (i != (len(XPoints)-1)):
                    wO += " + "

            wO += "\n = "

            for i in range(len(XPoints)):
                wO += f"{YPoints[i]}L_{{{i}}}"

                if (i != (len(XPoints)-1)):
                    wO += " + "

            wO += ".\n\n\n"

            # will have to do some redundant work to output the bases
            for i in range(len(self.X)):
                wO += f"L_{{{i}}}(x) = "

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

                wO += f"\\frac{{{genNominator}}}{{{genDenominator}}}\n"
                wO += f"=\\frac{{{spNominator}}}{{{spDenominator}}}\n"
                wO += f"=\\frac{{{spNominator}}}{{{parDenominator}}}\n"
                wO += f"=\\frac{{{spNominator}}}{{{fulDenominator}}}.\n\n\n"

            # return wO
            working.output = wO

    def createBasis(self, i, XPoints):
        denom = math.prod(XPoints[i] - XPoints[j] if i != j else 1 for j in range(len(XPoints))) # relies on XPoints being distinct btw
        return lambda x: math.prod([x - XPoints[j] if i != j else 1 for j in range(len(XPoints))])/denom

    def evaluate(self, x, working:Output = None):
        solution = sum(self.Y[i] * self.bases[i](x) for i in range(len(self.X)))

        if working is not None: # for this, we will have to redo some basis work to output them
            wO = "\n===LAGRANGIAN EVALUATION===\n"
            
            wO += f"y({x}) = "

            for i in range(len(self.X)):
                wO += f"{self.Y[i]}L_{{{i}}}({x})"

                if (i != (len(self.X)-1)):
                    wO += " + "
                
            wO += ".\n\n\n"

            baseEvaluations = [None] * len(self.X)

            for i in range(len(self.X)):
                wO += f"L_{{{i}}}({x}) = "

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

                wO += f"\\frac{{{fstNominator}}}{{{denominator}}}\n"
                wO += f"=\\frac{{{parNominator}}}{{{denominator}}}\n"
                wO += f"=\\frac{{{fulNominator}}}{{{denominator}}}\n"
                wO += f"={fulNominator/denominator}.\n\n\n"

                baseEvaluations[i] = fulNominator/denominator
            
            # final solution
            wO += f"y({x}) = "

            for i in range(len(self.X)):
                wO += f"{self.Y[i]}({baseEvaluations[i]})"

                if (i != (len(self.X)-1)):
                    wO += " + "

            wO += f"\n= {solution}.\n\n\n"
            working.output = wO

        return solution
    

# Allows incremental update (new points added without recomputing the entire thing), unlike Lagrangian
# can apply horner scheme to make computation fast
# class Newton():
#     def __init__(self):
#         pass