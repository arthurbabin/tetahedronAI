import abc #Module for POO

class AbstractColoredPiece(abc.ABC):
    """
    Abstract Class representing a colored 3D shape that can roll
    and exchange its colors with a board
    """

    @abc.abstractproperty
    def defaultColor(self):
        """
        Default color value to get rid of on the piece (goal of the game)
        """
        return 0 

    @abc.abstractproperty
    def faces(self):
        """
        Faces dictionnary storing the name and the value of each face
        """
        return {} 

    @abc.abstractmethod
    def move(self,direction,colorOfDestination):
        """
        Update the object according to the move and return the new color of the
        destination case (because when the Tetahedron touches the board it
        changes its color with the corresponding case)

        :direction: the direction string (either left, right, up or down)
        :colorOfDestination: the color value (integer) of the destination case
        :return: nothing
        """
        pass

    def isFullyColored(self):
        """
        Return True if all its faces are different from the default color

        :return: a boolean
        """
        return self.defaultColor not in self.faces.values()

class ColoredTetahedron(AbstractColoredPiece):
    """
    Python Class to represent a colored Tetahedron
    It can roll left, right and up if it is pointing down
    Or left, right and down if it is pointing up

    Then in this class we will call 
    "left" the face oriented to the left,
    "right" the face oriented to the right,
    "board" the face of the tetahedron that touches the board,
    and "other" the remaining face.
    """
    defaultColor = None
    faces = None

    def __init__(self,defaultColor=0):
        """
        Creation of the ColoredTetahedron, it is considered fully colored when all its faces are different from [defaultColor]

        :defaultColor: the color value that the player wants to get rid of
        """
        self.defaultColor = defaultColor
        self.faces = {
            "board":self.defaultColor, # color of the face touching the board
            "left":self.defaultColor, # color of the face oriented to left
            "right":self.defaultColor, # color of the face oriented to right
            "other":self.defaultColor # color of the remaining face
        }

    def move(self,direction,colorOfDestination):
        """
        Update the object according to the move and return the new color of the destination case (because when the Tetahedron touches the board it changes its color with the corresponding case)
        
        :direction: the direction string (either left, right, up or down)
        :colorOfDestination: the color value (integer) of the destination case
        :return: nothing
        """
        left,right,board,other=self.faces["left"],self.faces["right"],self.faces["board"],self.faces["other"]
        
        #The board face takes the destination color
        self.faces["board"]=colorOfDestination

        #rotate the tetahedron and return the value of the color that was 
        #previously oriented towards the direction
        if direction=="left":
            self.faces["left"]=other
            self.faces["right"]=board
            self.faces["other"]=right
            return left
        elif direction=="right":
            self.faces["left"]=board
            self.faces["right"]=other
            self.faces["other"]=left
            return right
        elif direction=="up" or direction=="down":
            self.faces["other"]=board
            return other
        else:
            raise ValueError("Direction not valid")

if __name__ == "__main__":
    tetra = ColoredTetahedron()
    print(tetra.faces)
