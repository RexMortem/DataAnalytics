from Interpolation import Lagrangian, factorial, choose
from DimensionalityReduction import APCA, mergeLeastDerivation
from FractionWrapper import valsToFractions
from Regression import sumAbsoluteError, sumSquaredError
from OutputManager import Output

output = Output()

# Lagrangian 

l1 = Lagrangian([6, 9, 15], [10, 15, 20], output)
output.write()
l1.evaluate(12, output)
output.write()

l1exact = Lagrangian(valsToFractions([6, 9, 15]), valsToFractions([10, 15, 20]), output)
output.write()
l1exact.evaluate(12, output)
output.write()

# APCA

X,Y = APCA([7, 5, 3, 3, 3, 4, 4, 6], N=3)
print("Squared Error: ", sumSquaredError(X, [7, 5, 3, 3, 3, 4, 4, 6]))

# Newton stuff
print("Non-integer choose function: ", choose(2, 2.4))

print(choose(1, 2.4))
print(choose(2, 2.4))