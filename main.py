from Interpolation import Lagrangian
from DimensionalityReduction import PCAA
from FractionWrapper import valsToFractions
from OutputManager import Output

output = Output()
fileOutput = Output(type="File")

# Lagrangian 

l1 = Lagrangian([6, 9, 15], [10, 15, 20], fileOutput)
fileOutput.write(filePath="l1")
l1.evaluate(12, output)
output.write()

l1exact = Lagrangian(valsToFractions([6, 9, 15]), valsToFractions([10, 15, 20]), fileOutput)
fileOutput.write(filePath="l1exact")
l1exact.evaluate(12, output)
output.write()

# Newton Forward Difference

