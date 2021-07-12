from guizero import*
import tkinter as tk
from tkinter import ttk
import string
import random

app = App(layout="grid",title="Skrabble",width=800,height=705)

alphabet = list(string.ascii_uppercase)

def Play():
    global DrawButton,z,no_of_players,NextButton    
    message1.visible=False
    combo.visible=False
    playbutton.visible=False
    no_of_players = int(combo.value)
    AddInfo()
    AddBag()
    text = "Click to take a tile from the bag!\nTiles remaining: "+str(len(alltiles))
    DrawButton = PushButton(app,grid=[0,6,4,1],text=text,command=TakeTile)
    DrawButton.text_size=15
    DrawButton.bg="powder blue"
    ShowHand()
    NextButton = PushButton(app,grid=[0,13,4,1],text="Finish Turn",enabled=False,command=NextTurn)
    NextButton.text_size=15
    NextButton.bg="red"
    NextTurn()

def AddDialogue():
    global message1,combo,playbutton
    ctrlframe = Box(app,layout="grid",grid=[0,0,4,17],width=583,height=705)
    message1 = Text(app, grid=[0,4,4,1],text="How many players?",size=30,width = 25)
    combo = Combo(app,options=[2,3,4],width=10,grid=[0,8,4,1])
    combo.text_size=20
    combo.bg="white"
    playbutton = PushButton(app,text="PLAY",grid=[0,12,4,1],width=7,command=Play)
    playbutton.text_size=50
    playbutton.bg="green2"

AddDialogue()

x3word = [18,25,32,137,151,256,263,270]
x2word = [36,48,54,64,72,80,90,96,144,192,198,208,216,224,234,240,252]
x3letter = [40,44,104,108,112,116,172,176,180,184,244,248]
x2letter = [21,29,58,60,69,76,83,122,126,128,132,140,148,156,
           160,162,166,205,212,219,228,230,259,267]

def BoardDesign(a,last):


    if a in x3word:
        squares[last].tk.configure(bg="red",font="Helvetica 9 bold")
        squares[last].text="TRIPLE\nWORD\nSCORE"
    
    elif a in x2word:
        squares[last].tk.configure(bg="LightPink2",font="Helvetica 9 bold")
        squares[last].text="DOUBLE\nWORD\nSCORE"
    
    elif a in x3letter:
        squares[last].tk.configure(bg="dodger blue",font="Helvetica 9 bold")
        squares[last].text="TRIPLE\nLETTER\nSCORE"

    elif a in x2letter:
        squares[last].tk.configure(bg="light blue",font="Helvetica 9 bold")
        squares[last].text="DOUBLE\nLETTER\nSCORE"
    else:
        squares[last].bg="light sea green"
        squares[last].text=""

tileindex = ""

def SelectSquare(a):
    global tileindex,TilesUsed

    if squares[a].bg == "light goldenrod":
        pass
    if squares[a].bg == "goldenrod1":
        UsedIndex = SquaresUsed.index(a)
        hand[TilesUsed[UsedIndex]].text=squares[a].text
        hand[TilesUsed[UsedIndex]].bg="light goldenrod"
        hand[TilesUsed[UsedIndex]].enabled=True
        hand[TilesUsed[UsedIndex]].text_color="black"
        TilesUsed.pop(UsedIndex)
        SquaresUsed.remove(a)        
        BoardDesign(a,a)
    else:
        if tileindex != "":
            squares[a].tk.configure(bg="goldenrod1",font="Helvetica 9 bold")
            squares[a].text=hand[tileindex].text
            hand[tileindex].bg="SystemButtonFace"
            hand[tileindex].text=""
            hand[tileindex].enabled=False
            TilesUsed.append(tileindex)
            SquaresUsed.append(a)
        tileindex = ""

def SetBoard():
    global a,squares,boardframe
    global squares
    boardframe = Box(app,layout="grid",grid=[4,0,1,17])
    boardframe.bg="turquoise4"
    squares = list()
    y = 0
    x = 0
    for a in range(289):
        if a % 17 == 0 and a!=0:
            y += 1
            x -= 17        
        if x in [0,16]:
            row = a//17
            squares.append(Text(boardframe,grid=[x,y],
                                text=alphabet[row-1],color="white",
                                width=2,height=1))
        elif y in [0,16]:
            squares.append(Text(boardframe,grid=[x,y],
                                text=x,color="white",
                                width=3))
        else:
            squares.append(PushButton(boardframe,grid=[x,y],width=3,height=1,
                                      command=lambda a=a: SelectSquare(a)))            
            squares[-1].tk.configure(borderwidth=2)
            last=-1
            BoardDesign(a,last)
        if squares[-1].value in ["Z","P"]:
            squares[-1].value=""
        x += 1

SetBoard()

def AddInfo():
    global playerinfo,scores
    playerinfo = list()
    scores = []
    for z in range(no_of_players):
        scores.append(0)
        text = "Player "+str(z+1)+"\n\nScore: "+str(scores[z])
        playerinfo.append(PushButton(app,text=str(text),grid=[z,0],width=8))
        playerinfo[-1].text_size=15
        playerinfo[-1].bg="white"
        if no_of_players==2:
            playerinfo[-1].grid=[2*z,0,2,1]
            playerinfo[-1].width=17
        if no_of_players==3:
            playerinfo[-1].width=10
            if z == 1:
                playerinfo[-1].grid=[z,0,2,1]
            if z == 2:
                playerinfo[-1].grid=[3,0]
        

