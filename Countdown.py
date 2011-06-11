import Tkinter
from Tkinter import Button
from Tkinter import Label
from Tkinter import Toplevel
import threading
import time

__author__="rishi"
__date__ ="$Jun 3, 2011 3:48:51 AM$"

class Countdown(threading.Thread): #Timer class for timed mode.

    def __init__(self,root,seconds,uiconfig,field):

        self.root = root
        self.seconds = seconds
        self.killThreadFlag = False #Flags that the timer must stop running.
        self.uicd = uiconfig #Reference to the countdown label
        self.field = field #Reference to the game field
        threading.Thread.__init__(self)

    def setTime(self,seconds):

        self.seconds = seconds
        self.uicd.config(text='%d:%02d'%(self.seconds//60,self.seconds%60))

    def run(self):

        """
        Only possible ways the thread timer must stop running:
        1. Timer hits 0:00 during Timed Mode (i.e. self.seconds == 0)
        2. User switches from Timed Mode to Untimed Mode
        3. User gets all of the sets in time.
        4. User exits program
        """
        try:
            [[x.config(state=Tkinter.NORMAL) for x in y] for y in self.field.checkfld] #Check buttons are enabled.
            self.uicd.config(text='%d:%02d'%(self.seconds//60,self.seconds%60)) #Display start time
            while self.seconds > 0 and not self.killThreadFlag:
                self.seconds-=1 #decrement time
                time.sleep(1.0) #wait for 1 seconds then continue.
                if self.killThreadFlag:
                    break
                self.uicd.config(text='%d:%02d'%(self.seconds//60,self.seconds%60)) #display decremented time.
            if self.seconds == 0: #If time ran out during timed mode, we display a message saying the player loses.
                [[x.config(state=Tkinter.DISABLED) for x in y] for y in self.field.checkfld]
                loserTL = Toplevel(self.root) #Popup message.
                loserTL.title('You Lose!')
                loserLBL = Label(loserTL,text="Time's Up. You Lose.",font=('Helvetica',14))
                loserBTN = Button(loserTL,text="OK",command=loserTL.destroy)
                loserLBL.pack()
                loserBTN.pack()
                loserTL.bind("<Return>",lambda e:loserTL.destroy())
                loserTL.place(x=self.root.winfo_screenwidth()/2,y=self.root.winfo_screenheight()/2)
            self.__init__(self.root,0,self.uicd,self.field) #Re-initialize whenever we need to restart the timer.
        except RuntimeError: #Thrown when program exits and this thread is still running. We destroy the timer.
            pass