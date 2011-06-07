__author__="rishi"
__date__ ="$Jun 3, 2011 1:07:46 AM$"

"""The building block of SET."""

class Card:

    def __init__(self, shad, shap, col, num, imgnum=None):
        """
        Initializes the Card object
        @param shad = shading of the shapes
        @param shap = the type of shape on the card
        @param col = color of the shapes
        @param num = number of shapes on the card
        @param imgnum = optional parameter whos image is represented by the file number in images/
        """
        self.color = col
        self.shape = shap
        self.number = str(num)
        self.shading = shad
        self.imgnum = str(imgnum) #Image number of the card according to the images/ directory.

#    def __str__(self):
#        cardstr = 'Color:' + self.color + ' Shape:' + self.shape + ' Number:' + self.number + ' Shading' + self.shading + ' Image No.' + self.imgnum
#        return cardstr