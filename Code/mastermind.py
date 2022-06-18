#Python Assignment 2.1 - Mastermind Game

"""
Created on Fri Dec 03 11:20:46 2021

@author: Lindelani
"""

from tkinter import *
import tkinter as tk
import random,os
from random import choices
import itertools as it
from tkinter import messagebox


#Building Linde's Mastermind Game for Girls

#________________________________________________________________________________________________________________________________________________________

#PART 1: Building the MENU WINDOW

class GameMenu:
    def __init__(self,root):
        self.master=root
        self.master.geometry('400x550') #The size of the menu
        self.master.config(bg='#ff99b7') #The background colour of the menu
        self.mmSavedGames=self.read('MMSavedGames.txt',5) #Option to Load previously Saved Games
        self.GameMainMenu()

#Function for the main menu
    def GameMainMenu(self):
        self.clear()   #Clearing the previous widgets
        
        #Buttons for the main menu
        self.button1=tk.Button(self.master,text='Play Mastermind', bg='#cc446c', fg='#ffffff', font='Helvetica 11 bold')                                 
        self.button2=tk.Button(self.master,text='Load Saved Games', bg='#cc446c', fg='#ffffff', font='Helvetica 11 italic')                                 
        self.button3=tk.Button(self.master,text='Exit Mastermind', bg='#cc446c', fg='#ffffff', font='Helvetica 11 italic')
        
        self.button1.pack(pady=40)
        self.button2.pack(pady=40)
        self.button3.pack(pady=40)
        
        #When the buttons are touched by the cursor their function will perform
        self.button1.bind('<Button-1>',lambda i:self.specs())
        self.button2.bind('<Button-1>',self.Reloading)
        self.button3.bind('<Button-1>',lambda i:exit())                                      

#Function for clearing the menu
    def clear(self):
        listtreturn = self.master.slaves()
        for l in listtreturn:
            l.destroy()

#Function for the games requirements
    def specs(self):
        self.clear()

        #Organising widgets with frames (Week 9 lecture)
        self.frame1=tk.Frame(self.master,bg='#ff99b7')
        self.frame1.pack()
        self.frame2=tk.Frame(self.master,bg='#ff99b7')
        self.frame2.pack()
        self.frame3=tk.Frame(self.master,bg='#ff99b7')
        self.frame3.pack()
              
#Labelling widget frames (for the columns)
        self.coLab=tk.Label(self.frame1,text='Select Game Columns ',bg='#ff99b7', font='Helvetica 11 bold italic') 
        self.coLab.grid(row=0,column=0,pady=25) 
        self.cols=['4','6','8']  
        self.col = StringVar()
        
#Choosing the columns  
        self.col.set(self.cols[0]) #Making the variable's initial value the same as the columns first value
        self.dropCol = tk.OptionMenu( self.frame1 , self.col , *self.cols) #Showing the other column options for the user to select
        self.dropCol.config(width=20)    
        self.dropCol.grid(row=0,column=1,pady=25) #Adding this to the initial grid

#Labelling widget frames (for the rows)
        self.roLab=tk.Label(self.frame2,text='Select Game Rows ',bg='#ff99b7', font='Helvetica 11 bold italic') 
        self.roLab.grid(row=0,column=0,pady=25)
        self.ros=[str(i) for i in range(10,16)]
        self.rowS = StringVar()

#Choosing the rows
        self.rowS.set(self.ros[-1])
        self.dropRow = tk.OptionMenu( self.frame2 , self.rowS , *self.ros) #Showing the other row options for the user to select
        self.dropRow.config(width=20)
        self.dropRow.grid(row=0,column=1,pady=20)

#Labelling widget frames (for selecting the player game mode options)
        self.typLab=tk.Label(self.frame3,text='Select Game Play ',bg='#ff99b7', font='Helvetica 11 bold italic') 
        self.typLab.grid(row=0,column=0,pady=25)
        self.typ=['Gamer Girl VS The Computer','The Computer VS Itself'] #The game's full player titles 
        self.typShort=['GvsT','TvsI'] #Shortened versions of the titles 
        self.dictionary=dict(zip(self.typ,self.typShort)) #Dictionary to label the full game player titles as keys and the short titles versions as values
        self.gType = StringVar()    
        
