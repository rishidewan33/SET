
__author__="rishi"
__date__ ="$Jun 6, 2010 4:09:32 PM$"

from Card import Card
from Game import Game
import Tkinter
from Tkinter import Tk
from Tkinter import Menu
from Tkinter import Button
from Tkinter import Checkbutton
from Tkinter import Label
from Tkinter import PhotoImage
from tkMessageBox import showinfo
from Tkinter import Toplevel

class GUIHandler:

    screenwidth = 0
    screenheight = 0
    windowwidth = 0
    windowheight = 0

    ## Initializes the GUI setup of the program.
    #
    def __init__(self,game):

        assert type(game) is Game
        self.root = Tk()
        self.root.title('SET')
        self.root.resizable(0,0)
        self.buttonField = None
        self.checkButtonField = None
        self.Game = game
        self.Field = game.Field
        assert self.Game
        assert self.Field
        GUIHandler.screenwidth = self.root.winfo_screenwidth()
        GUIHandler.screenheight = self.root.winfo_screenheight()
        GUIHandler.windowwidth = GUIHandler.screenwidth // 3
        GUIHandler.windowheight = GUIHandler.screenheight // 1.5


        self.root.geometry('%dx%d+%d+%d' % (GUIHandler.windowwidth,
                                          GUIHandler.windowheight,
                                          self.root.winfo_screenwidth()/8,
                                          self.root.winfo_screenheight()/8))

        menu = Menu(self.root)

        gamemenu = Menu(menu,tearoff=0)
        gamemenu.add_command(label='New Game',command=lambda:self.startNewGame(),accelerator="F2")
        gamemenu.add_command(label='Leaderboards',command=lambda:showinfo("Not implemented","Feature not implemented...yet."))
        gamemenu.add_command(label='Exit',command=lambda:self.root.destroy(),accelerator="Alt-F4")

        menu.add_cascade(label='Game',menu=gamemenu)

        settingmenu = Menu(menu,tearoff=0)

        gamedifficulty = Menu(settingmenu,tearoff=0)
        gamedifficulty.add_radiobutton(label='Beginner',command=lambda :self.changeGameDifficulty(0,True),accelerator="B")
        gamedifficulty.add_radiobutton(label='Novice',command=lambda :self.changeGameDifficulty(0,False),accelerator="N")
        gamedifficulty.add_radiobutton(label='Advanced',command=lambda :self.changeGameDifficulty(1,False),accelerator="A")

        settingmenu.add_cascade(label='Game Difficulty',menu=gamedifficulty)

        timedmode = Menu(settingmenu,tearoff=0)
        timedmode.add_radiobutton(label='On',command=lambda:showinfo("Not implemented","Feature not implemented...yet."))
        timedmode.add_radiobutton(label='Off',command=lambda:showinfo("Not implemented","Feature not implemented...yet."))
        
        settingmenu.add_cascade(label='Timed Mode',menu=timedmode)

        timeddifficulty = Menu(settingmenu,tearoff=0)
        timeddifficulty.add_radiobutton(label='Easy',accelerator="E")
        timeddifficulty.add_radiobutton(label='Medium',accelerator="M")
        timeddifficulty.add_radiobutton(label='Hard',accelerator="H")

        settingmenu.add_cascade(label='Timed Difficulty',menu=timeddifficulty)
        menu.add_cascade(label='Settings',menu=settingmenu)

        helpmenu = Menu(menu,tearoff=0)
        helpmenu.add_command(label='About SET',command=lambda:showinfo("Not implemented","Feature not implemented...yet."))

        menu.add_cascade(label='Help',menu=helpmenu)

        self.root.config(menu=menu)

        self.root.bind('<F2>',lambda e:gamemenu.invoke(0))
        self.root.bind('L',lambda e:gamemenu.invoke(1))
        self.root.bind('<Alt-F4>',lambda e:gamemenu.invoke(2))
        self.root.bind('b',lambda e:gamedifficulty.invoke(0))
        self.root.bind('n',lambda e:gamedifficulty.invoke(1))
        self.root.bind('a',lambda e:gamedifficulty.invoke(2))




        self.remainderLabel = Label(self.root,text="There are %d set(s) remaining on the board." % self.Game.numSetsTotal,bg="white",relief=Tkinter.RAISED,font=('Helvetica',12))
        self.remainderLabel.place(x=(GUIHandler.windowwidth-self.remainderLabel.winfo_reqwidth())//2,y=3*GUIHandler.windowheight//4)

        timer = Label(self.root,text="Untimed Mode",bg="green",relief=Tkinter.RAISED,font=('Helvetica',12))
        timer.place(x=(GUIHandler.windowwidth-timer.winfo_reqwidth())//2,y=3*GUIHandler.windowheight//4.5)

        hintbutton = Button(text="Hint, please!",font=("Helvetica",12),command=lambda :showinfo("Not implemented","Feature not implemented...yet."))
        hintbutton.place(x=(GUIHandler.windowwidth-hintbutton.winfo_reqwidth())//2,y=3*GUIHandler.windowheight//3.5)

        self.userSetsCreated = Toplevel(self.root)
        self.userSetsCreated.title("Sets Created")
        self.userSetsCreated.geometry("%dx%d+%d+%d" % (Card.pixelWidth*3,
                                               self.userSetsCreated.winfo_screenheight(),
                                               self.root.winfo_pointerx()+self.userSetsCreated.winfo_reqwidth(),0))
        self.userSetsCreated.protocol("WM_DELETE_WINDOW",0)
        self.userSetsCreated.resizable(0,0)
        self.root.focus_set()

        self.updateCardsOnField(self.Field)

    ## Process the card location that the user picked. The function calls the game instance's addCardChoice method
    # to get a callback on the result of adding the card choice.
    def processCardChoice(self,i):

        cbutton = self.checkButtonField[i//self.Field.cols()][i%self.Field.cols()]
        cbutton.select()
        result = self.Game.addCardChoice(i)

        if result == 3:
            cbutton.deselect()
            return
        elif not result:
            return

        if result == 2: #Case 1: 3 choices were made and the Game object verified them as a set.
            showinfo("Good Job!","You made a set!")
            self.remainderLabel.config(text="There are %d set(s) remaining on the board." % self.Game.numSetsRemaining())
            if not self.Game.numSetsRemaining():
                showinfo("WINNER!","Congratulations! You found all sets!")
                self.disableButtons()
        elif result == 1: #Case 2: 3 choices were made but the user has made this set before in the game.
            showinfo("Repeat","You've already made this set")
        elif type(result) == tuple: #Case #3: 3 choices were made but they didn't form a set.
            assert len(result) == 2
            showinfo("Not a set","Not a set because 2 are %s and 1 is %s" % (result[0],result[1]))
        for i in self.checkButtonField:
            for j in i:
                j.deselect()

    def disableButtons(self):
        for i in self.buttonField:
            for j in i:
                j.config(state=Tkinter.DISABLED)
        for i in self.checkButtonField:
            for j in i:
                j.config(state=Tkinter.DISABLED)

    #Hard Coded lists of button widgets because python won't let me generate each of the Buttons' command
    #feature correctly.

    def setupNoviceField(self):

        self._destroyAllButtons() if self.buttonField else None

        self.buttonField = [[Button(self.root,command=lambda :self.processCardChoice(0)),
                             Button(self.root,command=lambda :self.processCardChoice(1)),
                             Button(self.root,command=lambda :self.processCardChoice(2))],
                            [Button(self.root,command=lambda :self.processCardChoice(3)),
                             Button(self.root,command=lambda :self.processCardChoice(4)),
                             Button(self.root,command=lambda :self.processCardChoice(5))],
                            [Button(self.root,command=lambda :self.processCardChoice(6)),
                             Button(self.root,command=lambda :self.processCardChoice(7)),
                             Button(self.root,command=lambda :self.processCardChoice(8))]]

        self.checkButtonField = [[Checkbutton(self.root,command=lambda :self.processCardChoice(0)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(1)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(2))],
                                 [Checkbutton(self.root,command=lambda :self.processCardChoice(3)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(4)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(5))],
                                 [Checkbutton(self.root,command=lambda :self.processCardChoice(6)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(7)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(8))]]


    def setupAdvancedField(self):

        self._destroyAllButtons() if self.buttonField else None

        self.buttonField = [[Button(self.root,command=lambda :self.processCardChoice(0)),
                             Button(self.root,command=lambda :self.processCardChoice(1)),
                             Button(self.root,command=lambda :self.processCardChoice(2)),
                             Button(self.root,command=lambda :self.processCardChoice(3))],
                            [Button(self.root,command=lambda :self.processCardChoice(4)),
                             Button(self.root,command=lambda :self.processCardChoice(5)),
                             Button(self.root,command=lambda :self.processCardChoice(6)),
                             Button(self.root,command=lambda :self.processCardChoice(7))],
                            [Button(self.root,command=lambda :self.processCardChoice(8)),
                             Button(self.root,command=lambda :self.processCardChoice(9)),
                             Button(self.root,command=lambda :self.processCardChoice(10)),
                             Button(self.root,command=lambda :self.processCardChoice(11))]]

        self.checkButtonField = [[Checkbutton(self.root,command=lambda :self.processCardChoice(0)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(1)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(2)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(3))],
                                 [Checkbutton(self.root,command=lambda :self.processCardChoice(4)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(5)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(6)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(7))],
                                 [Checkbutton(self.root,command=lambda :self.processCardChoice(8)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(9)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(10)),
                                  Checkbutton(self.root,command=lambda :self.processCardChoice(11))]]

    def updateCardsOnField(self,cardField):

        rows = cardField.rows()
        cols = cardField.cols()

        if cols == 3:
            self.setupNoviceField()
        elif cols == 4:
            self.setupAdvancedField()
        else:
            raise IndexError("CardField argument has illegal number of columns")

        assert len(self.buttonField) == rows
        assert len(self.buttonField[0]) == cols

        spacing = (GUIHandler.windowwidth-(cols * Card.pixelWidth) - 5) / (cols-1)
        x,y = 0,0
        cbwidth = self.checkButtonField[0][0].winfo_reqwidth()
        for i in xrange(rows):
            for j in xrange(cols):
                pic = PhotoImage(file='../media/%s.gif' % str(cardField[i][j].getCardImgNumber()))
                self.buttonField[i][j].config(image=pic)
                self.buttonField[i][j].image = pic
                self.buttonField[i][j].place(x=x,y=y)
                self.checkButtonField[i][j].place(x=x + Card.pixelWidth//2 - cbwidth//4,y=(y+Card.pixelHeight+10))
                x += Card.pixelWidth + spacing
            y += Card.pixelHeight + 40
            x = 0

    def startNewGame(self):

        self.Game.resetGame()
        self.updateCardsOnField(self.Game.Field)
        self.remainderLabel.config(text="There are %d set(s) remaining on the board." % self.Game.numSetsTotal)
        ##print self.Game.setsListTotal
        
    def _destroyAllButtons(self):

        for i in self.buttonField:
            for j in i:
                j.destroy()
        for i in self.checkButtonField:
            for j in i:
                j.destroy()

    def changeGameDifficulty(self,i,f):

        if self.Game.changeGameDifficulty(i,f):
            self.startNewGame()

    def run(self):

        self.root.mainloop()

if __name__ == "__main__":
    pass
