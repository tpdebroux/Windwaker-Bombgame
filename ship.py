#24 bombs
#8x8 grid
#3 squids, 4x1, 3x1, 2x1
from random import randint
from tkinter import *
import tkinter.messagebox

def getBigPosition():
    vertical = randint(0, 1)
    global big_position
    if(vertical):
        x = randint(0, 7)
        y = randint(1, 6)
        if(y == 1):
            big_position = ((x, y-1),(x, y),(x,y+1),(x,y+2))
        else:
            big_position = ((x, y-2), (x,y-1),(x,y),(x,y+1))

    else:
        x = randint(1, 6)
        y = randint(0, 7)
        if(x == 1):
            big_position = ((x-1,y),(x,y),(x+1,y),(x+2,y))
        else:
            big_position = ((x-2,y),(x-1,y),(x,y),(x+1,y))

def getMediumPosition():
    while(True):
        vertical = randint(0, 1)
        global big_position
        global medium_position
        if(vertical):
            x = randint(0, 7)
            y = randint(1, 6)
            while((x,y) in big_position):
                x = randint(0, 7)
                y = randint(1, 6)
            medium_position = ((x, y-1),(x, y),(x,y+1))
        else:
            x = randint(1, 6)
            y = randint(0, 7)
            while((x,y) in big_position):
                x = randint(1, 6)
                y = randint(0, 7)
            medium_position = ((x-1,y),(x,y),(x+1,y))
        if(not((medium_position[0] in big_position) or
        (medium_position[1] in big_position) or
        (medium_position[2] in big_position))):
            break

def getSmallPosition():
    while(True):
        vertical = randint(0, 1)
        global big_position
        global medium_position
        global small_position
        if(vertical):
            x = randint(0, 7)
            y = randint(1, 6)
            while(((x, y) in big_position) or ((x, y) in medium_position)):
                x = randint(0, 7)
                y = randint(1, 6)
            small_position = ((x, y), (x, y + 1))
        else:
            x = randint(1, 6)
            y = randint(0, 7)
            while(((x, y) in big_position) or ((x, y) in medium_position)):
                x = randint(1, 6)
                y = randint(0, 7)
            small_position = ((x, y), (x + 1, y))
        if(not((small_position[0] in big_position) or
        (small_position[1] in big_position) or
        (small_position[0] in medium_position) or
        (small_position[1] in medium_position))):
            break

def convertPositions():
    global smallLocations
    global mediumLocations
    global bigLocations
    global small_position
    global medium_position
    global big_position
    smallLocations.append(small_position[0][0] * 8 + small_position[0][1])
    smallLocations.append(small_position[1][0] * 8 + small_position[1][1])
    mediumLocations.append(medium_position[0][0] * 8 + medium_position[0][1])
    mediumLocations.append(medium_position[1][0] * 8 + medium_position[1][1])
    mediumLocations.append(medium_position[2][0] * 8 + medium_position[2][1])
    bigLocations.append(big_position[0][0] * 8 + big_position[0][1])
    bigLocations.append(big_position[1][0] * 8 + big_position[1][1])
    bigLocations.append(big_position[2][0] * 8 + big_position[2][1])
    bigLocations.append(big_position[3][0] * 8 + big_position[3][1])
    print(bigLocations)
    print(mediumLocations)
    print(smallLocations)

big_position = 0
medium_position = 0
small_position = 0
getBigPosition()
#print(big_position)
getMediumPosition()
#print(medium_position)
getSmallPosition()
#print(small_position)
smallLocations = []
mediumLocations = []
bigLocations = []
convertPositions()

root = Tk()

buttons = []
bombcount = 23
gridFrame = Frame(root)
gridFrame.pack(side = RIGHT)
waterLogo = PhotoImage(file='waterIcon.png')
for r in range(8):
    for c in range(8):
        button = Button(gridFrame, image=waterLogo,
            width=50, height=50, bg='#7b7c7b',command=lambda index=(r*8 + c):targetSelect(index))
        button.grid(row=r,column=c)
        buttons.append(button)

missLogo = PhotoImage(file = 'miss.png')
hitLogo = PhotoImage(file = 'hit.png')
def checkWinState():
    global bigLocations
    global mediumLocations
    global smallLocations
    if(bigLocations[0] == bigLocations[1] == bigLocations[2] == bigLocations[3]
    == mediumLocations[0] == mediumLocations[1] == mediumLocations[2]
    == smallLocations[0] == smallLocations[1]
    == -1):
        gameOver(1)
def gameOver(result):
    if(result):
        print('Win!')
        answer = tkinter.messagebox.askyesno('You won!','Would you like to play again?')
        if(answer):
            print('yes')
            #play again
        else:
            #close program
            print('close program')
    else:
        print('lost.') 
        answer = tkinter.messagebox.askyesno('You lost.','Would you like to try again?')
        

def targetSelect(index):
    global bombcount
    global bombLabel
    global bigLocations
    global mediumLocations
    global smallLocations
    if((index in bigLocations) or (index in mediumLocations) or (index in smallLocations)):
        buttons[index].config(image=hitLogo)
        if(index in bigLocations):
            for i in range(4):
                if (bigLocations[i] == index):
                    bigLocations[i] = -1
                    break
        elif(index in mediumLocations):
            for i in range(3):
                if (mediumLocations[i] == index):
                    mediumLocations[i] = -1
                    break
        elif(index in smallLocations):
            for i in range(2):
                if (smallLocations[i] == index):
                    smallLocations[i] = -1
                    break
        #checkWinState()
    else:
        buttons[index].config(image=missLogo)
    buttons[index].config(state="disabled")
    bombs[bombcount].config(state="disabled")
    bombcount = bombcount - 1
    checkWinState()
    if(bombcount == -1):
        gameOver(0)
    bombLabel.config(text = bombcount + 1)

bombLogo = PhotoImage(file='bombIconLarger.png')
bombs = []
bombFrame = Frame(root)
bombFrame.pack(side = LEFT)
bombLabel = Label(bombFrame, text=bombcount+1, font=("Verdana", 16))
bombLabel.pack()

leftFrame = Frame(bombFrame)
leftFrame.pack()

for r in range(8):
    for c in range(3):
        bomb = Label(leftFrame,image=bombLogo,width=32,height=32)
        bomb.grid(row=r,column=c)
        bombs.append(bomb)

root.mainloop()
