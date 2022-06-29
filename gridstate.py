# a general description class to transfer grid states

import numpy as np

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
from stade_grid import SingleGrid, StadeGrid
from stade_agents import StadeAgent, UltraAgent

# general descriptors for agend state
idle = "N"
shouting = "S"
empty = "E"
lookupDict = {idle:1, shouting:2, empty:0}
reverseLookupDict = {1:idle, 2:shouting, 0:empty}

class gridState(Model):
    # model stuff
    running = None
    schedule = None
    # the grid's dimensions
    width = None
    height = None

    # the grid in itself (a numpy io utils and the grid object)
    num_grid = None
    grid = None

    # a description file to read inputs (TODO)
    inputFile = None

    def __init__(self, width, height, input=None):
        self.running = True
        self.schedule = SimultaneousActivation(self)

        if input:
            self.inputFile = input
            self.readInput()
            return

        self.width = width
        self.height = height
        self._initializeNumGrid();
        return

    def printGrid(self):
        print(self.num_grid)
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
            self._initializeNumGrid()
            for row in range(self.height):
                states = lines[2+row].strip('\n').split(',')
                for column in range(self.width):
                    self.num_grid[row, column] = lookupDict[states[column]]
        return

    # "solve" the current loaded grid by iterating N times the model
    def solveGrid(self):
        """Je savais pas comment intégrer proprement ta classe
        stade_model à ta classe sans tout casser ^^'
        du coup j'ai reconstruit un truc a partir de ta version du modele"""
        if self.num_grid.any() == None:
            print("error : num_grid should be initialized")
            exit()
        self._setGridFromNumGrid()
        for i in range(10):
            self.schedule.step()
        self._setNumGridFromGrid()


    #------------private functions---------------
    def _initializeNumGrid(self):
        if not self.width or not self.height:
            print("error in gridState : wrong dimensions")
            exit()
        self.num_grid = np.zeros([self.height, self.width])
        return

    def _setGridFromNumGrid(self):
        if self.num_grid.any() == None:
            print("error in gridState uninitialized numGrid")
            exit()
        self.grid = StadeGrid(self.width, self.height, True)
        for row in range(self.height):
            for column in range(self.width):
                a = None
                if reverseLookupDict[self.num_grid[row, column]] == idle:
                    a = StadeAgent(self._getAgentId(row, column), self)
                if reverseLookupDict[self.num_grid[row, column]] == shouting:
                    a = StadeAgent(self._getAgentId(row, column), self)
                    a.set_state("S")
                if a:
                    self.schedule.add(a)
                    self.grid.place_agent(a, (column, row))

    def _setNumGridFromGrid(self):
        for row in range(self.height):
            for column in range(self.width):
                a = self.grid[column, row]
                if a:
                    self.num_grid[row, column] = lookupDict[a.get_state()]
                    # flush scheduler for re-use of the grid
                    self.schedule.remove(a)
                    del a
                else: #empy place
                    self.num_grid[row, column] = lookupDict[empty]


    def _getAgentId(self, row, column):
        return row * self.width + column