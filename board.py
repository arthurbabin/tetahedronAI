from grid import TetraGrid
from coloredPiece import ColoredTetahedron

class Board:
    """
    Python Class representing the board of the Tetahedron game
    """

    def __init__(self,colors,n,mode="tetra"):
        """
        Create a board with [n] lines ([n] must be even)

        :colors: list of the possible colors of the board, the first one being the default case color (beware of the number of colors depending on the selected mode)
        :n: number of lines the board's grid has
        :mode: "tetra" (or "octa" but not implemented yet) corresponding to the shape of the piece the player wants to play with
        """
        assert n%2==0, "[n] must be even"
        self.colors = colors
        self.mode = mode

        #Creation of a Grid and a ColoredPiece according to the selected mode
        if self.mode=="tetra":
            self.grid = TetraGrid(n)
            self.playerPiece = ColoredTetahedron(defaultColor=0)
            self.playerPosition = (1,n-1)
            assert len(colors)==5
        else:
            #TODO implement OctaGrid and ColoredOctahedron
            #for octa mode
            self.grid = TetraGrid(n) 
            self.playerPiece = ColoredTetahedron(defaultColor=0)
            self.playerPosition = (1,n-1)
            assert len(colors)==9

        #Definition of attributes for color values
        self.numberOfColors = len(self.colors)-1 # default color does not count
        self.outOfBoardCaseValue = -1
        self.defaultCaseValue = 0
        self.underPlayerPieceCaseValue = 0

        #Place the player on the grid
        self.grid.changeValue(
                self.playerPosition[0],
                self.playerPosition[1],
                0.5 # special value to represent the player's piece on the board
                )

        #Place the color cases on the grid where the board is free
        self.randomizeColorCases()

    def randomizeColorCases(self):
        """
        The color cases are randomly selected among the cases with value [defaultValue] and set to the possible colors (one for each color of the board except the default color)

        :return: nothing
        """
        #  (worked but does not always give a solution)
        #  randomSelection = self.grid.selectRandomCases(
        #          number=self.numberOfColors,
        #          wantedValue=self.defaultCaseValue
        #          )

        # Use Edge coloring to find positions for the cases with a solution
        # for the game
        randomSelection = self.grid.selectRandomCasesBasedOnEdgeColoring(
                wantedValue=0
                )
        assert len(self.colors)-1==len(randomSelection)
        c = 1 #skip the default color by starting at position 1
        for i,j in randomSelection:
            self.grid.changeValue(i,j,c)
            c+=1

    def isValidMove(self,direction="left"):
        """
        Return if the player can move toward [direction]

        :direction: direction string (either left,right,up or down)
        :return: a boolean
        """
        i,j = self.playerPosition
        return self.grid.isValidMove(i,j, direction,self.outOfBoardCaseValue)

    def move(self,direction="left"):
        """
        Update the Board according to the player's move
        (We suppose that the move is valid)

        :direction: direction string (either left,right,up or down)
        :return: nothing
        """
        print("move",direction)
        # 1. Compute destination position and color
        i,j = self.playerPosition
        destPosX,destPosY = self.grid.getDestinationPosition(
                i,
                j,
                direction
                )
        destColor = self.grid.grid[destPosX,destPosY]

        # 2. Update the player's piece according to the move
        changedColor = self.playerPiece.move(direction,destColor)
        self.grid.changeValue(destPosX,destPosY,0.5)

        # 3. Update the case that was under the player's piece
        self.grid.changeValue(i,j,self.underPlayerPieceCaseValue)

        # 4. Keep in memory the new value of the case under the player's piece
        self.underPlayerPieceCaseValue = changedColor

        self.playerPosition = destPosX,destPosY

    def render(self):
        """
        Render the board with Pygame
        """
        #TODO

    def checkWin(self):
        """
        Return True if the player has won False otherwise

        :return: a boolean
        """
        return self.playerPiece.isFullyColored()