#Choosing the player game mode
        self.gType.set(self.typ[0])
        self.gam = tk.OptionMenu( self.frame3 , self.gType , *self.typ ) #Showing the user the game's player mode options they can select
        self.gam.config(width=35)
        self.gam.grid(row=0,column=1,pady=35) #Adding this to the initial grid

#Creating the 'start the game' button
        self.runBtn=tk.Button(self.master,text='Start The Game',width=20, bg='#cc446c', font='Helvetica 9 bold') 
        self.runBtn.pack(pady=15)
        self.runBtn.bind('<Button-1>',lambda x:self.start(int(self.col.get()),int(self.rowS.get()),self.dictionary[self.gType.get()])) #User presses this button to start the game

#________________________________________________________________________________________________________________________________________________________

#PART 2: Building the GAME FUNCTIONS

#Function starting the mastermind game
    def start(self,holes,guesses,typ,load=None):
        self.clear() 
        self.x=Mastermind(self.master,self,self.mmSavedGames,holes=holes,guesses=guesses,typ=typ,load=load) #This is the game frame for mastermind
        self.x.pack() 
        self.x.GameGUI() 

#Function for reloading the data from the user's previously saved games
    def Reloading(self,event):
        self.clear()
        self.names=['Save '+str(i) for i in range(5)] #The titles of all the saved files will be displayed in this list
        self.SaveLabs=[tk.Button(self.master,text=name,width=20,bg='#b23b5f',fg='#ffffff',font='Helvetica 10 bold italic') for name in self.names] 
        for widg in self.SaveLabs: #Showing the labels for the files
            widg.pack(pady=25) 
#Seperately binding each label individually to a button which will enable them to respond to whichever button the user's selects
        self.SaveLabs[0].bind('<Button-1>',lambda x:self.Continue(0))
        self.SaveLabs[1].bind('<Button-1>',lambda x:self.Continue(1))
        self.SaveLabs[2].bind('<Button-1>',lambda x:self.Continue(2))
        self.SaveLabs[3].bind('<Button-1>',lambda x:self.Continue(3))
        self.SaveLabs[4].bind('<Button-1>',lambda x:self.Continue(4))


#Function for continuing game from the selected saved file
    def Continue(self,ind):
        if self.mmSavedGames[ind][0]=='1': 
            self.clear()
            self.data=self.read("Saves\\Save "+str(ind)+'.txt',4)   #To read the data of the selected file
            self.LoadedData=self.splitting() #To load the saved game data into a visual form for the user
            self.start(*self.LoadedData[0],'GvsT',load=self.LoadedData) 
        else:   #Should the user have no previously saved file then the program will display this message
            messagebox.showinfo('There is no saved file here!')
            
#Function for reading the saved file data      
    def read(self,directory,x):
        maz=open(directory,'r') #To open the saved file from its directory path
        a=[]    
        for i in range(x): #For loop is applied to iterate through the list
            c=maz.readline()    
            c=c.rstrip('\n')   
            a.append(c) 
        maz.close()                                           
        return a     
    
#Function for changing the data from the selected saved file into a useable form for the user(player)
    def splitting(self):
        a=[[] for i in range(4)]  #Each save file has four rows which results in a list of four lists
        RCtup=self.data[0].split(',')  #Data is split using a comma delimiter converting data to a list, creating a list with each value as an element
        a[0]=[int(RCtup[0]),int(RCtup[1])]  #The first element is converted into the number of rows and columns
        a[1]=int(self.data[1])  
        hlp=self.data[2].split(',')
        outLis=[] 
        for i in range(0,len(hlp),a[0][0]):
            inLis=[]
            for j in range(a[0][0]):
                inLis.append(hlp[j+i])
            outLis.append(inLis)
        a[2]=outLis
        hlp=self.data[3].split(',')
        a[3]=hlp    
        return a

