import pygame, math, sys, random, copy
from pygame.locals import *

class Button:
    def __init__(self, Label, PosXStart, PosYStart, Width, Length, Surface):
        self.Label = Label
        self.PosXStart = PosXStart
        self.PosYStart = PosYStart
        self.Width = Width
        self.Length = Length
        self.BackgroundColour = (51,153,255) #Sexy blue colour for all buttons
        self.Surface = Surface
        self.Font = pygame.font.Font(None, 32)
        self.TextColour = (0,0,0) #Black

    def DisplayButton(self): #Method used to draw the button
        Button = pygame.draw.rect(self.Surface, self.BackgroundColour, (self.PosXStart, self.PosYStart, self.Length, self.Width))
        self._MakeLabel()

    def _MakeLabel(self):
        LabelX = (self.PosXStart + 10)
        LabelY = (self.PosYStart + (self.Length//20))
        ButtonText = self.Font.render(self.Label,1,self.TextColour)
        self.Surface.blit(ButtonText, (LabelX,LabelY))

    def ClickInRange(self, PositionTuple):
        if (PositionTuple[0] in range(self.PosXStart, self.PosXStart+self.Length+1)) and (PositionTuple[1] in range(self.PosYStart, self.PosYStart+self.Width+1)):
            return True
        else:
            return False
