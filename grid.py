import numpy as np

class TetraGrid:
    """
    Python Class to representent a grid of triangles as a matrix. 
    Here each line of triangles is a succession of triangles facing up and triangle facing down.
    Moreover the corners have a value of -1 in order to form a hexagon globally
    """

    def __init__(self,n):
        """
        Creation of the HexGrid with [n] lines, initialized with zeros (beware of the corners that will have a -1 value)

        :n: the number of lines we want for the grid (must be even)
        """
        assert n%2==0, "[n] must be even"
        self.width = 2*n-1
        self.height = n
        self.grid = np.zeros((self.height,self.width))
        startingPoint = (n-2)//2

        # Cut the corners for the hexagonal shape of the grid
        for i in range(self.height):
            #Compute the starting point of the line as the distance
            #between the line and the nearest "center" line
            #by middle line we mean line that are supposed to be full
            #those are at position n//2 and position n//2+1
            startingPoint = min(abs(i-n//2),abs(i-n//2+1)) 
            endingPoint = self.width-1-startingPoint # the symetrical value
            for j in range(self.width):
                if (j<startingPoint or j>endingPoint):
                    self.grid[i,j] = -1
        indices = np.where(self.grid!=-1) #all the indices different from -1
        self.validIndices = list(zip(indices[0],indices[1])) #format indices into a list of tuples int,int

    def selectRandomCases(self,number=4,wantedValue=0):
        """
        Select randomly [number] cases from the cases wich values are
        in [possibleValues]

        :number: number of random cases to select
        :wantedValue: integer corresponding to the wanted value in the grid for the selection
        :return: list of (int,int) corresponding to the selection of cases
        """
        # Indices of cells with the desired value
        indices = np.argwhere(self.grid == wantedValue)

        # Random selection among the indices
        random_rows_ID= np.random.choice(indices.shape[0], 
                                  size=number, 
                                  replace=False)
        randomSelection=indices[random_rows_ID,:]

        return randomSelection

    def selectRandomCasesBasedOnEdgeColoring(self,wantedValue=0):
        """
        Select randomly [number] cases from the cases wich values are
        in [possibleValues]

        :number: number of random cases to select
        :wantedValue: integer corresponding to the wanted value in the grid for the selection
        :return: list of (int,int) corresponding to the selection of cases
        """
        chromaticNumber = 4
        # Indices of cells with the desired value
        indices = np.argwhere(self.grid == wantedValue)

        # Shuffle indices for randomness
        np.random.shuffle(indices)

        # Filter only K indices corresponding to K different colors on the coloring
        result = []
        seenValues = []
        i=0
        while len(result)!=chromaticNumber:
            val = self.chromaticIndex(indices[i][0],indices[i][1])
            if val not in seenValues:
                result.append(indices[i])
                seenValues.append(val)
            i+=1
        print(result,seenValues)

        return result 


    def chromaticIndex(self,i,j):
        if not j%2:
            if (i//2)%2 == (j//2)%2:
                return 1
            else: 
                return 2
        else:
            if ((i-1)//2)%2 == (j//2)%2:
                return 3
            else:
                return 4

    def changeValue(self,i,j, value):
        """
        Change the value of case [i,j] to [value]

        :i: line coordinate in the grid
        :j: column coordinate in the grid
        :value: new value of the case
        :return: nothing
        """
        self.grid[i,j] = value

    def isCaseUp(self,i,j):
        """
        Return if the case (which is an equilateral triangle) is facing up or not 

        :i: line coordinate in the grid
        :j: column coordinate in the grid
        :return: a boolean
        """
        n = self.height
        return ((i+j)%2 and not (n//2)%2) or (not (i+j)%2 and (n//2)%2)

    def isValidMove(self,i, j,direction="left",outOfBoardValue=-1):
        """
        Return if the player at [i,j] can move toward [direction]

        :i: origin line coordinate
        :j: origin column coordinate
        :direction: string corresponding to the direction chosen (either left, right, up or down)
        :outOfBoardValue: integer corresponding to the values of cases that are not on the board
        :return: boolean
        """
        #First verify if the origin coordinates are valid
        if i<0 or i>=self.height or j<0 or j>=self.width:
            return False

        #Then for each direction check if the destination case is on the board
        if direction=="left":
            return (j-1)>=0 and self.grid[i,j-1]!=outOfBoardValue
        elif direction=="right":
            return (j+1)<self.width and self.grid[i,j+1]!=outOfBoardValue
        #Special treatment for up and down direction because it depends on the orientation of origin case
        elif direction=="up":
            #Can't go up if the origin case is a triangle facing up
            return (i-1)>=0 and (not self.isCaseUp(i,j)) and self.grid[i-1,j]!=outOfBoardValue
        elif direction=="down":
            #Can't go down if the origin case is a triangle facing down
            return (i+1)<self.height and self.isCaseUp(i,j) and self.grid[i+1,j]!=outOfBoardValue
        else:
            raise ValueError("Direction not valid")

    def getDestinationPosition(self,i,j,direction="left"):
        """
        Return the position tuple starting from case [i,j] and following direction [direction]. The move is supposed to be valid.

        :i: origin line coordinate
        :j: origin column coordinate
        :direction: string corresponding to the direction chosen (either left, right, up or down)
        :return: int,int corresponding to the coordinates of the destination
        """
        if direction=="left":
            destPosY,destPosX = (i,j-1)
        elif direction=="right":
            destPosY,destPosX = (i,j+1)
        elif direction=="up":
            destPosY,destPosX = (i-1,j)
        elif direction=="down":
            destPosY,destPosX = (i+1,j)
        else:
            raise ValueError("Direction not valid")
        return destPosY,destPosX