#________________________________________________________________________________________________________________________________________________________

#PART 3: Building the MASTERMIND GAME 1/2

#Class for mastermind game
class Mastermind(tk.Frame):

    def __init__(self, master,parent, mmSavedGames, colours=8, holes=4, guesses=10,typ='PvC',load=None, bg="#ffd8e3", fg="black", **kwargs):
        self.parent=parent #Root window
        self.numberOfColours = colours  
        self.numberOfHoles = holes  
        self.numberOfGuesses = guesses  
        self.gameType=typ   
        self.load=load  #List of the loaded data
        self.MMSavedGames=mmSavedGames #This will not be used if previous game files are empty
        self.BackToGamerGirl=True #Attribute to allow the game to return back to the player guess once the computer has made its move
        self.time=2500  #The computers set time to play is 2.5 seconds (2500ms)
        if self.load!=None: 
            self.BackToGamerGirl=False
            self.time=15
        self.steps=0    
        self.step=random.choice([i for i in range(self.numberOfGuesses)])   
        self.bg = bg #Background colour
        self.fg = fg    #Foreground colour
        self.clr2save=[] #List of colours used for different labels of the rows
        self.master = master
        self.colours = ["#9400D3", "#FF0000", "#FFFF00", "#F2ACB9", "#D3D3D3",
                        "#FFA500", "#D9027D", "#E5B6F7", "#FFFFFF", "#000000"][:self.numberOfColours] #Violet,Red,Yellow,Baby Pink,Light Grey,Orange,Fushia,Lilac,White,Black
        self.cLis={"#9400D3":'Violet', "#FF0000":'Red', "#FFFF00":'Yellow', "#F2ACB9":'Baby Pink', 
                "#D3D3D3":'Light Grey',"#FFA500":'Orange', "#D9027D":'Fushia', "#E5B6F7":'Lilac'}
        '''for i in self.colours:
            tk.Label(root,text=i).pack()'''
        self.combination=self.LengthCombinations(self.colours, self.numberOfHoles)
        self.ResetColours()
        self.answer = random.sample(self.colours, k=self.numberOfHoles) #Random colour combination picked by the computer
        if self.load != None:   
            self.answer=self.load[3]    
        super().__init__(self.master, bg=self.bg, **kwargs) 
        for i in self.answer:   
            print(self.cLis[i]+' ',end='')
        self.clrSelect=self.colours[0]  

#Function for building the game's GUI
    def GameGUI(self):

        self.allGuesses = [tk.Frame(self, bg=self.bg) for _ in range(self.numberOfGuesses)]
        self.allMarks = [tk.Frame(self, bg=self.bg) for _ in range(self.numberOfGuesses)]
        self.answerFrame = tk.Frame(self, bg=self.bg)
        self.answerCover = tk.Frame(self, bg=self.fg, relief=tk.RAISED) 

#Labels for the guesses
        self.allGuessPins = [[tk.Label(self.allGuesses[i], width=8, height=1, bg="#a3264c", relief=tk.SUNKEN)
                             for _ in range(self.numberOfHoles)]
                             for i in range(self.numberOfGuesses)]
#Labels for the correct guesses
        self.allMarkPins = [[tk.Label(self.allMarks[i], width=1, height=1, bg="#FFF1FA", relief=tk.SUNKEN)
                             for _ in range(self.numberOfHoles)]
                             for i in range(self.numberOfGuesses)]
#Label for answer box 
        self.answerPins = [tk.Label(self.answerFrame, width=2, height=1, bg=colour, relief=tk.RAISED) for colour in self.answer]
        self.guessBtn = tk.Button(self, text="Guess", command=self.NextGuess, bg=self.bg, fg=self.fg, font='Helvetica 8 bold')
        self.activeGuess = 0    

