import string
from exceptions import *

class Grid:
    """The class used for everything regarding the grid used to hold boats and/or strikes."""
    def __init__(self, kind: int, rows: int, cols: int):
        self.kind = kind
        self.cells = []

        if kind == 0:
            self.boats = []

        for i in range(0, rows):
            self.cells.append([])
            for j in range(0, cols):
                self.cells[i].append(None)

    def removeBoat(self, boat):
        newCells = []
        for i in self.cells:
            newLine = [j if not j == boat else None for j in i]
            newCells.append(newLine)
        self.cells = newCells

    def putBoat(self, boat):
        """Takes a Boat object and puts it on the Boat.xPos, Boat.yPos position rotated by Boat.turnid"""
        if self.kind == 1:
            raise NotPlayerGrid('Tried to place boat on the wrong grid')

        for i in range(0, boat.length):
            if boat.turnid == 0:
                if self.cells[boat.yPos - i][boat.xPos] is None:
                    if not self.boatAround([boat.yPos - i, boat.xPos], boatToCheck=boat):
                        self.cells[boat.yPos - i][boat.xPos] = boat
                        boat.occupies.append([boat.yPos - i, boat.xPos])
                        if not self.boats.__contains__(boat):
                            self.boats.append(boat)
                    else:
                        raise NextToBoat('Boat with id: ' + str(boat.kind) + 'could not be placed on:',
                                         [boat.yPos, boat.xPos], 'with rotation of', boat.turnid)
                else:
                    raise SpaceOccupied('Boat with id: ' + str(boat.kind) + 'could not be placed on:',
                                        [boat.yPos, boat.xPos], 'with rotation of', boat.turnid)
            elif boat.turnid == 1:
                if self.cells[boat.yPos][boat.xPos + i] is None:
                    if not self.boatAround([boat.yPos, boat.xPos + i], boatToCheck=boat):
                        self.cells[boat.yPos][boat.xPos + i] = boat
                        boat.occupies.append([boat.yPos, boat.xPos + i])
                        if not self.boats.__contains__(boat):
                            self.boats.append(boat)
                    else:
                        raise NextToBoat('Boat with id: ' + str(boat.kind) + 'could not be placed on:',
                                         [boat.yPos, boat.xPos], 'with rotation of', boat.turnid)
                else:
                    raise SpaceOccupied('Boat with id: ' + str(boat.kind) + 'could not be placed on:',
                                         [boat.yPos, boat.xPos], 'with rotation of', boat.turnid)
            elif boat.turnid == 2:
                if self.cells[boat.yPos + i][boat.xPos] is None:
                    if not self.boatAround([boat.yPos + i, boat.xPos], boatToCheck=boat):
                        self.cells[boat.yPos + i][boat.xPos] = boat
                        boat.occupies.append([boat.yPos + i, boat.xPos])
                        if not self.boats.__contains__(boat):
                            self.boats.append(boat)
                    else:
                        raise NextToBoat('Boat with id: ' + str(boat.kind) + 'could not be placed on:',
                                         [boat.yPos, boat.xPos], 'with rotation of', boat.turnid)
                else:
                    raise SpaceOccupied('Boat with id: ' + str(boat.kind) + 'could not be placed on:',
                                        [boat.yPos, boat.xPos], 'with rotation of', boat.turnid)
            elif boat.turnid == 3:
                if self.cells[boat.yPos][boat.xPos - i] is None:
                    if not self.boatAround([boat.yPos, boat.xPos - i], boatToCheck=boat):
                        self.cells[boat.yPos][boat.xPos - i] = boat
                        boat.occupies.append([boat.yPos, boat.xPos - i])
                        if not self.boats.__contains__(boat):
                            self.boats.append(boat)
                    else:
                        raise NextToBoat('Boat with id: ' + str(boat.kind) + 'could not be placed on:',
                                         [boat.yPos, boat.xPos], 'with rotation of', boat.turnid)
                else:
                    raise SpaceOccupied('Boat with id: ' + str(boat.kind) + ' could not be placed on: ',
                                        [boat.yPos, boat.xPos], ' with rotation of: ', boat.turnid)
            else:
                raise InvalidTurnID('TurnID of boat was not in interval [0, 3]')

    def boatAround(self, coords: list, boatToCheck=None):
        """Checks if there is a boat right next to passed coordinates.
        Takes a list in the form of [y, x]
        """
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if self.cells[coords[0] + i][coords[1] + j] is None:
                        continue
                    elif boatToCheck is None:
                        return True
                    elif boatToCheck.isOn([coords[0] + i, coords[1] + j]):
                        continue
                except IndexError:
                    continue

        return False

class Boat:
    """Class for all things related to the boat object"""
    def __init__(self, kind: int, xPos: int, yPos: int, turned: int):
        self.kind = kind
        self.xPos = xPos
        self.yPos = yPos
        self.turnid = turned
        self.broken = False
        self.occupies = []

        if kind == 0:
            self.length = 5
        elif kind == 1:
            self.length = 4
        elif kind == 2 or kind == 3:
            self.length = 3
        elif kind == 4:
            self.length = 2
        elif kind > 5:
            self.length = kind


    def isOn(self, coords: list):
        """Checks if the boat is on specified location, takes a list [y, x]"""
        return self.occupies.__contains__(coords)


def toCoords(instruction: str):
    """Takes position like A4 or E7 and converts it to coordinates for use on the grid"""
    if len(instruction) > 2:
        raise InvalidInstruction('instruction can only consist of a letter and a number, separated by a whitespace')

    instruction = instruction.split()
    alphabet = list(string.ascii_uppercase)
    for i, item in enumerate(alphabet):
        if instruction[0] == item:
            instruction[0] = i + 1
        else:
            continue

        return [int(instruction[i]) for i, item in enumerate(instruction)]  #return the coords as integers
