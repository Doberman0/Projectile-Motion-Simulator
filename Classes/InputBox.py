import pygame, math, sys, random, copy
from pygame.locals import *

class InputBox: #Class used to make input box
    def __init__(self,PosX, PosY, Label,WordDistance,LengthValidation,RangeTuple):
        self.StartX = PosX
        self.StartY = PosY
        self.Variable = "" #String which can vary
        self.Width = 30
        self.Length = 200
        self.Label = Label #Label given to box. E.g. Displacement(m): []
        self.Surface = DISPLAYSURF
        self.Font = pygame.font.Font(None,25)
        self.BLACK = (0,0,0)
        self.TextColour = self.BLACK #Input text colour
        self.WordDistance = WordDistance #How far away you want the label to be from the box
        self.Clicked = False #Checks if the input box has been clicked or not
        self.StringLength = LengthValidation #Ensures that the length of the string doesn't exceed a certain length. E.g No more than 5 characters
        self.Range = RangeTuple #Range of results allowed. E.g. 0 - 100.0 inclusive

    def MakeBox(self):
        #Makes the input box
        TopLine = pygame.draw.line(self.Surface, self.BLACK,(self.StartX-2,self.StartY),
                                   (self.StartX+self.Length+2,self.StartY),1)
        LeftLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX-2,self.StartY),
                                    (self.StartX-2,self.StartY+self.Width+2),1)
        BottomLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX-2,self.StartY+self.Width+2),
                                    (self.StartX+self.Length+2,self.StartY+self.Width+2),1)
        RightLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX+self.Length+2,self.StartY),
                                    (self.StartX+self.Length+2,self.StartY+self.Width+2),1)

        self._AddLabel() #Adds a label to the checkbox
        self._DisplayVariable() #Shows Variable on screen
        self._DisplayRange() #Displays the minimum & maximum value that can be entered

    def _AddLabel(self): #Private method used to add a label to a checkbox
        LabelX = self.StartX - self.WordDistance - 5
        LabelY = self.StartY + 3
        Text = self.Font.render(self.Label,1,self.TextColour)
        #Display the label
        self._AddText(Text, (LabelX,LabelY))

    def _DisplayVariable(self): #Private method which is meant to display the variable
        XStart = self.StartX + 5
        YStart = self.StartY + 3
        Text = self.Font.render(self.Variable,1,self.TextColour)
        #Display the variable
        self._AddText(Text, (XStart,YStart))

    def _DisplayRange(self): #Private method which enables the user to see the range of values permitted
        XStart = self.StartX + self.Length + 15
        YStart = self.StartY - 5
        MinText = self.Font.render('Min: ' + str(float(self.Range[0])),1,self.TextColour)
        MaxText = self.Font.render("Max: " + str(float(self.Range[1])),1,self.TextColour)
        #Display Range
        self._AddText(MinText, (XStart,YStart))
        self._AddText(MaxText, (XStart, YStart+20))

    def _AddText(self, Text, CoordinatesTuple): #Private method used to display text
        self.Surface.blit(Text, (CoordinatesTuple[0], CoordinatesTuple[1]))

    def ClickInRange(self, PositionTuple): #Checks if a mouse click is in range of the checkbox
        if (PositionTuple[0] in range(self.StartX, self.StartX+self.Length+1)) and (PositionTuple[1] in range(self.StartY, self.StartY+self.Width+1)):
            self.Clicked = True
        else:
            self.Clicked = False #This means that if the click is out of the box you can no longer enter variables in the box

    def AddCharacter(self, Input): #Adds character from alphabet -> ['1','2','3','4,'5','6','7','8','9','.',BACKSPACE]
        if (Input == K_1) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(1)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(1)
                else:
                    self.Variable += "1"
        elif (Input == K_2) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(2)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(2)
                else:
                    self.Variable += "2"
        elif (Input == K_3) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(3)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(3)
                else:
                    self.Variable += "3"
        elif (Input == K_4) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(4)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(4)
                else:
                    self.Variable += "4"
        elif (Input == K_5) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(5)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(5)
                else:
                    self.Variable += "5"
        elif (Input == K_6) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(6)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(6)
                else:
                    self.Variable += "6"
        elif (Input == K_7) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(7)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(7)
                else:
                    self.Variable += "7"
        elif (Input == K_8) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(8)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(8)
                else:
                    self.Variable += "8"
        elif (Input == K_9) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(9)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(9)
                else:
                    self.Variable += "9"
        elif (Input == K_0) and (len(self.Variable)<self.StringLength):
            if self._NumInRange(0)==True:
                if "." in self.Variable:
                    self.Variable = self._AdjustVariable(0)
                else:
                    self.Variable += "0"
        elif (Input == K_PERIOD) and (len(self.Variable)<self.StringLength):
            if "." not in self.Variable: #You should only be able to enter a decimal ('.') if the variable doesn't already have one
                self.Variable += "."

        elif (Input == K_BACKSPACE): #Deletes the final character in 'Variable'
            self.Variable = self.Variable[:-1]

    def _AdjustVariable(self,String): #Private method that adjusts the input so that it is always to 1dp
        self.Variable += str(String)
        self.Variable = "%0.2f" % float(self.Variable)
        return self.Variable[:-1]

    def _NumInRange(self, Num): #Checks if the number will be in range and returns if this is the case or not
        if (float(self.Variable + str(Num))>=self.Range[0]) and (float(self.Variable + str(Num))<=self.Range[1]):
            return True
        else:
            return False
