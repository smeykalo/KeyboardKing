# Keyboard King
# Ondřej Smeykal
### INFO: Původně jsem s tímhle úkolem plánoval o dost víc, a stále plánuji,
#         nicméně jaksi se to nestíhá. Proto je zde mnoho zbytečných proměnných,
#         importů a souborů.

### Module Import ###
import time
import tkinter
import random
from tkinter import PhotoImage
from random import randint
import tkinter.messagebox
import math

### Global Constants ###
COLLUMNS = [100, 200, 300, 400, 500, 600]
KEYMAP = {100:"s", 200:"d", 300:"f", 400:"j", 500:"k", 600:"l"}
KEYSPRITEMAP = {}

# Sprite Paths
if True:
    SKEY0 = "Assets\Sprites\SKEY0.png"
    SKEY1 = "Assets\Sprites\SKEY1.png"
    DKEY0 = "Assets\Sprites\DKEY0.png"
    DKEY1 = "Assets\Sprites\DKEY1.png"
    FKEY0 = "Assets\Sprites\FKEY0.png"
    FKEY1 = "Assets\Sprites\FKEY1.png"
    JKEY0 = "Assets\Sprites\JKEY0.png"
    JKEY1 = "Assets\Sprites\JKEY1.png"
    KKEY0 = "Assets\Sprites\KKEY0.png"
    KKEY1 = "Assets\Sprites\KKEY1.png"
    LKEY0 = "Assets\Sprites\LKEY0.png"
    LKEY1 = "Assets\Sprites\LKEY1.png"

    CLASSICBUTTON = "Assets\Sprites\classicTemp.png"
    ENDLESSBUTTON = "Assets\Sprites\EndlessTemp.png"

    BALL0 = "Assets\Sprites\Ball0.png"
    BALL1 = "Assets\Sprites\Ball1.png"
    BALL2 = "Assets\Sprites\Ball2.png"

    AUTHOR = "Assets\Sprites\AuthorPicture.png"

### Class Declaration ###

## Main App ##
class App(tkinter.Tk):
    """Manages the window for the game"""
    def __init__(self):
        super().__init__()
        # Window Setup
        self.title("Keyboard King")
        self.canvas = tkinter.Canvas(self, width=700, height=800, background="black")
        # Note to self: 700x790+260+0
        self.geometry("700x790+410+0")
        self.canvas.focus_set()
        self.canvas.pack()

        # Create the cascading menu
        self.menubar = tkinter.Menu(self)
        gameMenu = tkinter.Menu(self.menubar, tearoff=0)
        gameMenu.add_command(label="About", command=self.aboutWindow)
        gameMenu.add_command(label="How to play", command=self.rules)
        self.menubar.add_cascade(label="Help", menu=gameMenu)
        self.config(menu=self.menubar)
        

        # Create sprite images
        self.CLASSICBUTTON = PhotoImage(file=CLASSICBUTTON)
        self.ENDLESSBUTTON = PhotoImage(file=ENDLESSBUTTON)

        self.loadMainMenu()

    def loadMainMenu(self):
        """Loads the main menu"""
        self.startGameButton = tkinter.Button(self.canvas, text="Start Game", command=self.startClassic, height=99, width=299, borderwidth=0, image=self.CLASSICBUTTON)
        self.startGameButton.place(x=700/2-100, y=790/2-50)
        self.startEndlessButton = tkinter.Button(self.canvas, command=self.startEndless, height=99, width=299, borderwidth=0, image=self.ENDLESSBUTTON)
        self.startEndlessButton.place(x=700/2-100, y=790/2+80)

    def startClassic(self):
        """Starts the classic gamemode (that being what we were supposed to make)"""
        self.startGameButton.destroy()
        self.startEndlessButton.destroy()
        game = ClassicMode(self.canvas)
        game.resetBall()

    def startEndless(self):
        """Starts the endless mode"""
        self.startGameButton.destroy()
        self.startEndlessButton.destroy()
        game = EndlessMode(self.canvas)

    def rules(self):
        """Displays the tutorial window"""
        tkinter.messagebox.showinfo("How to play", "Press the key corresponding to the column where the ball is falling to get points. Try to get the high score!")

    def aboutWindow(self):
        """Opens the about window"""
        self.about = tkinter.Toplevel(self)
        self.about.title("About")
        self.about.geometry("150x125")

        self.about.picture = PhotoImage(file=AUTHOR)

        versionInfo = tkinter.Label(self.about, text="Version: Alpha 1.1")
        devInfo = tkinter.Label(self.about, text="Author: Ondřej Smeykal")
        devPic = tkinter.Label(self.about, image=self.about.picture)

        versionInfo.pack()
        devInfo.pack()
        devPic.pack()

    def run(self):
        self.mainloop()