#Beginning the game with an empty grid spaces then filling in the labels with each guess
        for rowIndex in range(self.numberOfGuesses):
            for holeIndex in range(self.numberOfHoles):
                self.allGuessPins[rowIndex][holeIndex].grid(row=0, column=holeIndex, padx=1, pady=4)
                self.allMarkPins[rowIndex][holeIndex].grid(row=0, column=holeIndex, padx=1, pady=4)
            tk.Label(self, text=str(rowIndex+1), bg=self.bg, fg=self.fg).grid(row=self.numberOfGuesses-rowIndex, column=0) 
            self.allGuesses[rowIndex].grid(row=rowIndex+1, column=1)
            self.allMarks[rowIndex].grid(row=rowIndex+1, column=3)
#For loop to fill those labels into the grid
        for i, a in enumerate(self.answerPins):
            a.grid(row=0, column=i, padx=1)
#Labels to free up some room
        tk.Label(self, text="   ", bg=self.bg).grid(row=0, column=2)
        tk.Label(self, text="   ", bg=self.bg).grid(row=0, column=4)
        
#The answer will covered with a black bar and positioned at the top of the game's panel
        for a in [tk.Label(self.answerCover, width=2, height=1, bg=self.fg) for _ in range(self.numberOfHoles)]:
            a.pack(side=tk.LEFT, padx=1)
#Black bar covering the colour combination
        self.answerCover.grid(row=0, column=1, pady=15)
        self.guessBtn.grid(column=1, row=999, pady=10)
        if self.gameType=='GvsT': #For game of Gamer Girl vs The Computer
            self.NextGuess(start=True)
        elif self.gameType=='TvsI': #For game of The Computer vs Itself
            self.NextGuess(start=True)

        self.colourFrame=tk.Frame(self) 
        self.colourFrame.grid(row=1000, column=0,columnspan=2,sticky='WE')
        selectFram=tk.Frame(self) #The colour (purple) which is set as a default will be shown here
        selectFram.grid(row=1001, column=0,columnspan=2,pady=4,sticky='WE')
        self.selctLab=tk.Label(selectFram,text='Select a Colour',anchor='w',font='Helvetica 8 bold')
        self.selectClrLab=tk.Label(selectFram,width=8,height=1,relief=tk.SUNKEN,bg=self.clrSelect) 

#Showing the available colours for the user to play with
        self.labLis=[]
        colN=0
        col=0
        for colr in self.colours: 
            ro=1
            if colN%2==0:   
                ro=0
            lab=tk.Label(self.colourFrame, width=4, height=1, bg=colr, relief=tk.RAISED, anchor="w")               
            lab.grid(row=ro,column=col)
            self.labLis.append(lab)  
            colN+=1
            col+=1

#A heart symbol will replace the cursor when the user hoovers over the colour pegs at the bottom of the game's panel
        for i, pin in enumerate(self.labLis):
            pin.bind("<1>", lambda event, i=i: self.SelectedColourChange(event, i))
            pin["cursor"] = "heart" 
        self.selctLab.grid(row=0,column=0)
        self.selectClrLab.grid(row=0,column=1)
        
#Button for 'New Game' option
        self.savs=['Save in File '+str(i) for i in range(5)]
        self.sav = StringVar()
        self.sav.set(self.savs[0])
        self.dropSav = tk.OptionMenu( self , self.sav , *self.savs) #The option menu for user to select which file they want their game saved in
        self.dropSav.grid(row=999,column=3,pady=20)        
        self.NewGBtn=tk.Button(self,text='New Game',width=10,bg='#b94e6f',font='Helvetica 8 bold',command=lambda:self.parent.__init__(self.master)) #New game button
        self.NewGBtn.grid(row=1000,column=3)
        self.Save=tk.Button(self,text='Save Game',width=10,bg='#e0b0bf',font='Helvetica 8 bold') 
        self.Save.grid(row=1001,column=3)
        self.Save.bind('<Button-1>',lambda x:self.Saving()) 

