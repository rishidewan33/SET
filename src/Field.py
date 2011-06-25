__author__="rishi"
__date__ ="$Jun 7, 2011 11:44:21 PM$"

##An abstract representation of a set of cards laid out on a table for the
# user to pick Sets from.
#
class Field(object):

    ##Initializes a 2-dimensional array for the representation of the field
    #
    ##@var cardField
    # The 2D Array representation of cards laid out on a field.
    def __init__(self,row,col):

        self.cardField = [[None for c in xrange(col)] for r in xrange(row)]

    ##Returns the number of rows in the field
    #
    def rows(self):

        return len(self.cardField)

    ##Returns the number of columns in the field
    #
    def cols(self):

        return len(self.cardField[0])

    ##When a new game is started, we will create a new 2D array.
    #
    def reset(self,row,col):

        self.cardField = [[None for c in xrange(col)] for r in xrange(row)]

    ##Removes a row of cards for the game object to pick up when resetting the game.
    #
    def pop(self):

        return self.cardField.pop()

    ##Operator overload for array indexing
    #
    def __getitem__(self,i):

        return self.cardField[i]

    ##Operator overload for length acquisition
    #
    def __len__(self):

        return len(self.cardField)

    ##Operator overload for string representation
    #
    def __str__(self):

        output = ''
        for i in range(len(self.cardField)):
            for j in range(len(self.cardField[0])):
                output += str(self.cardField[i][j])
            output+='\n'
        return output
