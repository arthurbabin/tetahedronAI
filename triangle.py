class Triangle:

    #initialisation of a Triangle
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color
        
    #Change the color of the Triangle
    def set_color(self, color):
        #only 4 colors are possible
        if color in ['blue', 'green', 'red', 'black']:
            self.color = color
        else:
            self.color = None

    #'delete' the color of the triangle 
    def set_color_none(self):
        self.set_color(self,"")
