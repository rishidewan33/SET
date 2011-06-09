import Tkinter
from Tkinter import Button
from Tkinter import Checkbutton
from Tkinter import Label
from Tkinter import Menu
from Tkinter import PhotoImage
from Tkinter import RAISED
from Tkinter import Tk
from Tkinter import Toplevel

from Countdown import Countdown
from Deck import Deck
from Difficulty import *
from Game import Game

"""The Field class is the one of the main components of the game, this allows the user to see what's on the board in the GUI Program."""

class Field:

    def __init__(self, root):
        
        self.fld = [[None, None, None, None], [None, None, None, None], [None, None, None, None]]        
        self.cardfld = [[Label(root, relief=RAISED),
            Label(root, relief=RAISED),
            Label(root, relief=RAISED),
            Label(root, relief=RAISED)],
        [Label(root, relief=RAISED),
            Label(root, relief=RAISED),
            Label(root, relief=RAISED),
            Label(root, relief=RAISED)],
        [Label(root, relief=RAISED),
            Label(root, relief=RAISED),
            Label(root, relief=RAISED),
            Label(root, relief=RAISED)]]
        
        self.checkfld = [[Checkbutton(root, command=lambda:addChoice(0)),
            Checkbutton(root, command=lambda:addChoice(1)),
            Checkbutton(root, command=lambda:addChoice(2)),
            Checkbutton(root, command=lambda:addChoice(3))],
        [Checkbutton(root, command=lambda:addChoice(4)),
            Checkbutton(root, command=lambda:addChoice(5)),
            Checkbutton(root, command=lambda:addChoice(6)),
            Checkbutton(root, command=lambda:addChoice(7))],
        [Checkbutton(root, command=lambda:addChoice(8)),
            Checkbutton(root, command=lambda:addChoice(9)),
            Checkbutton(root, command=lambda:addChoice(10)),
            Checkbutton(root, command=lambda:addChoice(11))]]
            
        for i in xrange(len(self.fld)):
            for j in xrange(len(self.fld[i])):
                self.cardfld[i][j].place(x=j * 105, y=i * 100)
                self.checkfld[i][j].place(x=j * 105 + 35, y=i * 100 + 70)
                Label(root, text=str((4 * i) + j + 1), font=('Helvetica', 12)).place(x=j * 105 + 55, y=i * 100 + 70)

    def getCardAt(self, a, b):
        return self.fld[a][b]

    def clearButtons(self):

        for i in self.checkfld:
            for j in i:
                j.deselect()

    def createNewField(self, deck):
        counter = 0
        for i in xrange(len(self.fld)):
            for j in xrange(len(self.fld[i])):
                self.fld[i][j] = deck.dk[counter]
                img = PhotoImage(file="media/" + self.fld[i][j].imgnum + ".gif") #Creates an instance of an image.
                self.cardfld[i][j].config(image=img)
                self.cardfld[i][j].photo = img #Because we're doing image assignment in a function, it's good to keep a reference of the image when the function is done.
                counter += 1   

def switchTimedMode(boolVal):

    global timedMode
    
    if boolVal == timedMode:
        return
    timedMode = not timedMode

    if timedMode:
        if difficulty.difficulty == Difficulty.UNTIMED:
            difficulty.difficulty = Difficulty.EASY
    else:
        difficulty.difficulty = Difficulty.UNTIMED
    [[x.config(state=Tkinter.DISABLED) for x in y] for y in myField.checkfld]
    newGame()

def showAbout(): #This shows the About Section of SET.

    aboutpopup = Toplevel(root)
    aboutpopup.title('About SET')
    Label(aboutpopup, text="SET v2.0\nGame invented by Marsha Jean Falco\nSource Code written by Rishi Dewan\ncsmajor@mail.utexas.edu\nwww.setgame.com").pack()
    Button(aboutpopup,text="OK",command=aboutpopup.destroy).pack()
    sw = aboutpopup.winfo_screenwidth()
    sh = aboutpopup.winfo_screenheight()
    rw = aboutpopup.winfo_reqwidth()
    rh = aboutpopup.winfo_reqheight()
    aboutpopup.geometry("+%d+%d" % ((sw - rw) / 2, (sh -rh) / 2))
    aboutpopup.focus_set()