turn=0
movecount=0

TilesUsed = []
SquaresUsed = []

alignment = "null"

def AddScore():
    global alignment
    if SquaresUsed != []:
        if len(SquaresUsed) !=1:
            diff = abs(SquaresUsed[0]-SquaresUsed[1])
            if diff < 17:
                alignment = "horizontal"
            else:
                alignment = "vertical"
            print(alignment)
        else:
            alignment = "vertical"
            
        words = []    
        for i in SquaresUsed:
            word = [] 
            if alignment == "vertical":
                #print(SquaresUsed)
                checkleft = 1
                Scanleft = True
                
                while Scanleft == True:
                    if squares[i-checkleft].bg == "light goldenrod":
                        #print(squares[i-checkleft].text)
                        word.append(squares[i-checkleft].text)
                    else:
                        Scanleft = False                
                    checkleft+=1

                word.append(squares[i].text)
                    
                Scanright = True
                checkright = 1
                while Scanright == True:
                    if squares[i+checkright].bg == "light goldenrod":
                    #if len(squares[i+checkright].text) == 1:
                        #print(squares[i+checkright].text)
                        word.append(squares[i+checkright].text)
                    else:
                        Scanright = False                
                    checkright+=1

                #print(word)
                if len(word) > 1:
                    words.append(word)
        print(words)
            

            
    scoremultiply = 1
    score = 0
    for i in SquaresUsed:
        #print(i)
        letter = squares[i].text
        #print(letter)
        letterindex = alphabet.index(letter)
        value = points[letterindex]
        #print(value)
        if i in x2letter:
            value *= 2
        elif i in x3letter:
            value *= 3
        #print(value)
        score += value
    #print(score)
    #print(scores)
    scores[turn] += score
    #print(scores)
    text = "Player "+str(turn+1)+"\n\nScore: "+str(scores[turn])
    playerinfo[turn].text=str(text)
    
    
        
        

def NextTurn():
    global turn,TilesUsed,SquaresUsed,movecount
    #print(TilesUsed)
    #print(SquaresUsed)
    
    AddScore()
        
    TilesUsed.sort(reverse=True)
    for each in TilesUsed:
        hands[turn].pop(each)
    TilesUsed = []
    SquaresUsed = []
    
    if movecount != 0:
        turn+=1
        if turn == no_of_players:
            turn -= no_of_players
    movecount+=1
    SwitchHand()
    for square in squares:
        if square.bg=="goldenrod1":
            square.bg="light goldenrod"
            

def SwitchHand():
    global keeptiles
    for i in playerinfo:
        i.enabled=False
        i.bg="white"
        i.text_color="black"        
    playerinfo[turn].enabled=True
    playerinfo[turn].bg="black"
    playerinfo[turn].text_color="white"          
    keeptiles = len(hands[turn])
    for i in range(7):
        if i > keeptiles-1:
            hand[i].bg="SystemButtonFace"
            hand[i].text=""
            hand[i].enabled=False
        else:
            hand[i].text=hands[turn][i]
            hand[i].bg="light goldenrod"
            hand[i].enabled=True
        hand[i].text_color="black"
    if keeptiles < 7:
        DrawButton.enabled=True
        NextButton.enabled=False

        
def SelectTile(i):
    global tileindex, HandFull
    if len(hands[turn])==7:      
        for j in hand:
            if j.enabled==True:
                j.bg="light goldenrod"
                j.text_color="black"
        hand[i].bg="black"
        hand[i].text_color="white"
        tileindex = i

def ShowHand():
    global hand
    hand = list()
    for i in range(7):
        hand.append(PushButton(app,grid=[i,11],text="",width=3,
                               command=lambda i=i: SelectTile(i)))        
        hand[-1].text_size=30
        hand[-1].tk.configure(borderwidth=5) 
        if i > 3:
            hand[-1].grid = [i-4,12,2,1]

def AddBag():
    global alltiles,hands,points
    alphabet.append("")
    points = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1,
              1, 1, 1, 4, 4, 8, 4, 10, 0]
    letterfreq = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1,
                  6, 4, 6, 4, 2, 2, 1, 2, 1, 2]
    alltiles = []
    for number in range(27):
        for freq in range(letterfreq[number]):
            alltiles.append(alphabet[number])
    random.shuffle(alltiles)
    hands = list()
    for x in range(no_of_players):
        hands.append([])


def TakeTile():
    Visible = 0
    for i in range(7):
        if hand[i].enabled==True:
            Visible += 1
    hand[Visible].bg="light goldenrod"
    hand[Visible].enabled=True
    if Visible == 6:
        DrawButton.enabled=False
        NextButton.enabled=True
    hand[Visible].text=alltiles[-1]
    hands[turn].append(alltiles[-1])
    alltiles.pop()
    DrawButton.text="Click to take a tile from the bag!\nTiles remaining: "+str(len(alltiles))
           

def AddDialogue():
    global message1,combo,playbutton
    ctrlframe = Box(app,layout="grid",grid=[0,0,4,17],width=583,height=705)
    message1 = Text(app, grid=[0,4,4,1],text="How many players?",size=30,width = 25)
    combo = Combo(app,options=[2,3,4],width=10,grid=[0,8,4,1])
    combo.text_size=20
    combo.bg="white"
    playbutton = PushButton(app,text="PLAY",grid=[0,12,4,1],width=7,command=Play)
    playbutton.text_size=50
    playbutton.bg="green2"

AddDialogue()

app.display()