## Game Objects ##
class Ball:
    def __init__(self, canvas, speed, x=COLLUMNS[randint(0,5)]):
        super().__init__()
        self.canvas = canvas
        self.x1 = x
        self.velocity = speed
        self.sprite = tkinter.PhotoImage(file=BALL0)

    def create(self, y1 = 0):
        """Creates a ball at the top of the screen in one of the 6 collumns"""
        #self.x1 = math.ceil(self.x1/100)*100
        try:
            self.canvas.delete(self.ball)
        except:
            pass
        self.ball = self.canvas.create_image(self.x1,y1,anchor="nw", image=self.sprite)

    def move(self):
        y1 = self.getPosition()[1]
        y1 += self.velocity
        self.canvas.move(self.ball, 0, self.velocity)

    def getPosition(self):
        """Return the coordinates of the balls bounding box"""
        x1,y1,x2,y2 = self.canvas.bbox(self.ball)
        return x1,y1,x2,y2

    def delete(self):
        """Delete the ball"""
        #self.velocity = 0
        self.canvas.delete(self.ball)

    def changeLane(self, col):
        """Changes the collumn where the ball is"""
        self.canvas.moveto(self.ball, col)

    def changeSprite(self, sprite):
        newSprite = tkinter.PhotoImage(file=sprite)
        self.canvas.itemconfig(self.ball, image=newSprite)
        self.sprite = newSprite        
        
## Game Modes ##
class ClassicMode:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.create_rectangle(0, 620, 700, 640, fill="red", outline="red")
        
        ## Variables
        # Setup for key sprites and changing them
        self.sSprite = tkinter.PhotoImage(file=SKEY0)
        self.dSprite = tkinter.PhotoImage(file=DKEY0)
        self.fSprite = tkinter.PhotoImage(file=FKEY0)
        self.jSprite = tkinter.PhotoImage(file=JKEY0)
        self.kSprite = tkinter.PhotoImage(file=KKEY0)
        self.lSprite = tkinter.PhotoImage(file=LKEY0)

        self.sDown = False
        self.dDown = False
        self.fDown = False
        self.jDown = False
        self.kDown = False
        self.lDown = False

        # Other variables
        self.gameOver = False
        self.updating = False
        self.lastCol = None
        self.score = 0
        self.lives = 10
        self.switchTime = 3000
        self.canvas.bind("<KeyPress>", self.keyPress)
        self.canvas.bind("<KeyRelease>", self.keyRelease)
        self.canScore = True
        self.speed = 2
        self.combo = 0
        
        self.update()
        self.scoreBoard = self.canvas.create_text(80, 760, text=f"Points: {self.score}, Combo: {self.combo}, Lives: {self.lives}", fill="red")
        
    def resetBall(self):
        """Create a new ball at the top of the screen"""
        # Ensure a new column
        try:
            newCol = COLLUMNS[randint(0,5)]
            while self.lastCol == newCol:
                newCol = COLLUMNS[randint(0,5)]
        except:
            pass
        self.ball = Ball(self.canvas, self.speed, newCol)
        self.ball.create()
        self.switchTimer = self.canvas.after(self.switchTime, self.laneSwitch)

    def update(self):
        """Updates the ball every frame and checks for key presses and loss"""
        try:
            ## Update movement
            self.ball.move()

            # Check for life loss
            if self.ball.getPosition()[1] > 620:
                self.lastCol = self.ball.getPosition()[0]
                self.die()

            # Update the Scoreboard
            self.canvas.itemconfig(self.scoreBoard, text=f"Points: {self.score}, Combo: {self.combo}, Lives: {self.lives}")

        except:
            pass

    
        # Update the key sprites
        if True:
            if self.sDown == True:
                self.sSprite = tkinter.PhotoImage(file=SKEY1)
            else:
                self.sSprite = tkinter.PhotoImage(file=SKEY0)
            if self.dDown == True:
                self.dSprite = tkinter.PhotoImage(file=DKEY1)
            else:
                self.dSprite = tkinter.PhotoImage(file=DKEY0)
            if self.fDown == True:
                self.fSprite = tkinter.PhotoImage(file=FKEY1)
            else:
                self.fSprite = tkinter.PhotoImage(file=FKEY0)
            if self.jDown == True:
                self.jSprite = tkinter.PhotoImage(file=JKEY1)
            else:
                self.jSprite = tkinter.PhotoImage(file=JKEY0)
            if self.kDown == True:
                self.kSprite = tkinter.PhotoImage(file=KKEY1)
            else:
                self.kSprite = tkinter.PhotoImage(file=KKEY0)
            if self.lDown == True:
                self.lSprite = tkinter.PhotoImage(file=LKEY1)
            else:
                self.lSprite = tkinter.PhotoImage(file=LKEY0)

        self.S = self.canvas.create_image(75, 650, anchor="nw", image=self.sSprite)
        self.D = self.canvas.create_image(175, 650, anchor="nw", image=self.dSprite)
        self.F = self.canvas.create_image(275, 650, anchor="nw", image=self.fSprite)
        self.J = self.canvas.create_image(375, 650, anchor="nw", image=self.jSprite)
        self.K = self.canvas.create_image(475, 650, anchor="nw", image=self.kSprite)
        self.L = self.canvas.create_image(575, 650, anchor="nw", image=self.lSprite)

        self.updateTimer = self.canvas.after(10, self.update)

    def laneSwitch(self):
        """Get a point and switch lane and all that after hitting the correct key"""
        self.canvas.after_cancel(self.switchTimer)
        lastX = self.ball.getPosition()[0]
        y = self.ball.getPosition()[1]
        newX = lastX
        # Switch to a unique column
        while newX == lastX:
            newX = COLLUMNS[randint(0,5)]
        self.ball.changeLane(newX)
        self.ball.changeSprite(BALL0)
        # Update scoring and reset the timer
        self.canScore = True

        self.switchTimer = self.canvas.after(self.switchTime, self.laneSwitch)

    def keyPress(self, event):
        """Check if the correct key was pressed and proceed accordingly"""
        if self.canScore == True:
            correctKey = KEYMAP.get(round(self.ball.getPosition()[0]/100)*100)
            if event.keysym == correctKey:
                self.combo += 1
                self.score += 10*self.combo
                self.canScore = False
                self.canvas.after_cancel(self.switchTimer)
                self.ball.changeSprite(BALL1)
                self.canvas.after(300, self.laneSwitch)
            else:
                self.canvas.itemconfig(self.ball, fill= "black")
                self.ball.changeSprite(BALL2)
                self.canScore = False
                self.canvas.after_cancel(self.switchTimer)
                self.canvas.after(1000, self.laneSwitch)
                self.combo = 0
        
        # Change key states
        if True:
            if event.keysym == "s":
                self.sDown = True
            else:
                self.sDown = False

            if event.keysym == "d":
                self.dDown = True
            else:
                self.dDown = False

            if event.keysym == "f":
                self.fDown = True
            else:
                self.fDown = False

            if event.keysym == "j":
                self.jDown = True
            else:
                self.jDown = False

            if event.keysym == "k":
                self.kDown = True
            else:
                self.kDown = False

            if event.keysym == "l":
                self.lDown = True
            else:
                self.lDown = False

    def keyRelease(self, event):
            if event.keysym == "s":
                self.sDown = False
            
            if event.keysym == "d":
                self.dDown = False
            
            if event.keysym == "f":
                self.fDown = False
            
            if event.keysym == "j":
                self.jDown = False
            
            if event.keysym == "k":
                self.kDown = False
            
            if event.keysym == "l":
                self.lDown = False
            
    def die(self):
        """Lose one life (after a ball goes over the thing)"""
        # Check for game loss
        self.lives -= 1
        self.canScore = True
        self.canvas.after_cancel(self.switchTimer)
        if self.lives == 0:
            self.gameOver = True
            self.gameEnd()

        self.ball.delete()
        if self.gameOver != True:
            # Increase the difficulty
            self.switchTime -= 100
            self.speed += 0.5
            self.canvas.after_cancel(self.switchTimer)
            
            self.resetBall()

    def gameEnd(self):
        """End the game after losing all lives"""
        self.canvas.after_cancel(self.updateTimer)

