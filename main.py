import pygame
from board import Board 

class Game:
    LINE_NB = 4 # Number of lines on the board (must be even)
    shapeWidth = 90 # size of the shapes
    shapeHeight= 90 # size of the shapes
    borderSize= 3
    BG_COLOR = (36,36,36) # Background color
    COLORS = ["white","black","red","green","blue"]

    def __init__(self,colors,mode="tetra"):
        pygame.init()
        pygame.display.set_caption("Tetrahedron Game")
        self.updateMode(mode=mode)
        self.isWin = False

    def updateMode(self,mode="tetra"):
        self.board = Board(self.COLORS,self.LINE_NB,mode=mode)
        #if mode=="tetra" or True: #TODO implement mode octa
        self.screenWidth = self.shapeWidth+(self.shapeWidth/2+self.borderSize)*(self.board.grid.grid.shape[1]-1)
        self.screenHeight = (self.shapeHeight+self.borderSize)*self.board.grid.grid.shape[0]-self.borderSize
        self.screen = pygame.display.set_mode((self.screenWidth,self.screenHeight))
        self.running = True #Execute the program until the user closes the window

    def drawShape(self,i,j):
        color = self.COLORS[int(self.board.grid.grid[i,j])]
        #if self.mode=="tetra" or True: #TODO implement mode octa
        centerX = 0.5*self.shapeWidth+j/2*self.shapeWidth+j*self.borderSize
        centerY = 0.5*self.shapeHeight+i*self.shapeHeight+i*self.borderSize
        if self.board.grid.isCaseUp(i,j):
            points = [
                    (centerX,centerY-0.5*self.shapeHeight),
                    (centerX+0.5*self.shapeHeight,centerY+0.5*self.shapeHeight),
                    (centerX-0.5*self.shapeHeight,centerY+0.5*self.shapeHeight)
                    ]
        else:
            points = [
                    (centerX,centerY+0.5*self.shapeHeight),
                    (centerX+0.5*self.shapeHeight,centerY-0.5*self.shapeHeight),
                    (centerX-0.5*self.shapeHeight,centerY-0.5*self.shapeHeight)
                    ]
        pygame.draw.polygon(self.screen,color,points)

    def drawPiece(self,i,j):
        color = self.COLORS[int(self.board.grid.grid[i,j])]
        #if self.mode=="tetra" or True: #TODO implement mode octa
        centerX = 0.5*self.shapeWidth+j/2*self.shapeWidth+j*self.borderSize
        centerY = 0.5*self.shapeHeight+i*self.shapeHeight+i*self.borderSize
        center = centerX,centerY
        lowerLeft = centerX-0.5*self.shapeHeight,centerY+0.5*self.shapeHeight
        upperLeft = centerX-0.5*self.shapeHeight,centerY-0.5*self.shapeHeight
        lowerRight= centerX+0.5*self.shapeHeight,centerY+0.5*self.shapeHeight
        upperRight= centerX+0.5*self.shapeHeight,centerY-0.5*self.shapeHeight
        lowerMiddle= centerX,centerY+0.5*self.shapeHeight
        upperMiddle= centerX,centerY-0.5*self.shapeHeight
        if self.board.grid.isCaseUp(i,j):
            leftFace = [upperMiddle,center,lowerLeft]
            rightFace = [upperMiddle,center,lowerRight]
            otherFace = [lowerLeft,center,lowerRight]
        else:
            leftFace = [upperLeft,center,lowerMiddle]
            rightFace = [upperRight,center,lowerMiddle]
            otherFace = [upperLeft,center,upperRight]
        leftColor = self.COLORS[int(self.board.playerPiece.faces["left"])]
        rightColor = self.COLORS[int(self.board.playerPiece.faces["right"])]
        otherColor = self.COLORS[int(self.board.playerPiece.faces["other"])]
        pygame.draw.polygon(self.screen,leftColor,leftFace)
        pygame.draw.polygon(self.screen,rightColor,rightFace)
        pygame.draw.polygon(self.screen,otherColor,otherFace)
        if self.board.grid.isCaseUp(i,j):
            pygame.draw.polygon(self.screen,"black",[lowerLeft,center],width=3)
            pygame.draw.polygon(self.screen,"black",[lowerRight,center],width=3)
            pygame.draw.polygon(self.screen,"black",[upperMiddle,center],width=3)
        else:
            pygame.draw.polygon(self.screen,"black",[upperLeft,center],width=3)
            pygame.draw.polygon(self.screen,"black",[upperRight,center],width=3)
            pygame.draw.polygon(self.screen,"black",[lowerMiddle,center],width=3)

    def render(self):
        self.screen.fill(self.BG_COLOR)
        playerX,playerY = self.board.playerPosition
        for i,j in self.board.grid.validIndices:
            self.drawShape(i,j)
        self.drawPiece(playerX,playerY)
        pygame.display.update()

    def verifyEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.board.isValidMove(direction="left"):
                    self.board.move(direction="left")
                elif event.key == pygame.K_RIGHT and game.board.isValidMove(direction="right"):
                    self.board.move(direction="right")
                elif event.key == pygame.K_UP and game.board.isValidMove(direction="up"):
                    self.board.move(direction="up")
                elif event.key == pygame.K_DOWN and game.board.isValidMove(direction="down"):
                    self.board.move(direction="down")

    def displayMessage(self,msg):
        #  font_style = pygame.font.SysFont(None,100)
        #  renderedMsg = font_style.render(msg,True,"red")
        #  self.screen.blit(renderedMsg,[self.screenWidth/2,self.screenHeight/2])
        print(msg)

    def wantsToContinue(self):
        prompt = "Do you want to play again ? (y/n) "
        while True:
            try:
               return {"y":True,"n":False}[input(prompt).lower()]
            except KeyError:
               print("Invalid input please enter True or False!")


if __name__ == "__main__":
    # !!! Default case color value first
    colors = ["white","black","red","green","blue"]
    wantsToContinue = True
    while wantsToContinue:
        #Create Game
        game = Game(colors,mode="tetra")

        #Game loop
        while game.running:
            # Verify Pygame events
            game.verifyEvents()

            # Display the board
            game.render()

            # Check if the player has won
            if game.board.checkWin():
                game.displayMessage("You Won!")
                pygame.time.delay(200)
                game.running = False

            # Wait
            pygame.time.delay(200)

        # Quit Pygame
        pygame.quit()

        #Ask the user to play again 
        wantsToContinue = game.wantsToContinue()