#Function creating the length combinations
    def LengthCombinations(self,lst, n):  
        if n == 0:
            return [[]]
        
        l =[] #List with combinations for game mode of the computer vs itself 
        for i in range(0, len(lst)):
            
            m = lst[i]
            remLst = lst[i + 1:]
            
            for p in self.LengthCombinations(remLst, n-1): #To run colour combinations
                l.append([m]+p)
                
        return l    

#Function to allow the user/computer to make their guess
    def NextGuess(self, start=False):
        for colour in self.GuessedPinColours(): #To check for blank pegs
            if colour == "#a3264c" and not start:
                return None

#Reset to allow for next guess
        self.ResetColours()
        self.allGuesses[self.activeGuess].config(bg=self.bg)    
        for pin in self.allGuessPins[self.activeGuess]: #All formerly linked labels and buttons are undone
            pin.unbind("<1>")
            pin["cursor"] = "heart"

#To mark pins used for a guess
        score = self.GuessCheck(self.GuessedPinColours(), self.answer) 
        if not start and len(score) != 0:
            score = self.GuessCheck(self.GuessedPinColours(), self.answer)
            self.clr2save.append(self.GuessedPinColours())

            score.sort(reverse=True) #Sorting the guess sort list from right to wrong in descending order
            for i, pin in enumerate(self.allMarkPins[self.activeGuess]):    
                if i > len(score)-1:    
                    break
                if score[i]==0: #If user's score is zero this signifies there was no match between their guess and the answer
                    continue
                elif score[i]==1: #Used for a guess that matches but is in the wrong position
                    pin.config(bg='White', relief=tk.RAISED)
                elif score[i]==2: #Used for a guess that matches and is in the right position      
                    pin.config(bg='Red', relief=tk.RAISED)
                    
#Test to reveal the winning player 
        if score == [2 for _ in range(self.numberOfHoles)]: #All red = Win
            self.answerCover.grid_forget()  
            self.answerFrame.grid(row=0, column=1, pady=15) #Revealing the answer
            self.guessBtn["command"] = None
            messagebox.showinfo("WINNER", "Congratulations! YOU are the Master Mind - You go girl!")
            return None

#Moving up and highlighting the new row after a guess 
        self.lis=[i-1 for i in range(self.numberOfGuesses,0,-1)]
        if self.lis[self.activeGuess]<self.numberOfGuesses:
            if self.gameType=='GvsT' and self.BackToGamerGirl:
                self.activeGuess -= 1
                self.allGuesses[self.activeGuess].config(bg=self.fg) #To change the colour of a clicked label
                for i, pin in enumerate(self.allGuessPins[self.activeGuess]):
                    pin.bind("<1>", lambda event, i=i: self.PinColourChange(event, i))
                    pin["cursor"] = "heart"
            else:
                if self.BackToGamerGirl:    
                    self.guessComp=random.choice(self.combination)  #If its the computer's turn it will randomly make a guess from the guess combination
                    if self.step==self.steps and self.steps!=0: 
                        self.guessComp=self.answer
                else:
                    if len(self.load[2])==0:
                        self.activeGuess=self.load[1] 
                        self.BackToGamerGirl=True 
                    print(self.load[2])
                    if len(self.load[2])!=0: 
                        self.guessComp=self.load[2].pop(0) #To pop a colour pattern
                self.count=0 
                self.activeGuess-=1
                self.steps+=1
                self.allGuesses[self.activeGuess].config(bg=self.fg) #To change the colour of the label once clicked
                self.ComputerPlay() 

        else: #If the game is over
            self.answerCover.grid_forget()  
            self.answerFrame.grid(row=0, column=1, pady=15)
            self.guessBtn["command"] = None
            messagebox.showinfo("LOSER", "This Game is Over! Maybe try harder next time Girlll?...") #End of game display message
            self.parent.clear() 
            self.parent.GameMainMenu()
            return None

