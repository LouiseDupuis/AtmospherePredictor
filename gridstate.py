# a general description class to transfer grid states

import numpy as np

# general descriptors for agend state
idle = "N"
shouting = "S"
empty = "E"
lookupDict = {idle:1, shouting:2, empty:0}

class gridState:
    # the grid's dimensions
    width = None
    height = None

    # the grid in itself
    grid = None

    # a description file to read inputs (TODO)
    inputFile = None

    def __init__(self, width, height, input=None):
        if input:
            self.inputFile = input
            self.readInput()
            return

        self.width = width
        self.height = height
        self._initializeGrid();
        return

    def printGrid(self):
        print(self.grid)
        return

    def readInput(self):
        """format of file :
        <width>
        <height>
        table with format : <agent descriptor>, <agent descriptor>, ... \n
                            <agent descriptor>, <agent descriptor>, ... \n
                            etc"""
        if not self.inputFile:
            print("error in gridState : no input file")
            return
        with open(self.inputFile, "r") as file:
            lines = file.readlines()
            self.width = int(lines[0])
            self.height = int(lines[1])
            self._initializeGrid()
            for row in range(self.height):
                states = lines[2+row].strip('\n').split(',')
                for column in range(self.width):
                    self.grid[row, column] = lookupDict[states[column]]
        return




    #------------private functions---------------
    def _initializeGrid(self):
        if not self.width or not self.height:
            print("error in gridState : wrong dimensions")
            exit()
        self.grid = np.zeros([self.height, self.width])
        return