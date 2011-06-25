__author__="rishi"
__date__ ="$Jun 6, 2011 4:17:08 AM$"

class Card(object):

    pixelWidth = 95
    pixelHeight = 62

    attrdict = {'color':['red','purple','green'],
                'shading':['solid','stripped','open'],
                'shape':['squiggle','diamond','oval'],
                'number':['one','two','three'] }

    def __init__(self, col, shap, num, shad):

        ##
        #Initializes the Card object (All field will have the value 0, 1, or 2)
        #@param shad = shading of the shapes (0=solid,1=stripped,2=open)
        #@param shap = the type of shape on the card (0=Squiggle,1=Diamond,2=Oval)
        #@param col = color of the shapes (0=Red,1=Purple,2=Green)
        #@param num = number of shapes on the card (0=1,1=2,2=3)

        self.color = col
        self.shape = shap
        self.number = num
        self.shading = shad

    def getCardImgNumber(self):

        return (27*self.shading + 9*self.shape + 3*self.color + self.number)

    def __setattr__(self, key, value):
        assert type(value) == int
        if value > 2 or value < 0:
            return
        self.__dict__[key] = value

    def __str__(self):
        return 'Color: %d, Shape: %d, Number: %d, Shading: %d\n' % (self.color,self.shape,self.number,self.shading)