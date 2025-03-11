import Interpolation
import DimensionalityReduction
from FractionWrapper import valsToFractions

l1 = Interpolation.Lagrangian([5,6,9,11], [12, 13, 14, 16])
print(l1.evaluate(10))

l2 = Interpolation.Lagrangian([6, 9, 15], [10, 15, 20])
print(l2.evaluate(12))

l1exact = Interpolation.Lagrangian(valsToFractions([5,6,9,11]), valsToFractions([12, 13, 14, 16]))
print(l1exact.evaluate(10))

l2exact = Interpolation.Lagrangian(valsToFractions([6,9,15]), valsToFractions([10, 15, 20]))
print(l2exact.evaluate(12))