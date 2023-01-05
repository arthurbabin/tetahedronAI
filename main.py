import pygame
import math
from board import Board 

class Game:
    LINE_NB = 4 # Number of lines on the board (must be even)
    shapeWidth = 30 # size of the shapes
    BG_COLOR = (0,0,0) # Background color
    COLORS = ["white","black","red","green","blue"]

    def __init__(self,colors,mode="tetra"):
        pygame.init()
        self.updateMode(mode=mode)

    def updateMode(self,mode="tetra"):
        self.board = Board(self.COLORS,self.LINE_NB,mode=mode)
        #if mode=="tetra" or True: #TODO implement mode octa
        self.shapeHeight = self.shapeWidth * math.sqrt(3)/2
        screenWidth = self.shapeWidth*self.board.grid.grid.shape[1]
        screenHeight = self.shapeHeight*self.board.grid.grid.shape[0]
        self.screen = pygame.display.set_mode((screenWidth,screenHeight))
        self.running = True #Execute the program until the user closes the window

    def drawShape(self,i,j):
        #if self.mode=="tetra" or True: #TODO implement mode octa
        posX,posY = i*self.shapeHeight,j*self.shapeWidth #upper left corner of the bounding box of the shape
        if self.board.grid.isCaseUp(i,j):
            points = [
                    (posX,posY+self.shapeHeight),
                    (posX+self.shapeWidth/2,posY),
                    (posX+self.shapeWidth,posY+self.shapeHeight)
                    ]
        else:
            points = [
                    (posX,posY),
                    (posX+self.shapeWidth/2,posY+self.shapeHeight),
                    (posX+self.shapeWidth,posY)
                    ]
        color = self.COLORS[self.board.grid.grid[i,j]]
        pygame.draw.polygon(self.screen,color,points)

    def drawPiece(self,i,j):
        pass

    def render(self):
        playerX,playerY = self.board.playerPosition
        for i,j in self.board.grid.validIndices:
            if i!=playerY or j!=playerX:
                self.drawShape(i,j)
        self.drawPiece(playerX,playerY)

    def verifyEvents(self):
        # Met en pause le programme pendant 1 seconde
        pygame.time.delay(1000)

        # Vérifie les événements de Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

# !!! Default case color value first
colors = ["white","black","red","green","blue"]
game = Game(colors,mode="tetra")
while(game.running):
    pass