class EndlessMode(ClassicMode):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.resetBall()
        self.lives = 3
        self.combo = 0
        self.score = 0
        self.rawPoints = 0

    def keyPress(self, event):
        if self.canScore == True:
            correctKey = KEYMAP.get(round(self.ball.getPosition()[0]/100)*100)
            self.lastCol = self.ball.getPosition()[0]
            if event.keysym == correctKey:
                self.rawPoints += 1
                self.combo += 1
                self.ball.changeSprite(BALL1)
                self.resetBall()
                # Add the score
                if self.combo < 10:
                    self.score += 10
                else:
                    self.score += 10*(self.combo-9)
                # Speed up if conditions are met
                if self.rawPoints % 10 == 0:
                    self.speed += 1

            if event.keysym != correctKey:
                self.canScore = False
                self.ball.changeSprite(BALL2)
                self.ball.velocity = 50
                self.combo = 0
                # Slow down a bit
                if self.speed > 4:
                    self.speed -= 2
                else:
                    self.speed = 2
    
    def resetBall(self):
        super().resetBall()
        self.canvas.after_cancel(self.switchTimer)

    def die(self):
        """Lose one life (after a ball goes over the thing)"""
        # Check for game loss
        self.lives -= 1
        self.canScore = True
        if self.lives == 0:
            self.gameOver = True
            self.gameEnd()

        self.ball.delete()
        if self.gameOver != True:
            self.resetBall()


### Main Program ###
if __name__ == "__main__":
    app = App()
    app.run()