def addChoice(num):

    if num in cardChoices:
        cardChoices.remove(num)
    else:
        cardChoices.append(num)
        if len(cardChoices) == 3:
            cardChoices.sort()
            setPicked()

def setPicked():

    card1 = myField.getCardAt(cardChoices[0] // 4, cardChoices[0] % 4)
    card2 = myField.getCardAt(cardChoices[1] // 4, cardChoices[1] % 4)
    card3 = myField.getCardAt(cardChoices[2] // 4, cardChoices[2] % 4)

    if g.isSet(card1, card2, card3, root):
        if g.setExists([cardChoices[0], cardChoices[1], cardChoices[2]]): #If the user already made this set before in the current game, an error message will show.
            picked = Toplevel()
            picked.geometry('200x50-550+300')
            Label(picked, text="You've already made this Set.").pack()
            pbutton = Button(picked, text="OK", command=picked.destroy)
            pbutton.pack()
            picked.focus_set()
            picked.bind("<Return>", lambda e:picked.destroy())
            root.wait_window(picked)

        else:
            g.addSetMade([cardChoices[0], cardChoices[1], cardChoices[2]])
            made = Toplevel()
            made.title('Set Made')
            Label(made, text="Congrats. You just made a Set.").pack()
            Button(made, text="OK", command=made.destroy).pack()
            made.geometry('200x50-550+300')
            made.focus_set()
            made.bind("<Return>", lambda e:made.destroy())
            root.wait_window(made)
            numsets = g.checkFieldForSets(myField)
            setsleft = numsets-g.getNumSetsAcquired()
            update(setsMade, g.getNumSetsAcquired(), [card1, card2, card3])
            uisetsremain.config(text='There are ' + str(setsleft) + ' Set(s) remaining on the board.')
            if(setsleft == 0):
                congrats = Toplevel()
                congrats.geometry('-550+300')
                congrats.focus_set()
                if difficulty.difficulty == Difficulty.HARD:
                    Label(congrats, text="Very nice! You've found all of the Sets on Hard.").pack()
                elif difficulty.difficulty == Difficulty.MEDIUM:
                    Label(congrats, text="Alright! You found all of the Sets on Medium.\nSee if you can handle Hard.").pack()
                elif difficulty.difficulty == Difficulty.EASY:
                    Label(congrats, text="Congratulations! You've found all of the Sets.\nSee if you can take down Medium, or even Hard if you dare.").pack() #Message which congratulates the player.
                else:
                    Label(congrats, text="You've found all sets! You should try the game in Timed Mode.").pack()
                Button(congrats, text="Sweet!", command=congrats.destroy).pack()
                congrats.bind("<Return>", lambda e:congrats.destroy())
                uicountdown.config(text='WINNER!')
                try:
                    timerThread.killThreadFlag = True
                except:
                    pass
                [[x.config(state=Tkinter.DISABLED) for x in y] for y in myField.checkfld]
    myField.clearButtons()
    del cardChoices[:]


def update(setsMade, gsa, cards):

    """
    Mainly updates the setsMade window with a display of the set (of cards) that was recently made.
    """
    
    for i in xrange(3):
        img = PhotoImage(file='media/' + cards[i].imgnum + '.gif')
        label = Label(setsMade, image=img, relief=RAISED)
        label.photo = img
        label.place(x=100 * i, y=75 * (gsa-1))

def newGame():

    """
    Resets the field, the game (g) data, and wipes out the setsMade Toplevel window.
    """

    global timerThread

    [i.destroy() for i in setsMade.children.values()] #clear the setsMade window
    myField.clearButtons()
    myDeck.shuffleDeck()
    myField.createNewField(myDeck)
    g.new_game()
    del cardChoices[:]
    while True:
        numsets = g.checkFieldForSets(myField)
        if numsets == 0:
            myDeck.shuffleDeck()
            myField.createNewField(myDeck)
        else:
            #print [map(lambda x: x+1,i) for i in g.visited] #list of sets printed for testing purposes (a.k.a. Solutions)
            uisetsremain.config(text='There are ' + str(numsets) + ' Set(s) remaining on the board.')
            uisetsremain.place(x=(root.winfo_width()-uisetsremain.winfo_width())/2)
            if timedMode:
                try:
                    timerThread.setTime(numsets*difficulty.difficulty*10)
                except:
                    timerThread = Countdown(root,numsets*difficulty.difficulty*10,uicountdown,myField)
                try:
                    timerThread.start()
                except:
                    pass
            else:
                uicountdown.config(text='Untimed Mode')
                if timerThread is not None:
                    timerThread.killThreadFlag = True
            [[x.config(state=Tkinter.NORMAL) for x in y] for y in myField.checkfld]
            return

"""
Script to start up SET.
"""

root = Tk() #Creates an instance of the main GUI window (where most of the gameplay occurs).
gamewidth = 413
gameheight = 400

timedMode = False
timerThread = None

difficulty = Difficulty()

root.title('SET Game')
x = root.winfo_screenwidth()/4
y = root.winfo_screenheight()/4
root.geometry('413x400+%d+%d'%(x,y)) #The geometry of a window is basically set as 'widthxheight-xcoordinate+ycoordinate'

menu = Menu(root)
root.resizable(0, 0)
root.config(menu=menu)

gamemenu = Menu(menu, tearoff=0)
helpmenu = Menu(menu, tearoff=0)
settingsmenu = Menu(menu,tearoff=0)

menu.add_cascade(label='Game', menu=gamemenu)
menu.add_cascade(label='Settings', menu=settingsmenu)
menu.add_cascade(label='Help', menu=helpmenu)

timedmenu = Menu(menu,tearoff=0)
timedmenu.add_command(label='On', command=lambda:switchTimedMode(True))
timedmenu.add_command(label='Off', command=lambda:switchTimedMode(False))

difficultymenu = Menu(menu,tearoff=0)
difficultymenu.add_command(label='Easy',command=lambda:difficulty.setDifficulty(Difficulty.EASY))
difficultymenu.add_command(label='Medium',command=lambda:difficulty.setDifficulty(Difficulty.MEDIUM))
difficultymenu.add_command(label='Hard',command=lambda:difficulty.setDifficulty(Difficulty.HARD))

settingsmenu.add_cascade(label='Timed Mode',menu=timedmenu)
settingsmenu.add_cascade(label='Difficulty',menu=difficultymenu)

gamemenu.add_command(label='New Game', command=lambda:newGame(), accelerator="F2")
gamemenu.add_command(label='Exit', command=lambda:root.destroy(), accelerator="Alt+F4")

helpmenu.add_command(label='About SET', command=lambda:showAbout())

uisetsremain = Label(root)
uicountdown = Label(root,width=len('Untimed Mode'))
uisetsremain.place(x=33, y=310)
uicountdown.place(x=145, y=350)

setsMade = Toplevel(root)
setsMade.resizable(0, 0) #Makes the window's size unchangable.
setsMade.protocol("WM_DELETE_WINDOW", lambda: 0) #cannot exit the setsMade window
setsMade.title('Sets made so far')
setsMade.geometry('300x%d-300+10'%root.winfo_screenheight())

root.focus_set()
myDeck = Deck()
myField = Field(root) #In this case, we'll only create one instance of Field.
myField.createNewField(myDeck) #We'll just clears the field of cards and replaces the field with new cards (Replace the image of each label with another card).
g = Game()
cardChoices = []

while True: #initial instantiation of the game.
    numsets = g.checkFieldForSets(myField)
    if numsets == 0: #If the field checkers finds no sets. Do it again. (In here, we could just simply have a set numbers on the board, but it'd be really slow)
        myDeck.shuffleDeck()
        myField.createNewField(myDeck)
        g = Game()
    else:
        break

uisetsremain.config(text='There are ' + str(numsets) + ' Set(s) remaining on the board.', font=('Helvetica', 14), bg='white', relief=RAISED)
uicountdown.config(text = 'Untimed Mode',font=('Helvetica',14),bg='light grey', relief=RAISED)

root.bind("<F2>", lambda e:newGame()) #When user press F2, a new game starts.
root.bind("<Alt-F4>", lambda e:root.destroy()) #Pressing Alt-F4 exits the game.

root.mainloop() #starts the root GUI Window