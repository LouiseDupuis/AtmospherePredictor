# an automated class to solve a disposition based on input
import gridstate

#  testing

testGridSimple = gridstate.gridState(7, 5)
print("Simple grid :")
testGridSimple.printGrid()

testGridInput = gridstate.gridState(0, 0, input="./testread.txt")
print("Input grid :")
testGridInput.printGrid()

testGridInput._setGridFromNumGrid()

testGridInput._initializeNumGrid()

testGridInput.printGrid()

testGridInput._setNumGridFromGrid()

testGridInput.printGrid()

testGridInput.solveGrid()

testGridInput.printGrid()