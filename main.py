import Interpolation
import DimensionalityReduction
from FractionWrapper import valsToFractions

l1 = Interpolation.Lagrangian([6, 9, 15], [10, 15, 20])
l1.evaluate(12)

l1exact = Interpolation.Lagrangian(valsToFractions([6, 9, 15]), valsToFractions([10, 15, 20]))
l1exact.evaluate(12)