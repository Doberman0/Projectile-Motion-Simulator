import pygame, math, sys, random, copy
from pygame.locals import *

class CheckBox:
    def __init__(self, PosX, PosY, Width,Surface,Label,WordDistance):
        self.Surface = Surface #What surface the box will be drawn on
        self.StartX = PosX
        self.StartY = PosY
        self.Width = Width #Determines the dimensions of the box (will always be a*a dimensions)
        self.Thickness = 8 #Determines thickness of tick
        self.GREEN = (0,255,0) #The colour of the tick
        self.BLACK = (0,0,0) #Box outline colour
        self.Clicked = False
        self.Label = Label
        self.Font= pygame.font.Font(None,25) #Using Pygame's default font
        self.TextColour = self.BLACK #Text colour will be black
        self.WordDistance = WordDistance #Allows the user to customise how far away the checkbox is away from the user

    def MakeBox(self): #Makes box by drawing lines on the surface
        TopLine = pygame.draw.line(self.Surface, self.BLACK,(self.StartX-2,self.StartY),
                                   (self.StartX+self.Width+2,self.StartY),1)
        LeftLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX-2,self.StartY),
                                    (self.StartX-2,self.StartY+self.Width+2),1)
        BottomLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX-2,self.StartY+self.Width+2),
                                    (self.StartX+self.Width+2,self.StartY+self.Width+2),1)
        RightLine = pygame.draw.line(self.Surface,self.BLACK,(self.StartX+self.Width+2,self.StartY),
                                    (self.StartX+self.Width+2,self.StartY+self.Width+2),1)
        self._AddLabel() #Adds a label to the checkbox
        if self.Clicked == True:
            self._AddTick() #Adds tick

    def ClickInRange(self, PositionTuple): #Checks if a mouse click is in range of the checkbox
        if (PositionTuple[0] in range(self.StartX, self.StartX+self.Width+1)) and (PositionTuple[1] in range(self.StartY, self.StartY+self.Width+1)):
            #This allows you to check and uncheck the box
            if self.Clicked == True:
                self.Clicked = False
            else:
                self.Clicked = True

    def _TickCoordinates(self): #A private method that allows me to get the coordinates of 2 lines which will form to make one tick
        X1 = self.StartX
        Y1 = self.StartY + (self.Width//2)
        X2 = self.StartX + (self.Width//2)
        Y2 = self.StartY + self.Width
        X3 = self.StartX + self.Width
        Y3 = self.StartY
        return X1,Y1,X2,Y2, X3,Y3

    def _AddTick(self):
           #Initialise coordinates
           FirstX,FirstY,SecondX,SecondY,ThirdX,ThirdY = self._TickCoordinates() #Private methods used to get coordinates of tick
           #Actually Draws Lines => making the tick
           pygame.draw.line(self.Surface, self.GREEN, (FirstX,FirstY),(SecondX,SecondY),self.Thickness)
           pygame.draw.line(self.Surface, self.GREEN, (SecondX, SecondY),(ThirdX,ThirdY),self.Thickness)

    def _AddLabel(self): #Private method used to add a label to a checkbox
        LabelX = self.StartX - self.WordDistance
        LabelY = self.StartY + 8
        Text = self.Font.render(self.Label,1,self.TextColour)
        self.Surface.blit(Text, (LabelX,LabelY))