#Function for The Computer vs Itself (Computer) game mode
    def ComputerPlay(self):
        pin=self.allGuessPins[self.activeGuess] 
        if self.count<len(self.guessComp): #Checks number of computer moves against the column number
            self.clrSelect=self.guessComp[self.count] #To select the colour of a label
            pin[self.count].config(bg=self.clrSelect, relief=tk.RAISED) 
            self.count+=1   
            self.master.after(self.time,self.ComputerPlay) 
        else:
            self.NextGuess()   

    @staticmethod #(to eliminate the use of the self argument)
    def GuessCheck(guess, answer):
        cLis={"#9400D3":'Violet', "#FF0000":'Red', "#FFFF00":'Yellow', "#F2ACB9":'Baby Pink', 
                "#D3D3D3":'Light Grey',"#FFA500":'Orange', "#D9027D":'Fushia', "#E5B6F7":'Lilac','#a3264c':'darkpink'}
        answer = answer.copy()
        reds = [2 if secret == guess_item else 0 for secret, guess_item in zip(answer, guess)]
        whites = [] 
        for guess_item in guess: 
            if guess_item in answer: 
                answer[answer.index(guess_item)] = None
                whites.append(1)
            else: 
                whites.append(0) 
        score=[0 for i in range(len(reds))]
        for i in range(len(reds)):
            if reds[i]!=2:
                score[i]=reds[i]+whites[i]
            else:
                score[i]=reds[i] 
        return score

#Function to get the colours of the guessed pin
    def GuessedPinColours(self):
        return [pin["bg"] for pin in self.allGuessPins[self.activeGuess]]   
    
#Function to change the colour of the pin once it has been raised
    def PinColourChange(self, event, i):
        event.widget.config(bg=self.clrSelect, relief=tk.RAISED)    
        
#Function to change the user's selected colour peg
    def SelectedColourChange(self, event, i): 
        ind=i
        self.clrSelect=self.colours[ind] 
        self.selectClrLab.config(bg=self.clrSelect, relief=tk.SUNKEN) 
        
#Function to rest all of the colours
    def ResetColours(self):
        self.colourCycles = it.tee(it.cycle(self.colours), self.numberOfHoles)  

#________________________________________________________________________________________________________________________________________________________

#PART 4: Building the MASTERMIND GAME 2/2 (Saving)

#Function to save the game
    def Saving(self):
        nam=self.sav.get() #Get game data
        lists=self.DataforSaveFile() #Data is changed to list form
        lisSavable=self.Savables(lists) #Converted to a format that can be saved
        self.DataturnedText(lisSavable,'Saves\\'+nam+'.txt') 
        self.MMSavedGames[int(nam[-1])]='1'
        self.DataturnedText(self.MMSavedGames, 'MMSavedGames.txt')   

#Function to process the game data into a saved file
    def DataforSaveFile(self):
        lis=[[self.numberOfHoles,self.numberOfGuesses],self.activeGuess,self.clr2save,self.answer]  
        return lis
    
#Function to transfer the data to a recoverable file
    def Savables(self,lists):
        data=[[] for i in range(4)] #Data is split 
        data[0]=','.join([str(lists[0][0]),str(lists[0][0])]) #Columns and rows are placed first
        data[1]=str(lists[1]+1) 
        outLis=[]
        for i in lists[2]:
            for j in i:
                outLis.append(j)
        data[2]=','.join(outLis) 
        data[3]=','.join(lists[3])  
        return data

#Function to send the saved data sequentially into a text file
    def DataturnedText(self,lists,directory):
        nam=open(directory,'w') 
        nam.close() 
        nam=open(directory,'a')         
        for i in range(len(lists)): 
            argument=lists[i]+'\n'  
            nam.write(argument)
        nam.close() 


if __name__ == "__main__":
    root = tk.Tk()  #Root window
    root.title("Linde's MASTERMIND Game for Girls! #WomenInTech")     
    gamemenu=GameMenu(root) #Game menu object
    root.mainloop() 

#________________________________________________________________________________________________________________________________________________________